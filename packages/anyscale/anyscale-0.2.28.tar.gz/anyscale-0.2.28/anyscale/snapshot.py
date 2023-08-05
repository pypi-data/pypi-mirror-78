import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
from subprocess import STDOUT
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union

import click
import ray.ray_constants
import requests

from anyscale.conf import (
    BACKUP_CONTAINER_IMAGE,
    DOCKER_REGISTRY,
    DOCKER_SNAPSHOT_BUCKET,
    REGISTRY_IMAGE,
)
from anyscale.project import get_project_id
from anyscale.util import (
    check_is_feature_flag_on,
    confirm,
    get_cluster_config,
    get_requirements,
    send_json_request,
    Timer,
)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)

REGISTRY_CONF_PATH = "/etc/docker/registry/config.yml"

REGISTRY_CONF_TEMPLATE = """
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  s3:
    accesskey: {ACCESS_KEY}
    secretkey: {SECRET_KEY}
    sessiontoken: {STS_TOKEN}
    region: {REGION}
    bucket: {BUCKET}
    rootdirectory: {S3_PATH}
http:
  addr: :5555
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
"""


def copy_file(to_s3: bool, source: str, target: Any, download: bool) -> None:
    """Copy a file.

    The file source or target may be on S3.

    Args:
        to_s3 (bool): If this is True, then copy to/from S3, else the local
            disk. If this is True, then the file source or target will be a
            presigned URL to which GET or POST HTTP requests can be sent.
        source (str or S3 URL): Source file local pathname or S3 GET URL. If
            this is an S3 URL, target is assumed to be a local pathname.
        target (str or S3 URL): Target file local pathname or S3 URL with POST
            credentials. If this is an S3 URL, source is assumed to be a local
            pathname.
        download (bool): If this is True, then this will upload from source to
            target, else this will download.
    """
    try:
        if to_s3:
            if download:
                with open(target, "wb") as f:
                    response = requests.get(source)
                    for block in response.iter_content(1024):
                        f.write(block)
            else:
                with open(source, "rb") as f:
                    files = {"file": ("object", f)}
                    resp = requests.post(
                        target["url"], data=target["fields"], files=files
                    )
                    assert resp.ok, resp.text
        else:
            shutil.copyfile(source, target)
    except (OSError, AssertionError) as e:
        logger.warn("Failed to copy file %s , aborting", source)
        raise e


def create_snapshot(
    project_definition: Any,
    yes: bool,
    description: Optional[str] = None,
    tags: List[str] = [],
) -> str:
    """Create a snapshot of a project.

    Args:
        project_definition: Project definition.
        yes: Don't ask for confirmation.
        description: An optional description of the snapshot.
        tags: Tags for the snapshot.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
        Exception: If saving the snapshot files fails.
    """
    # Find and validate the current project ID.
    project_dir = project_definition.root
    project_id = get_project_id(project_dir)

    cluster_config = get_cluster_config(
        os.path.join(project_dir, project_definition.cluster_yaml())
    )

    resp = send_json_request(
        "/api/v2/snapshots/",
        {
            "project_id": project_id,
            "project_config": json.dumps(project_definition.config),
            "cluster_config": json.dumps(cluster_config),
            "description": description if description else "",
            "tags": tags,
        },
        method="POST",
    )
    snapshot_uuid: str = resp["result"]["id"]
    return snapshot_uuid


def describe_snapshot(uuid: str) -> Any:
    resp = send_json_request("/api/v2/snapshots/{}".format(uuid), {})
    return resp["result"]


def list_snapshots(project_dir: str) -> List[str]:
    """List all snapshots associated with the given project.

    Args:
        project_dir: Project root directory.

    Returns:
        List of Snapshots for the current project.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("/api/v2/snapshots/", {"project_id": project_id})
    snapshots = resp["result"]["snapshots"]
    return [snapshot["id"] for snapshot in snapshots]


def get_snapshot_uuid(project_dir: str, snapshot_uuid: str) -> str:
    """Get a snapshot of the given project with the given name.

    Args:
        project_id: The ID of the project.
        snapshot_name: The name of the snapshot to get. If there are multiple
            snapshots with the same name, then the user will be prompted to
            choose a snapshot.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("/api/v2/snapshots/", {"project_id": project_id})
    snapshots = resp["result"]["snapshots"]
    if len(snapshots) == 0:
        raise ValueError("No snapshots found with name {}".format(snapshot_uuid))
    snapshot_idx = 0
    if len(snapshots) > 1:
        print(
            "More than one snapshot found with UUID {}. "
            "Which do you want to use?".format(snapshot_uuid)
        )
        for i, snapshot in enumerate(snapshots):
            print("{}. {}".format(i + 1, snapshot["uuid"]))
        snapshot_idx = click.prompt(
            "Please enter a snapshot number from 1 to {}".format(len(snapshots)),
            type=int,
        )
        snapshot_idx -= 1
        if snapshot_idx < 0 or snapshot_idx > len(snapshots):
            raise ValueError("Snapshot index {} is out of range".format(snapshot_idx))
    result: str = snapshots[snapshot_idx]["id"]
    return result


def generate_docker_image_name(project_id: int, snapshot_id: str) -> str:
    tag = f"{project_id}_{snapshot_id}"
    return DOCKER_REGISTRY + "/snapshots:" + tag


## Backup container schema
## /root/backup
##      - project_directory/  # Mounted to the {project_directory}
##      - file_mounts/        # Contains all normal {file_mounts}
## /root/save_dir
##      - Exact copy of /root/backup, BUT ALL LOCAL
## /root/backup/ is rsync'd to /root/save_dir/ (NOTE the "/" at the end of both)
def start_backup_container_command(
    cluster_config: Dict[str, Any], session_id: int, directory_name: str
) -> str:
    docker_mounts = [
        "-v {dst}:/root/backup/file_mounts/{dst}:ro"
        for dst in cluster_config.get("file_mounts", {}).keys()
    ]

    docker_mounts.append(
        f"-v $HOME/{directory_name}:/root/backup/project_directory/:ro "
    )

    return (
        f"docker run --rm --name backup_container_{session_id} -d -it "
        + " ".join(docker_mounts)
        + f"{BACKUP_CONTAINER_IMAGE} bash || true"
    )


def restore_docker_snapshot_commands(
    cluster_config: Dict[str, Any],
    session_id: int,
    project_id: int,
    snapshot_id: str,
    directory_name: str,
) -> List[str]:
    new_image_name = generate_docker_image_name(project_id, snapshot_id)

    docker_mounts = [
        "-v {dst}:/root/backup/file_mounts/{dst}"
        for dst in cluster_config.get("file_mounts", {}).keys()
    ]

    docker_mounts.append(f"-v $HOME/{directory_name}:/root/backup/project_directory/ ")

    restore_commands = [
        f"mkdir -p {mount}" for mount in cluster_config.get("file_mounts", {}).keys()
    ]

    restore_commands.append(f"mkdir -p $HOME/{directory_name}")

    mount_string = " ".join(docker_mounts)
    # TODO(ilr) Move away from /root in container.
    restore_commands.extend(
        [
            f"docker run --rm --name temp_backup_{session_id} -d -it {mount_string} {new_image_name}-files bash",
            f"docker exec temp_backup_{session_id} rsync -a /root/save_dir/ /root/backup/",
            f"docker stop temp_backup_{session_id}",
        ]
    )
    return restore_commands


def restart_registry_commands(user_aws_credentials: Any, project_id: int,) -> List[str]:
    registry_config_content = REGISTRY_CONF_TEMPLATE
    registry_config_content = registry_config_content.format(
        ACCESS_KEY=user_aws_credentials["AWS_ACCESS_KEY_ID"],
        SECRET_KEY=user_aws_credentials["AWS_SECRET_ACCESS_KEY"],
        STS_TOKEN=user_aws_credentials["AWS_SESSION_TOKEN"],
        REGION="us-west-2",  # TODO: revisit for customer accounts.
        BUCKET=DOCKER_SNAPSHOT_BUCKET,  # TODO: revisit for customer accounts.
        S3_PATH=f"docker/{project_id}",
    )

    return [
        f"docker stop registry || true && mkdir -p /tmp/docker/registry/ && cat >/tmp/docker/registry/config.yml <<'EOL'{registry_config_content}\nEOL",
        f"docker run -d -p 5555:5555 -v /tmp/docker/registry/config.yml:{REGISTRY_CONF_PATH} --name registry {REGISTRY_IMAGE}  || docker start registry",
    ]

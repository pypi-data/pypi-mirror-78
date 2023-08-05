from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# mypy: ignore-errors

import os
import re
import shutil
import zipfile

from setuptools import Distribution, find_packages, setup
import setuptools.command.build_ext as _build_ext


def find_version(path):
    with open(path) as f:
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE)
        if match:
            return match.group(1)
        raise RuntimeError("Unable to find version string.")


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):  # noqa: N
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True


except ImportError:
    bdist_wheel = None


class build_ext(_build_ext.build_ext):  # noqa: N
    def run(self):
        import io
        import requests
        import tarfile
        import tempfile
        import bz2

        work_dir = tempfile.mkdtemp()
        try:
            url = "https://anyscale-dev.s3-us-west-2.amazonaws.com/fswatch-1.14.0-2.zip"
            content = requests.get(url).content

            fswatch = zipfile.ZipFile(io.BytesIO(content))
            fswatch.extractall(pwd=work_dir.encode())
            for f in [
                "fswatch-linux",
                "fswatch-darwin",
                "libfswatch.11.dylib",
            ]:
                destination = os.path.join("anyscale", f)
                # Remove the file if it already exists to make sure old
                # versions get removed.
                try:
                    os.remove(destination)
                except OSError:
                    pass
                shutil.copy2(f, destination)
                os.chmod(destination, 0o755)
                self.move_file(destination)

        finally:
            shutil.rmtree(work_dir)

    def move_file(self, filename):
        # TODO(rkn): This feels very brittle. It may not handle all cases. See
        # https://github.com/apache/arrow/blob/master/python/setup.py for an
        # example.
        source = filename
        destination = os.path.join(self.build_lib, filename)
        # Create the target directory if it doesn't already exist.
        parent_directory = os.path.dirname(destination)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        if not os.path.exists(destination):
            print("Copying {} to {}.".format(source, destination))
            shutil.copy(source, destination, follow_symlinks=True)


class BinaryDistribution(Distribution):
    def is_pure(self):
        return True

    def has_ext_modules(self):
        return True


setup(
    name="anyscale",
    version=find_version("anyscale/__init__.py"),
    author="Anyscale Inc.",
    description=("Command Line Interface for Anyscale"),
    packages=find_packages(exclude="tests"),
    cmdclass={"bdist_wheel": bdist_wheel, "build_ext": build_ext},
    distclass=BinaryDistribution,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "boto3",
        "Click>=7.0",
        "GitPython",
        "jsonpatch",
        "jsonschema",
        "ray>=0.8.5",
        "requests",
        "tabulate",
        "aiohttp",
    ],
    entry_points={"console_scripts": ["anyscale=anyscale.scripts:main"]},
    include_package_data=True,
    zip_safe=False,
)

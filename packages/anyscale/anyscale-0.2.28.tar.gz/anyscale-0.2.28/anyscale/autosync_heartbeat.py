from contextlib import contextmanager
from threading import Event, Thread
import time
from typing import Iterator

from anyscale.util import send_json_request

TIME_BETWEEN_HEARTBEATS = 30  # seconds


@contextmanager
def managed_autosync_session(session_id: int) -> Iterator[str]:
    # Register to the API that we enabled autosync
    resp = send_json_request(
        "/api/v2/autosync_sessions/?session_id={}".format(session_id),
        {},
        method="POST",
    )
    autosync_session_id = resp["result"]["id"]
    heartbeat_thread = AutosyncHeartbeat(autosync_session_id)
    heartbeat_thread.start()

    try:
        yield autosync_session_id
    finally:
        heartbeat_thread.finish.set()
        send_json_request(
            "/api/v2/autosync_sessions/{}".format(autosync_session_id),
            {},
            method="DELETE",
        )
        heartbeat_thread.join()
        print("Autosync finished.")


class AutosyncHeartbeat(Thread):
    def __init__(self, autosync_session_id: str):
        super().__init__()
        self.autosync_session_id = autosync_session_id
        self.finish = Event()

    def run(self) -> None:
        while not self.finish.is_set():
            try:
                print("heartbeat sending")
                send_json_request(
                    "/api/v2/autosync_sessions/{}/heartbeat".format(
                        self.autosync_session_id
                    ),
                    {},
                    method="POST",
                )
            except Exception as e:
                print("Error sending heartbeat:", e)
            self.finish.wait(TIME_BETWEEN_HEARTBEATS)

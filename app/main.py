import os
import threading
from typing import List

import uvicorn
from fastapi import FastAPI

from app.capture import Capture
from app.config.logging_config import get_logger
from app.model.http_packet import HttpPacket
from app.utils import get_available_port

LOGGER = get_logger("capture")


class API(FastAPI):
    def __init__(self, capture: Capture) -> None:
        super(API, self).__init__(
            title="Docker Network Traffic Capturer",
            docs_url="/",
        )

        @self.get("/health")
        def health() -> str:
            return "OK"

        @self.get(
            "/",
            response_model=List[HttpPacket],
            summary="Get all packets that have been captured so far",
            description=(
                "Returns all packets that have been captured since the start of "
                "recording or - if `collect` has been called in the meantime - since "
                "the last time `collect` was called."
            ),
        )
        def get_packets() -> List[HttpPacket]:
            return capture.get_all()

        @self.get(
            "/collect",
            response_model=List[HttpPacket],
            summary="Collect all captured packets and then reset the internal memory",
            description="Returns all packages that have been recorded since the last time this method was called.",
        )
        def collect() -> List[HttpPacket]:
            return capture.collect()

        @self.post(
            "/collect/file/{filename}",
            summary="Collect all captured packets, store them into the given file and then reset the internal memory",
            description=(
                "Collects all packages that have been recorded since the last time `collect` was called and stores "
                "all captured packets in a file with the given name."
            ),
        )
        def collect_to_file(filename: str):
            capture.collect_to_file(filename)

        @self.on_event("shutdown")
        def _on_shutdown():
            capture.stop()


def _start_capture() -> Capture:
    """Validates the requirements for network capturing and
    then starts a live capture in a new thread."""
    capture = Capture()
    thread = threading.Thread(target=capture.start)
    thread.start()
    return capture


def _start_api(capture: Capture):
    """Starts the REST-API. If not predefined in an environment variable
    named `FIXED_API_PORT`, a random port is used for the API.
    The port which is used stored in a file named `API_PORT`."""
    if "FIXED_API_PORT" in os.environ:
        port = os.getenv("FIXED_API_PORT")
    else:
        port = get_available_port()

    with open("API_PORT", "w") as file:
        file.write(str(port))
    LOGGER.info(f"Exported port {port} to file 'API_PORT'.")

    uvicorn.run(API(capture), host="0.0.0.0", port=port)  # type: ignore


if __name__ == "__main__":
    capture = _start_capture()
    _start_api(capture)

import threading
from typing import List

import uvicorn
from fastapi import FastAPI

from app.capture import Capture
from app.model.http_packet import HttpPacket


class API(FastAPI):
    def __init__(self, capture: Capture) -> None:
        super(API, self).__init__(
            title="Docker Network Traffic Capturer",
            docs_url="/",
        )

        @self.get("/health")
        def health() -> str:
            return "OK"

        @self.get("/collect")
        def collect() -> List[HttpPacket]:
            return capture.collect()


def _start_capture() -> Capture:
    capture = Capture()
    thread = threading.Thread(target=capture.start)
    thread.start()
    return capture


def _start_api(capture: Capture):
    uvicorn.run(API(), host="0.0.0.0", port=8000)  # type: ignore


if __name__ == "__main__":
    capture = _start_capture()
    _start_api(capture)

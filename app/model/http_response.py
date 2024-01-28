from typing import Optional

from app.model.http_packet import HttpPacket


class HttpResponse(HttpPacket):
    """Represents one captured HTTP response packet."""

    status_code: int
    """Response code of the HTTP response."""

    status_code_description: str
    """Description of the response code of the HTTP response."""

    request_in: Optional[int]
    """Frame number of the request to which this response corresponds."""

    duration: Optional[float]
    """Duration of the response in seconds, i.e. the time since the request."""

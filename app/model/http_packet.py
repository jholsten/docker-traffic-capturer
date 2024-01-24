from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.model.http_request import HttpRequest
from app.model.http_response import HttpResponse


class HttpPacket(BaseModel):
    """Represents one captured HTTP packet."""

    timestamp: datetime
    """Timestamp of when this packet was sent."""

    source_ip: str
    """IP address of the host which has sent this packet."""

    source_port: int
    """Port of the application which has sent this packet."""

    destination_ip: str
    """IP address of the host which has received this packet."""

    destination_port: int
    """Port of the application which has received this packet."""

    request: Optional[HttpRequest]
    """Additional information about the HTTP request. Is only set
    if this packet represents a request."""

    response: Optional[HttpResponse]
    """Additional information about the HTTP response. Is only set
    if this packet represents a response."""

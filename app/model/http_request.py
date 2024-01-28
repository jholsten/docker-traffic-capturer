from app.model.http_packet import HttpPacket


class HttpRequest(HttpPacket):
    """Represents one captured HTTP request packet."""

    uri: str
    """URI of the HTTP request."""

    method: str
    """HTTP method of the HTTP request."""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class HttpResponse(BaseModel):
    """Represents the information about a captured HTTP response."""

    version: str
    """HTTP protocol version which was used for the HTTP response."""

    status_code: int
    """Response code of the HTTP response."""

    status_code_description: str
    """Description of the response code of the HTTP response."""

    request_in: Optional[int]
    """Frame number of the request to which this response corresponds."""

    duration: Optional[float]
    """Duration of the response in seconds, i.e. the time since the request."""

    headers: Dict[str, str]
    """Response headers as map of key and value."""

    payload: Optional[Any]
    """Response body of the HTTP response."""

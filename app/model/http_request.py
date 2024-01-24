from typing import Any, Dict, Optional

from pydantic import BaseModel


class HttpRequest(BaseModel):
    """Represents the information about a captured HTTP request."""

    version: str
    """HTTP protocol version which was used for the HTTP request."""

    uri: str
    """URI of the HTTP request."""

    method: str
    """HTTP method of the HTTP request."""

    headers: Dict[str, str]
    """Request headers as map of key and value."""

    payload: Optional[Any]
    """Request body of the HTTP request."""

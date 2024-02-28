from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class HttpPacketType(str, Enum):
    """Type of a HTTP packet."""

    REQUEST = "REQUEST"
    """Packet represents a request."""

    RESPONSE = "RESPONSE"
    """Packets represents a response."""


class HttpPacket(BaseModel):
    """Represents one captured HTTP packet."""

    number: int
    """Frame number of this packet."""

    network_id: str
    """ID of the network in which this packet was captured."""

    timestamp: datetime
    """Timestamp of when this packet was sent."""

    type: HttpPacketType
    """Type of this HTTP packet."""

    source_ip: str
    """IP address of the host which has sent this packet."""

    source_port: int
    """Port of the application which has sent this packet."""

    destination_ip: str
    """IP address of the host which has received this packet."""

    destination_port: int
    """Port of the application which has received this packet."""

    version: str
    """HTTP protocol version which was used."""

    headers: Dict[str, List[str]]
    """Request/Response headers as map of key and values."""

    payload: Optional[Any]
    """Request/Response body of this packet."""

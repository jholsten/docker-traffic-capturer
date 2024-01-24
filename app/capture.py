import os
from typing import Dict, List, Optional, Tuple, cast

import pyshark
from pyshark.packet.fields import LayerField, LayerFieldsContainer
from pyshark.packet.layers.base import BaseLayer
from pyshark.packet.packet import Packet as PysharkPacket
from pyshark.tshark import tshark

from app.config.logging_config import get_logger
from app.model.http_packet import HttpPacket
from app.model.http_request import HttpRequest
from app.model.http_response import HttpResponse

LOGGER = get_logger("capture")


class Capture:
    """Service which captures all HTTP packets in a Docker network.
    The ID of the Docker network has to be specified in the environment
    variable `NETWORK_ID` when the application is started.

    Upon request, all packets collected since the last request can be
    retrieved. This resets the internal memory and returns all packets
    collected so far.
    """

    network_id: str
    """ID of the Docker network for which packets are to be captured."""

    _packets: List[HttpPacket]
    """Packets that have been collected so far since the last call to 
    the `collect` method."""

    @property
    def interface_id(self) -> str:
        """ID of the network interface on which the traffic is monitored.
        For Docker bridge networks, this is composed of the prefix `br-`
        and the `network_id` truncated to 12 characters."""
        return "br-" + self.network_id[:12]

    def __init__(self):
        network_id = os.environ.get("NETWORK_ID")
        if not network_id:
            raise Exception("Environment variable 'NETWORK_ID' needs to be set.")
        if not len(network_id) not in [12, 64]:
            raise Exception("Network ID needs to correspond to either the non-truncated SHA-256 ID or the ID truncated to 12 characters.")
        LOGGER.info(f"Will capture packets for network {network_id}.")
        self._assert_interface_id_exists()

    def start(self):
        """Starts capturing HTTP packets on the `interface_id`."""
        LOGGER.info(f"Starting to capture HTTP packets on interface ID {self.interface_id}.")
        capture = pyshark.LiveCapture(interface=self.interface_id, capture_filter="http")
        capture.apply_on_packets(self._on_packet_captured)

    def collect(self) -> List[HttpPacket]:
        raise Exception()  # TODO

    def _on_packet_captured(self, packet: PysharkPacket):
        """Callback function which is executed when a new package was captured.
        Parses the packet and stores it in local memory."""
        http_packet = self._parse_http_packet(packet)
        if http_packet is not None:
            self._packets.append(http_packet)

    def _assert_interface_id_exists(self):
        """Asserts that the `interface_id` is available on this host."""
        available_interfaces = [i.lower() for i in cast(List[str], tshark.get_all_tshark_interfaces_names())]
        if self.interface_id.lower() not in available_interfaces:
            raise Exception(
                f"Interface {self.interface_id} does not exist, unable to initiate capture. "
                "Did you start this Docker container with network mode 'host'?\n"
                f"Possible interfaces: [{', '.join(available_interfaces)}]"
            )

    def _parse_http_packet(self, packet: PysharkPacket) -> Optional[HttpPacket]:
        """Parses the given `packet` captured by pyshark to an instance of `HttpPacket`.
        Returns `None` in case the given package does not contain an HTTP layer."""
        if "http" not in packet:
            return None
        request = self._parse_request(packet.http)
        response = self._parse_response(packet.http)
        source_port, destination_port = self._get_ports(packet)
        source_ip, destination_ip = self._get_ip_addresses(packet)
        return HttpPacket(
            timestamp=packet.sniff_time,
            source_ip=source_ip,
            source_port=source_port,
            destination_ip=destination_ip,
            destination_port=destination_port,
            request=request,
            response=response,
        )

    def _parse_request(self, http_layer: BaseLayer) -> Optional[HttpRequest]:
        """Parses information from the given `http_layer` to an instance of `HttpRequest`.
        Returns `None` in case the layer does not contain any request information, i.e.
        the packet represents a response."""
        if http_layer.get("request") is None:
            return None
        return HttpRequest(
            version=str(http_layer.get("request_version")),
            uri=str(http_layer.get("request_uri")),
            method=str(http_layer.get("request_method")),
            headers=self._parse_headers(cast(LayerFieldsContainer, http_layer.get("request_line")).all_fields),
            payload=http_layer.get("file_data"),
        )

    def _parse_response(self, http_layer: BaseLayer) -> Optional[HttpResponse]:
        """Parses information from the given `http_layer` to an instance of `HttpResponse`.
        Returns `None` in case the layer does not contain any response information, i.e.
        the packet represents a request."""
        if http_layer.get("response") is None:
            return None
        return HttpResponse(
            version=str(http_layer.get("response_version")),
            status_code=cast(int, http_layer.get("response_code")),
            status_code_description=str(http_layer.get("response_code_desc")),
            headers=self._parse_headers(cast(LayerFieldsContainer, http_layer.get("response_line")).all_fields),
            payload=http_layer.get("file_data"),
        )

    def _parse_headers(self, line: Optional[List[LayerField]]) -> Dict[str, str]:
        """Parses headers from the given request or response line."""
        if not line:
            return {}
        headers: Dict[str, str] = {}
        for entry in line:
            key = str(entry.showname_key)
            value = str(entry.showname_value).replace("\\n", "").replace("\\r", "")
            headers[key] = value
        return headers

    def _get_ports(self, packet: PysharkPacket) -> Tuple[int, int]:
        """Retrieves source and destination port from the transport layer of the given `packet`.

        Returns:
          - `source_port: int`
          - `destination_port: int`
        """
        transport_layer: BaseLayer = packet[packet.transport_layer]
        return cast(int, transport_layer.get("srcport")), cast(int, transport_layer.get("dstport"))

    def _get_ip_addresses(self, packet: PysharkPacket) -> Tuple[str, str]:
        """Retrieves source and destination IP address from the IP layer of the given `packet`.

        Returns:
          - `source_ip: str`
          - `destination_ip: str`
        """
        ip_layer: BaseLayer = packet.ip
        return str(ip_layer.get("src")), str(ip_layer.get("dst"))
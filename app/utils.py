import socket


def get_available_port() -> int:
    """Returns a random available port on this host."""
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]

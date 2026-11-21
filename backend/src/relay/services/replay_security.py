import ipaddress
import socket
from urllib.parse import urlsplit
from fastapi import HTTPException

def validate_destination(url: str) -> None:
    parsed = urlsplit(url)

    if parsed.scheme != "https":
        raise HTTPException(
            status_code=400,
            detail="Replay destinations must use HTTPS.",
        )

    if not parsed.hostname:
        raise HTTPException(
            status_code=400,
            detail="Invalid destination hostname.",
        )

    if parsed.username or parsed.password:
        raise HTTPException(
            status_code=400,
            detail="Credentials in destination URLs are not allowed.",
        )

    try:
        addresses = socket.getaddrinfo(
            parsed.hostname,
            parsed.port or 443,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror:
        raise HTTPException(
            status_code=400,
            detail="Destination hostname could not be resolved.",
        )

    if not addresses:
        raise HTTPException(
            status_code=400,
            detail="Destination hostname has no valid IP addresses.",
        )

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])

        if not ip.is_global:
            raise HTTPException(
                status_code=400,
                detail="Private or non-public destinations are not allowed.",
            )

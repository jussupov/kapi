import logging
import ssl
from typing import Optional
import socket

from kapi.url import URL
from kapi.response import Response

HTTP_PORT = 80
HTTPS_PORT = 443


class Request:
    def __init__(
        self,
        method: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[str] = None
    ) -> None:
        headers = {} if headers is None else headers        
        self.method = method
        self.url = URL(url)
        self.headers = headers

    def __repr__(self) -> str:
        return f"<Request [{self.method}]>"
    
    def send(self) -> Optional[Response]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            match self.url.protocol:
                case 'http':
                    return self._send(sock, port=HTTP_PORT)
                case 'https':
                    return self._send(sock, port=HTTPS_PORT)
        return None

    @staticmethod
    def _recv_response(sock) -> bytes:
        buffer = b""
        sock.settimeout(0.5)
        while True:
            try:
                chunk = sock.recv(4096)
                if chunk is None:
                    break
                buffer += chunk
            except socket.timeout:
                break
        return buffer

    @staticmethod
    def _catch_redirect(response):
        if response.status_code == 302 or response.status_code == 301:
            return Request(url=response.headers['Location']).send()
        return response

    def _send(self, sock, port=80):
        if port == HTTPS_PORT:
            sock = self.ssl_socket(sock=sock)
        sock.connect((self.url.host, port))
        request = 'GET %s HTTP/1.1\r\nHost: %s\r\n\r\n' % (
            self.url.path, self.url.host
        )
        sock.sendall(request.encode())
        buffer = self._recv_response(sock)
        return self._catch_redirect(Response(buffer))

    def ssl_socket(self, sock):
        context = ssl.create_default_context()
        return context.wrap_socket(sock, server_hostname=self.url.host)
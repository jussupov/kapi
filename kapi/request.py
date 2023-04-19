import logging
import ssl
from typing import Optional
import socket

from kapi.url import URL
from kapi.response import Response


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
        self.response: Optional[Response] = None

    def __repr__(self) -> str:
        return f"<Request [{self.method}]>"
    
    def send(self) -> Response:
        match self.url.protocol:
            case 'http':
                return self._send_http()
            case 'https':
                return self._send_https()
        return self.response

    @staticmethod
    def _recv_response(sock) -> bytes:
        buffer = b""
        sock.settimeout(2)
        while True:
            try:
                chunk = sock.recv(4096)
                if chunk is None:
                    break
                buffer += chunk
            except socket.timeout:
                break
        return buffer

    def _send_http(self) -> Response:
        pass

    def _send_https(self) -> Response:
        https_port = 443
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            s_sock = self.ssl_socket(sock=sock)
            try:
                s_sock.connect((self.url.host, https_port))
                request = 'GET %s HTTP/1.1\r\nHost: %s\r\n\r\n' % (
                    self.url.path, self.url.host
                )
                s_sock.sendall(request.encode())
                buffer = self._recv_response(s_sock)
                self.response = Response(buffer)
            except ssl.SSLError as e:
                logging.error(f"SSL error: {e}")
            except socket.error as e:
                logging.error(f"Socket error: {e}")
            except Exception as e:
                logging.error(f"Error: {e}")
            finally:
                s_sock.close()
            return self.response

    def ssl_socket(self, sock):
        context = ssl.create_default_context()
        return context.wrap_socket(sock, server_hostname=self.url.host)
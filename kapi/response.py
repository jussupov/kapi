

class Response:

    def __init__(self, response: bytes) -> None:
        self.response = response.decode()
        self.status_code = None
        self.headers = {}
        self.content = None
        self.setup()

    def _set_status_code(self):
        status_line = self.response.split('\r\n')
        self.status_code = int(status_line[0].split(' ')[1])

    def _set_content(self):
        self.content = self.response.split('\r\n\r\n')[1]

    def _set_headers(self):
        headers_text = self.response.split('\r\n', 1)[1].split('\r\n\r\n')[0]
        for header_item_text in headers_text.split('\r\n'):
            header_item = header_item_text.split(': ', 1)
            self.headers[header_item[0]] = header_item[1]

    def setup(self):
        self._set_status_code()
        self._set_headers()
        self._set_content()

    def __repr__(self):
        return '<Response [status_code: %d]>' % self.status_code

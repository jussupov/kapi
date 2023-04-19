import re

pattern = r'^(?P<protocol>[^:]+)://(?P<host>[^/:]+)(?::(?P<port>\d+))?(?P<path>[^?]*)(?:\?(?P<query>.+))?$'


class URL:

    def __init__(self, url) -> None:
        self.protocol, self.host, self.port, self.path, self.query_string, self.query_params = self.parse_url(url)

    def parse_url(self, url):
        match = re.match(pattern, url)
        match_dict = match.groupdict()
        protocol = match.group('protocol') if 'protocol' in match_dict else None
        host = match.group('host') if 'host' in match_dict else None
        port = match.group('port') if 'port' in match_dict else None
        path = match.group('path') if 'path' in match_dict else '/'
        query_string = match.group('query') if 'query' in match_dict else None
        query_params = dict(re.findall(r'(\w+)=(\w+)', query_string)) if query_string else {}
        return protocol, host, port, path, query_string, query_params

    def __str__(self):
        port = ':' + self.port if self.port else ''
        query_string = '?' + self.query_string if self.query_string else ''
        path = self.path or ''
        return f"{self.protocol}://{self.host}{port}{path}{query_string}"


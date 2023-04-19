import pytest
from kapi.url import URL

def test_url_parse():
    url_string = 'https://www.example.com:8080/path/to/resource'
    url = URL(url_string)
    assert url.host == 'www.example.com'
    assert url.port == '8080'
    assert url.path == '/path/to/resource'
    assert url.protocol == 'https'

def test_url_str():
    url_string = 'https://www.example.com:8080/path/to/resource'
    url = URL(url_string)
    assert str(url) == 'https://www.example.com:8080/path/to/resource'

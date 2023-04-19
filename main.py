from kapi.request import Request


def send(url):
    r = Request(method='GET', url=url)
    print(r.send())


if __name__ == "__main__":
    send('https://vk.com/')
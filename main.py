from kapi.request import Request


if __name__ == "__main__":
    r = Request(method='GET', url='https://vk.com/')
    response = r.send()
    print(response.content)
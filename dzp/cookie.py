import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

all_cookies = []
index = 0


def covert_cookie(cookie):
    cookie_list = cookie.split(';')
    cookies = {}
    for c in cookie_list:
        name, value = tuple(c.strip().split('='))
        cookies[name] = value

    return cookies


def get_cookies():
    global index
    if not all_cookies:
        read_cookies()

    cookie = all_cookies[index]
    index += 1
    index = index % len(all_cookies)
    return covert_cookie(cookie)


def read_cookies():
    with open(os.path.join(BASE_DIR,'cookies.txt'), 'r') as f:
        for line in f:
            all_cookies.append(line.strip())


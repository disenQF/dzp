from random import choice
import requests
from lxml import etree

proxies = [
    'http://119.101.112.48:9999',
    'https://119.101.113.177:9999',
    'https://119.101.116.254:9999',
    'https://119.101.113.91:9999',
    'http://119.101.115.176:9999',
    'http://119.101.113.174:9999'
]

http_proxies = []
https_proxies = []

def test_proxy():

    deletable_proxy_ips = []   # 无效的代理ip
    for ip_address in proxies:

        if ip_address.split(':')[0] == 'http':
            url = 'http://ip.tool.chinaz.com'
            verify(url,
                   '//dd[@class="fz24"]/text()',
                   ip_address,
                   deletable_proxy_ips, http_proxies)

        else:
            url = 'https://ip.cn'
            verify(url,
                   '//div[@class="well"]/p[1]/code/text()',
                   ip_address,
                   deletable_proxy_ips, https_proxies)

    print('无效的代理', deletable_proxy_ips)
    for ip in deletable_proxy_ips:
        proxies.remove(ip)


def verify(url, xpath_str, ip_address, deletable_proxy_ips, proxies):
    ip = ip_address.split('//')[-1]
    type = ip_address.split(':')[0]
    try:
        resp = requests.get(url, proxies={type: ip}, timeout=10)
        et = etree.HTML(resp.text)
        proxy_ip = et.xpath(xpath_str)[0]

        if ip_address.find(proxy_ip) > 0:
            print(f'--{ip_address} 验证通过--')
            proxies.append(ip_address)
        else:
            print(f'--{ip_address} 验证失败---')
            deletable_proxy_ips.append(ip_address)
    except:
        print(f'--{ip_address} 验证失败---')
        deletable_proxy_ips.append(ip_address)


def random_proxy():
    return choice(proxies)


def random_http_proxy():
    if not http_proxies:
        test_proxy()
    return choice(http_proxies)


def random_https_proxy():
    if not https_proxies:
        test_proxy()

    return choice(https_proxies)


if __name__ == '__main__':
    test_proxy()
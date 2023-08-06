from urllib.request import urlopen
from json import loads


def get_ipv4():
    url = 'https://api.ipify.org'
    try:
        adr = urlopen(url).read().decode()
        return adr
    except Exception as x:
        return '!'

import xml.etree.ElementTree as ET
from pyjma import util
import requests

def get_url(url, proxies=None):

    if proxies:
        r = requests.get(url=url, proxies=proxies, timeout=5)
    else:
        r = requests.get(url=url, timeout=5)
    r.encoding = "utf-8"
    status_code = r.status_code
    if status_code == 200:
        return r.content
    else:
        raise Exception("Can not get content from URL")


def get_xml(url, proxies=None):
    content = util.get_url(url, proxies)
    root = ET.fromstring(content)
    return root
import requests
from pyjma import earthquake
from pyjma import volcano
from pyjma import typhoon
from pyjma import heavy_rain
import re
from datetime import datetime as dt
from pyjma import util

def disaster_data(data_types = [], proxies = None):

    data = {"status": "OK", "results": []}

    if "earthquake" in data_types or "volcano" in data_types:

        namespaces = {"": 'http://www.w3.org/2005/Atom'}
        url = "http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml"

        root = util.get_xml(url, proxies)

        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
            if "earthquake" in data_types and title == "震源・震度に関する情報":
                item = earthquake.process_earthquake_data(entry, proxies)
                data["results"].append(item)

    if "typhoon" in data_types:

        url = "http://www.data.jma.go.jp/developer/xml/feed/extra.xml"
        root = util.get_xml(url, proxies)
        event_ids = []
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
            if "typhoon" in data_types and "台風解析・予報情報" in title:
                item = typhoon.process_typhoon_data(entry, proxies)
                
                if item["event_id"] not in event_ids:
                    event_ids.append(item["event_id"])
                    data["results"].append(item)

    if 'heavy_rain_alarm' in data_types:
        url = "http://www.data.jma.go.jp/developer/xml/feed/regular.xml"
        root = util.get_xml(url, proxies)
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
            if "heavy_rain_alarm" in data_types and '大雨危険度通知' in title:
                item = heavy_rain.process_heavy_rain_alarm_data(entry, proxies)
                data["results"].append(item)
                break

    return data

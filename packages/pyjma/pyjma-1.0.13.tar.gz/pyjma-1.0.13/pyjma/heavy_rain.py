import re
from datetime import datetime as dt
from pyjma import util
import types
import logging

def process_heavy_rain_alarm_data(entry, proxies = None):
    uuid = entry.find('.//{http://www.w3.org/2005/Atom}id').text
    link = entry.find(
        './/{http://www.w3.org/2005/Atom}link').attrib["href"]
    
    print(link)
    root = util.get_xml(link, proxies)

    data = {}

    for meteorological_info in root.findall(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}MeteorologicalInfo"):

        datetime_text = dt.fromisoformat(meteorological_info.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}DateTime").text)
        for item in meteorological_info.findall(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Item"):
            
            area = item.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Area")

            area_code = area.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Code").text

            if area_code not in data:
                data[area_code] = {
                    'name': area.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Name").text
                }


            # prefecture = area.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Prefecture")
            # if prefecture is None:
            #     data[area_code]['prefecture'] = prefecture.text 

            # prefecture_code = area.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}PrefectureCode").text
            # if prefecture_code is None:
            #     data[area_code]['prefecture_code'] = prefecture_code.text 

            # 'prefecture': area.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Prefecture").text,
            #     'prefecture_code': area.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}PrefectureCode").text,

            item_type = item.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Type").text
            data[area_code][item_type] = {
                'report_at' : datetime_text,
                'significancies' : {}
            }
            for significancy in item.findall(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Significancy"):
                significancy_type = significancy.attrib['type']
                data[area_code][item_type]['significancies'][significancy_type] = {
                    'name': significancy.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Name").text,
                    'code': int(significancy.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Code").text),
                    'condition': significancy.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Condition").text
                }
                
    return {'type':'heavy_rain', 'data': data}
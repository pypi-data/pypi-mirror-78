import re
from datetime import datetime as dt
from pyjma import util

def parse_typhoon_coordinate(coorstring):
    coors = re.split('(\+)|(\-)|(/)', coorstring)
    coors = [a for a in coors if a != ""]
    coors = [a for a in coors if a is not None]

    lat = float(coors[1])
    if coors[0] == "-":
        lat = 180 + lat

    lng = float(coors[3])
    if coors[2] == "-":
        lng = 180 + lng

    return lat, lng

def process_typhoon_data(entry, proxies = None):
    return_data = {"type": "typhoon"}

    return_data["uuid"] = entry.find('.//{http://www.w3.org/2005/Atom}id').text
    return_data["link"] = entry.find('.//{http://www.w3.org/2005/Atom}link').attrib["href"]

    # extract detail data
    root = util.get_xml(return_data["link"], proxies)

    # event id 
    return_data["event_id"] = root.find(".//{http://xml.kishou.go.jp/jmaxml1/informationBasis1/}EventID").text

    # typhoon name
    return_data["name"] = root.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Name").text
    # typhoon kana
    return_data["name_kana"] = root.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}NameKana").text
    # typhoon no
    return_data["number"] = root.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Number").text

    # typhoon remark
    return_data["current_remark"] = root.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Remark").text

    # reported_datetime
    return_data["report_datetime"] = dt.fromisoformat(root.find(".//{http://xml.kishou.go.jp/jmaxml1/informationBasis1/}ReportDateTime").text)

    # MeteorologicalInfos
    return_data["estimated_path"] = []
    for meteorological_info in root.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}MeteorologicalInfos"):
        data = {}
        data["datetime"] = dt.fromisoformat(meteorological_info.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}DateTime").text)

        # type
        data["type"] = meteorological_info.find(".//{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}DateTime").attrib["type"]

        # wind speed
        try:
            data["center_wind_speed_mps"] = int(meteorological_info.find(".//{http://xml.kishou.go.jp/jmaxml1/elementBasis1/}WindSpeed[@condition='中心付近'][@unit='m/s']").text)
        except:
            data["center_wind_speed_mps"] = None

        if data["type"] == "実況":
            # center of typhoon
            coordinate = meteorological_info.find(".//{http://xml.kishou.go.jp/jmaxml1/elementBasis1/}Coordinate[@type='中心位置（度）']").text
            lat, lng = parse_typhoon_coordinate(coordinate)
            data["center"] = {
                "lon": lng,
                "lat": lat
            }
            # current position
            return_data["current_center"] = data["center"]
            return_data["current_center_wind_speed_mps"] = data["center_wind_speed_mps"]
        else:
            # center of typhoon
            coordinate = meteorological_info.find(".//{http://xml.kishou.go.jp/jmaxml1/elementBasis1/}BasePoint[@type='中心位置（度）']").text
            lat, lng = parse_typhoon_coordinate(coordinate)
            data["center"] = {
                "lon": lng,
                "lat": lat
            }

        return_data["estimated_path"].append(data)

    return_data["estimated_path"] = sorted(return_data["estimated_path"], key=lambda x:x["datetime"])

    return return_data
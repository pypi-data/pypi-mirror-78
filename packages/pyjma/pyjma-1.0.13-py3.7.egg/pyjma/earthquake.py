import re
from datetime import datetime as dt
from pyjma import util

def parse_earthquake_coordinate(coorstring):
    coors = re.split('(\+)|(\-)|(/)', coorstring)
    coors = [a for a in coors if a != ""]
    coors = [a for a in coors if a is not None]

    lat = float(coors[1])
    if coors[0] == "-":
        lat = 180 + lat

    lng = float(coors[3])
    if coors[2] == "-":
        lng = 180 + lng

    try:
        depth = int(coors[5])
    except:
        depth = 0

    return lat, lng, depth


def process_earthquake_data(entry, proxies = None):
    uuid = entry.find('.//{http://www.w3.org/2005/Atom}id').text
    link = entry.find(
        './/{http://www.w3.org/2005/Atom}link').attrib["href"]
    root = util.get_xml(link, proxies)

    event_id = root.find(".//{http://xml.kishou.go.jp/jmaxml1/informationBasis1/}EventID").text

    try:
        magnitude = root.find(
            ".//{http://xml.kishou.go.jp/jmaxml1/elementBasis1/}Magnitude").text
        magnitude = float(magnitude)
    except:
        magnitude = 0.0

    coordinate = root.find(
        ".//{http://xml.kishou.go.jp/jmaxml1/elementBasis1/}Coordinate").text
    lat, lng, depth = parse_earthquake_coordinate(coordinate)

    origin_time = dt.fromisoformat(root.find(
        ".//{http://xml.kishou.go.jp/jmaxml1/body/seismology1/}OriginTime").text)

    epicenter = ""
    try:
        epicenter += root.find(".//{http://xml.kishou.go.jp/jmaxml1/body/seismology1/}Earthquake").find(
            ".//{http://xml.kishou.go.jp/jmaxml1/body/seismology1/}Name").text
    except:
        pass

    comment = ""
    try:
        comment += root.find(
            ".//{http://xml.kishou.go.jp/jmaxml1/body/seismology1/}ForecastComment/{http://xml.kishou.go.jp/jmaxml1/body/seismology1/}Text").text
    except:
        pass

    return {
        "type": "earthquake",
        "event_id": event_id,
        "uuid": uuid,
        "link": link,
        "magnitude": magnitude,
        "location": {
            "lon": lng,
            "lat": lat
        },
        "depth": depth,
        "origin_time": origin_time,
        "epicenter": epicenter,
        "comment": comment
    }

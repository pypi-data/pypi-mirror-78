import re
from datetime import datetime as dt
from pyjma import util
import xmltodict

def process_volcano_data(entry):
    uuid = entry.find('.//{http://www.w3.org/2005/Atom}id').text
    link = entry.find(
        './/{http://www.w3.org/2005/Atom}link').attrib["href"]
    xml_string = util.get_url(link)
    return xmltodict.parse(xml_string)
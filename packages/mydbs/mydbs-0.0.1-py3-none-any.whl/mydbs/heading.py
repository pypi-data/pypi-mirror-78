from configparser import ConfigParser
import xml.etree.ElementTree as Et
from functools import wraps

conf = ConfigParser()
conf.read('mydbs.ini')

xml_file = open('sql.xml')
tree = Et.parse(xml_file)
root = tree.getroot()

def error_report(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print('Error! '+str(e))
    return wrapper


import requests
from requests.exceptions import HTTPError
import copy
from models import constants

class Location:
    def __init__(self,query):
        coords = Location.getLocation(query)
        self.addr = coords[-1]
        self.lat=coords[0]
        self.lon=coords[1]
    
    def __str__(self):
        return self.addr
    

    @staticmethod
    def getLocation(place):
        url =f'{constants.tomtom_base}{place}.json?key={constants.tomtom_key}'
        res = requests.get(url)
        res_json = res.json()
        addr = res_json['results'][0]['address']['freeformAddress']
        coords = tuple([res_json['results'][0]['position']['lat'],res_json['results'][0]['position']['lon'],addr])
       
        return coords
    
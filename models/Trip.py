import requests
from requests.exceptions import HTTPError
import copy
from models.Location import Location
import random
from models import constants

class Trip:
    def __init__(self,*places):

        self.id=random.randint(0,100)
        self.places=[]
        for p in places:
            l = Location(p)
            self.places.append(l)
        if len(places) > 0:
            self.details=self.get_summary()
    
    @classmethod
    def fromPlaces(cls,id=-1,places=[]):
        temp=cls()
        if id == -1:
            temp.id=random.randint(0,100)
        temp.places=places
        #print(temp.places)
        temp.details=temp.get_summary()
        return temp
    
    
    @staticmethod
    def getDirections(origin,dest):
        
        url  = f'{constants.tomtom_route}{origin.lat},{origin.lon}:{dest.lat},{dest.lon}/json?instructionsType=text&language=en-US&key={constants.tomtom_key}'
        res = requests.get(url)
        
        res_json = res.json()
        dist= tuple([res_json['routes'][0]['summary']['lengthInMeters'],res_json['routes'][0]['summary']['travelTimeInSeconds']])
        #print(origin, dest,dist)
        return dist

    def distance(self):
        distances = []
        for i in range(len(self.places)-1):
            distances.append(Trip.getDirections(self.places[i],self.places[i+1]))
        return distances
    
    def __add__(self,other):
        
        if isinstance(other,str):
            newLoc = Location(other)  
            self.places= self.places + [newLoc]
            self.details=self.get_summary()
            return self         
            #return Trip.fromPlaces(id=self.id,places=self.places + [newLoc])
        elif isinstance(other,Trip):
            if self.places[-1].addr == other.places[0].addr:
                newplaces= self.places[:]+other.places[1:]
                #print(newplaces)
                return Trip.fromPlaces(places=newplaces)
            else:
                raise NameError('Trips cannot be combined.')

    def __mul__(self,num):
        if isinstance(num,int):
            if num == 1:
                return self

            places = self.places[:]
            places_new = places[:]
            num-=1
            for x in range(num):
                if x % 2 == 0:
                    places_new.extend(places[-2::-1])
                else:
                    places_new.extend(places[1:])
                #print('places_new',places_new)
                #print('places',places)
            self.places=places_new
            self.details=self.get_summary()
            return self  
            #return Trip.fromPlaces(id=self.id,places=places_new)

        else:
            raise NameError('Multiplier MUST be an integer')
        
    def __gt__(self,other):
        return self.distance() > other.distance()

    def __lt__(self,other):
        return self.distance() < other.distance()
    
    def __eq__(self,other):
        return self.places == other.places

    # def __str__(self):
    #     return ' '.join([l.addr for l in self.places])
    @staticmethod
    def _toMiles(m):
        return str.format("{:0.2f}",m*0.00062)

    @staticmethod    
    def _secToTime(secs):
        m = secs//60
        secs=secs%60
        h = m // 60
        m = m%60

        res=""
        if h > 0:
            res+=" "+str(h)+" hour"
        if h > 1:
            res+="s"
        
        if m > 0:
            res+=" "+str(m)+" minute"
        if m > 1:
            res+="s"
        
        if secs > 0:
            res+=" "+str(secs)+" second"
        if secs > 1:
            res+="s"
        return (res)

    @staticmethod
    def _getWeather(loc):
        url=f'{constants.weatherStack_base}?access_key={constants.weatherStack_key}&query={loc.lat},{loc.lon}&units=f'
        res = requests.get(url)
        
        res_json = res.json()
        return (res_json['current']['temperature'],res_json['current']['weather_icons'][0])


    def summary(self):
        details=self.details
        maxsrc=max([len(x['start']) for x in self.details['stops']])+5
        maxdst=max([len(x['end']) for x in self.details['stops']])+5
        maxtime=len('23 hours 59 minutes 59 seconds')+5
        print('***Your Itinerary***')
        print ()
        print(f'Here is a summary of your trip from {details["src"]} to {details["dst"]}')
        print()
        print("{:<5}{:<{maxsrc}}{:<{maxdst}}{:>20}{:>{maxtime}}".format("No.","Origin", "Destination", "Distance (miles)","Time",maxsrc=maxsrc,maxtime=maxtime,maxdst=maxdst))
        print('-'*(maxsrc+maxdst+maxtime+25))

        for stop in details['stops']:
            print("{:<5}{:<{maxsrc}}{:<{maxdst}}{:>20}{:>{maxtime}}".format(str(stop['id']),stop['start'],stop['end'], stop['dist'],stop['time'],maxsrc=maxsrc,maxtime=maxtime,maxdst=maxdst))

        print('-'*(maxsrc+maxdst+maxtime+25))
        print("{:<5}{:<{maxsrc}}{:<{maxdst}}{:>20}{:>{maxtime}}".format("","","Total ",details['totalDist'] ,details['totalTime'],maxsrc=maxsrc,maxtime=maxtime,maxdst=maxdst))
        print('-'*(maxsrc+maxdst+maxtime+25))
        print()
        temp = details['dstWeather']
        print()
        print(f'It is currently {temp} degrees in {details["dst"]}. Have a safe trip! ')

    def get_summary(self):
        distances = self.distance()
        total_dist = 0
        total_time = 0
        summary = {}
        summary['id'] = self.id
        summary['src'] = str(self.places[0])
        summary['dst'] = str(self.places[-1])
        summary['stops'] = []
        for idx, d in enumerate(distances):
            total_dist += d[0]
            total_time += d[1]
            stop = {}
            stop['id'] = idx + 1
            stop['start'] = str(self.places[idx])
            stop['end'] = str(self.places[idx + 1])
            stop['dist'] = Trip._toMiles(d[0])
            stop['time'] = Trip._secToTime(d[1])
            summary['stops'].append(stop)
        summary['totalDist'] = Trip._toMiles(total_dist)
        summary['totalTime'] = Trip._secToTime(total_time)
        weatherDetails = Trip._getWeather(self.places[-1])
        summary['dstWeather'] = weatherDetails[0]
        summary['weatherIcon'] = weatherDetails[1]
        trip = {
            'id': self.id,
            'places': self.places,
            'details': summary
        }
        return trip

    # Needed to modify this method since the trips_new.dat file has Locations object as well.
    # Therefore commenting the original method and modified version is above.
    # def get_summary(self):
    #     distances=self.distance()
    #     total_dist=0
    #     total_time=0
    #     summary={}
    #     summary['id']=self.id
    #     summary['src']=str(self.places[0])
    #     summary['dst']=str(self.places[-1])
    #     summary['stops']=[]
    #     for idx,d in enumerate(distances):
    #         total_dist+=d[0]
    #         total_time+=d[1]
    #         stop={}
    #         stop['id']=idx+1
    #         stop['start']=str(self.places[idx])
    #         stop['end']=str(self.places[idx+1])
    #         stop['dist']=Trip._toMiles(d[0])
    #         stop['time']=Trip._secToTime(d[1])
    #         summary['stops'].append(stop)
    #     summary['totalDist']=Trip._toMiles(total_dist)
    #     summary['totalTime']=Trip._secToTime(total_time)
    #     weatherDetails = Trip._getWeather(self.places[-1])
    #     summary['dstWeather']= weatherDetails[0]
    #     summary['weatherIcon']= weatherDetails[1]
    #     return summary
    
    def __str__(self):
        return f'ID:{self.id} Src: {self.places[0]} Dest: {self.places[-1]}'


if __name__ == '__main__':
    t1 = Trip('New York NY', 'Boston MA', 'Washington DC', 'Arlington VA')
    # t1 = ID:56 Src: New York, NY Dest: Saginaw, MI
    print(t1)
    # print(t1.places)
    # print(t1.get_summary())
    # t2 = t1 + 'Saginaw MI'
    # print(t2)
    # print(t2.places)
    # print(t2.get_summary())
    print('Trip Details::::::::::::::::\n', t1.details)
    # print(t2)
    # t2 = t2 + 'Bay City MI'
    # print(t2)
    # print(t2.get_summary())

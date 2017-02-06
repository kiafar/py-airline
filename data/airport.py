#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
airport module extracts and represents airports data.
@since:12/04/2016
@author:Tirdad Kiafar
"""
from data.fileIO import IO


###############################################################################
class Airport():
    '''Holds data of an airport.'''

    def __init__(self):
        '''Holds data of an airport.'''
        self._country = ''  # country name
        self._iata_code = ''  # iata code
        self._icao_code = ''  # icao code
        self._name = ''  # name
        self._latitude = 0  # latitude
        self._longitude = 0  # longitude
        self._elevation = 0  # elevation
        self._tz_code = 0  # timezone code like Asia/Kabul
        self._tz_name = 0  # timezone name like Afghanistan Time
        self._continent = 0  # continent
        self._iso_country = 0  # iso country code like IE
        self._iso_region = 0  # region code like IE-C
        self._municipality = ''  # municipality
        self._type = ''  # airport type like large_airport, medium_airport
        self._scheduled_service = ''  # scheduled services, yes or no

    def __str__(self):
        return "{'Country':" + "'" + self._country + "'" + \
                ", 'IataCode':" + "'" + self._iata_code + "'" + \
                ", 'IcaoCode':" + "'" + self._icao_code + "'" + \
                ", 'Name':" + "'" + self._name + "'" + \
                ", 'Latitude':" + str(self._latitude) + \
                ", 'Longitude':" + str(self._longitude) + \
                ", 'TimeZoneCode':" + "'"+self._tz_code + "'" + "}"

    @property
    def country(self):
        return self._country

    @property
    def iata_code(self):
        return self._iata_code

    @property
    def icao_code(self):
        return self._icao_code

    @property
    def name(self):
        return self._name

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def elevation(self):
        return self._elevation

    @property
    def tz_code(self):
        return self._tz_code

    @property
    def tz_name(self):
        return self._tz_name

    @property
    def continent(self):
        return self._continent

    @property
    def iso_country(self):
        return self._iso_country

    @property
    def iso_region(self):
        return self._iso_region

    @property
    def municipality(self):
        return self._municipality

    @property
    def type(self):
        return self._type

    @property
    def scheduled_service(self):
        return self._scheduled_service

    def __eq__(self, other):
        '''Override the default Equals behavior'''
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)


###############################################################################
class AirportAtlas(dict):
    '''Holds airports data. uses 3 letter iata code as identifier.
    Could be used in two ways: airports['code'] or airports('code')'''

    def __init__(self, dataFile):
        '''Constructor

        Args:
            dataFile (str): path to airports csv file.'''
        self.__names = []
        self.__codes = []
        self.__extract_airports(dataFile)

    def __extract_airports(self, dataFile):
        '''This function receives the file path of data and sets the objects.

        Args:
            dataFile (str): path to aircraft data csv file.'''
        # using IO class for consistency
        io = IO(dataFile)
        reader = io.get_csv_dict()
        for row in reader:
            airp = Airport()
            airp._country = row['country']
            airp._iata_code = row['iataCode']
            airp._icao_code = row['icaoCode']
            airp._name = row['name']
            airp._latitude = float(row['latitudeDegree'])
            airp._longitude = float(row['longitudeDegree'])
            try:  # some records dont have value
                airp._elevation = float(row['elevationFeet'])
            except ValueError:
                airp._elevation = 0
            airp._tz_code = row['timeZoneCode']
            airp._tz_name = row['timeZoneName']
            airp._continent = row['continent']
            airp._iso_country = row['isoCountry']
            airp._iso_region = row['isoRegion']
            airp._municipality = row['municipality']
            airp._type = row['type']
            airp._scheduled_service = row['scheduledService']
            self[airp.iata_code] = airp
            self.__names.append(airp.name)
            self.__codes.append(airp.iata_code)

    @property
    def names(self) -> list:
        '''Returns the list of airport names'''
        return self.__names

    @property
    def codes(self) -> list:
        '''Returns the list of airport codes'''
        return self.__codes

    def find_closest(self, lat, lon) -> Airport:
        '''Finds the closest airport to a given position.

        Args:
            lat (float): latitude of target.
            lon (float): longitude of target
        Returns:
            Airport: airport object'''
        control_dist = 24000
        res = None
        for code, airp in self.items():
            tmp = abs(airp.latitude - lat) + abs(airp.longitude - lon)
            if tmp < control_dist:
                control_dist = tmp
                res = airp
        return res

    def get_by_name(self, name) -> Airport:
        '''Finds and returns an airport by name.
        
        Args:
            name (str): name of airport.
        Returns:
            Airport: Airport object.'''
        for code, airport in self.items():
            if airport.name.lower() == name.lower():
                return airport

    def __call__(self, iataCode) -> Airport:
        '''Returns the Airport object of the given code.

        Args:
            iataCode (str): 3 letter iata aiport code, e.g. DUB'''
        iataCode = iataCode.upper()
        if iataCode not in self.keys():  # verify iataCode
            raise KeyError("IATA Code: '{}' unknown".format(iataCode))
        return self[iataCode]


###############################################################################
def test():
    airp = AirportAtlas('airports.csv')
    while True:
        code = input('Enter 3 letter IATA code: ').upper()
        if code not in airp.keys():
            print(code+' Not in database..')
            continue
        print('Country: {}'.format(airp(code).country))
        print('Airport Name: {}'.format(airp(code).name))
        print('Airport Latitude: {} deg'.format(airp(code).latitude))
        print('Airport Longitude: {} deg'.format(airp(code).longitude))
        print('Airport City: {}'.format(airp(code).municipality))


if __name__ == '__main__':
    test()

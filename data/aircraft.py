#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
aircraft module extracts and represents aircraft data.
@since:12/04/2016
@author:Tirdad Kiafar
"""
import csv
from data.fileIO import IO

UNIT_IMPERIAL = 'imperial'
UNIT_METRIC = 'metric'
MIL_TO_KM = 1.60934
GAL_TO_LIT = 3.78541


###############################################################################
class Aircraft():
    '''Holds data of an airplane. note that all atributes are read only.'''
    def __init__(self):
        '''Holds data of an aircraft.'''
        self._code = ''  # aircraft code
        self._eng_type = ''  # aircraft type
        self._units = ''  # unit types, associated with measures like range
        self._manufacturer = ''  # manufacturer company
        self._max_range = 0  # flying range
        self._fuel_capacity = 0  # maximum fuel capacity of aircraft, liters
        self._consumption_rate = 0  # fuel consumption, liter/km

    @property
    def code(self):
        return self._code

    @property
    def eng_type(self):
        return self._eng_type

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if self._units != '':  # make this read only after first time
            raise AttributeError("can't set attribute")
        if units not in [UNIT_IMPERIAL, UNIT_METRIC]:
            raise ValueError("units has to be either 'imperial' or 'metric'")
        self._units = units

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def max_range(self, unit='metric'):
        res = 0
        if unit == UNIT_METRIC:
            if self._units == UNIT_METRIC:
                res = self._max_range
            else:  # unit is imperial, convert
                res = self._max_range * MIL_TO_KM
        elif unit == UNIT_IMPERIAL:
            if self._units == UNIT_IMPERIAL:
                res = self._max_range
            else:  # unit is metric, convert
                res = int(self._max_range / MIL_TO_KM)
        return res

    @property
    def fuel_capacity(self, unit='metric'):
        res = 0
        if unit == UNIT_METRIC:
            if self._units == UNIT_METRIC:
                res = self._fuel_capacity
            else:  # unit is imperial, convert
                res = self._fuel_capacity * GAL_TO_LIT
        elif unit == UNIT_IMPERIAL:
            if self._units == UNIT_IMPERIAL:
                res = self._fuel_capacity
            else:  # unit is metric, convert
                res = int(self._fuel_capacity / GAL_TO_LIT)
        return res

    @property
    def consumption_rate(self):
        return self._consumption_rate

    def __str__(self):
        '''A string representing the aircraf which is manufacturer + code.
        e.g. Airbus A380'''
        return self._manufacturer + ' ' + self._code


###############################################################################
class Aircrafts(dict):
    '''Holds aircrafts data. Could be used in two ways: aircraft['code'] or
    aircraft('code').'''

    def __init__(self, dataFile):
        '''Constructor

        Args:
            dataFile (str): path to aircraft data csv file.'''
        self.__names = []
        self.__codes = []
        self.__extract_aircrafts(dataFile)

    def __extract_aircrafts(self, dataFile):
        '''This function receives the file path of data and sets the objects.

        Args:
            dataFile (str): path to aircraft data csv file.'''
        # using IO class for consistency
        io = IO(dataFile)
        reader = io.get_csv_dict()
        for row in reader:
            plane = Aircraft()
            plane._code = row['code']
            plane._eng_type = row['type']
            # this one has a one time setter to validate the code
            plane.units = row['units']
            plane._manufacturer = row['manufacturer']
            plane._max_range = float(row['range'])
            plane._fuel_capacity = float(row['capacity'])
            plane._consumption_rate = plane.fuel_capacity/plane.max_range
            self[plane.code] = plane
            self.__names.append(str(plane))
            self.__codes.append(plane.code)

    @property
    def names(self):
        '''Returns a list of string representation of planes'''
        return self.__names

    @property
    def codes(self):
        '''Returns a list of plane codes'''
        return self.__codes

    def get_by_str(self, string) -> Aircraft:
        '''Gets a string representation of an aircraft and returns aircraft'''
        # extract the aircraft code
        code = string.split()[-1].strip().upper()
        aircraft = self.get(code)
        if aircraft is None:
            return
        return aircraft

    def __call__(self, planeCode) -> Aircraft:
        '''Returns the Aircraft object of the given code.

        Args:
            planeCode (str): plane code. e.g. 737'''
        if planeCode not in self.keys():  # verify planeCode
            raise KeyError("Plane code: '{}' unknown".format(planeCode))
        return self[planeCode]


###############################################################################
def test():
    aircraft = Aircrafts('aircrafts.csv')
    print('Aircraft: {}'.format(str(aircraft('767'))))
    print('Type: {}'.format(aircraft('737').eng_type))
    print('Flying Range: {}'.format(aircraft('737').max_range))
    print('Fuel Capacity: {} liters'.format(aircraft('737').fuel_capacity))
    print('Fuel Consumption: {} l/km'.format(aircraft('737').consumption_rate))


if __name__ == '__main__':
    test()

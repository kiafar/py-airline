#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fuel module extracts and represents fuel data.
@since:12/04/2016
@author:Tirdad Kiafar
"""
from data.fileIO import IO
UNIT = 'EURO/LITTER'
UNIT_SHORT = 'eu/lit'


###############################################################################
class FuelObj:
    def __init__(self):
        '''Holds data of an individual fuel item.'''
        self._country = ''
        self._iso_country = ''
        self._price = 0
        self._unit = UNIT
        self._unit_short = UNIT_SHORT

    @property
    def country(self):
        return self._country

    @property
    def iso_country(self):
        return self._iso_country

    @property
    def price(self):
        return self._price

    @property
    def unit(self):
        return self._unit

    @property
    def unit_short(self):
        return self._unit_short


###############################################################################
class FuelMap(dict):
    '''Holds aircrafts data. Could be used in two ways: aircraft['code'] or
    aircraft('code').'''

    def __init__(self, dataFile):
        '''Constructor

        Args:
            dataFile (str): path to aircraft data csv file.'''
        self.__extract_fuels(dataFile)

    def __extract_fuels(self, dataFile):
        '''This function receives the file path of data and sets the objects.

        Args:
            dataFile (str): path to aircraft data csv file.'''
        io = IO(dataFile)
        reader = io.get_csv_dict()
        for row in reader:
            fuel = FuelObj()
            fuel._country = row['country']
            fuel._iso_country = row['iso_country']
            fuel._price = float(row['price_eur_lit'])
            self[fuel.iso_country] = fuel

    def __call__(self, iso_country) -> FuelObj:
        '''Returns the fuel object with the given country iso code.

        Args:
            iso_country (str): iso 2 letter country code.e.g. IE,US
        Returns:
            FuelObj: related fuel object.'''
        if iso_country not in self.keys():  # verify country code
            raise KeyError("Country code: '{}' unknown".format(iso_country))
        return self[iso_country]


###############################################################################
def test():
    fm = FuelMap('fuelprice.csv')
    print('Country: {}'.format(fm('IE').country))
    print('Iso Country Code: {}'.format(fm('IE').iso_country))
    print('Fuel Price: {}'.format(fm('IE').price))

if __name__ == '__main__':
    test()

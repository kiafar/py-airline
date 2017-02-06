#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
currency module extracts and represents currencies data.
@since:12/04/2016
@author:Tirdad Kiafar
"""
import csv


###############################################################################
class Currency():
    '''Holds data of an currency.'''

    def __init__(self):
        '''Holds data of an aircraft.'''
        self._country = ''  # country name
        self._iso_country = ''  # iso 2 letter country code
        self._code = ''  # iso 3 letter currency code
        self._name = ''  # currency name
        self._euro_to = 0  # 1 unit of this currency costs this much euro
        self._euro_from = 0  # 1 euro costs this much of this currency

    @property
    def country(self):
        return self._country

    @property
    def iso_country(self):
        return self._iso_country

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        if self._code != '':  # make this read only after first time
            raise AttributeError("can't set attribute")
        if len(code) != 3:
            raise ValueError('Currency code is 3 letters')
        self._code = code

    @property
    def name(self):
        return self._name

    @property
    def euro_to(self):
        '''1 unit of this currency costs this much euro'''
        return self._euro_to

    @property
    def euro_from(self):
        '''1 euro costs this much of this currency'''
        return self._euro_from

    def convert_to_euro(self, value) -> float:
        '''This function converts the given amount in current currency to euro
        and will return a float of the converted amount
        
        Args:
            value (float): the amount of money to be converted to euro'''
        return value * self._euro_to

    def convert_from_euro(self, value) -> float:
        '''This function converts the given amount in euro to current currency
        and will return a float of the converted amount
        
        Args:
            value (float): the amount of money to be converted to currency'''
        return value * self._euro_from


###############################################################################
class Currencies(dict):
    '''Holds currencies data. uses 2 letter country iso code as identifier. 
    Could be used in two ways: currencies['code'] or currencies('code')'''

    def __init__(self, dataFile):
        '''Constructor

        Args:
            dataFile (str): path to currency csv file.'''
        self.__extract_currencies(dataFile)

    def __extract_currencies(self, dataFile):
        '''This function receives the file path of data and sets the objects.

        Args:
            dataFile (str): path to aircraft data csv file.'''
        with open(dataFile, 'r') as data:  # open file as data
            reader = csv.DictReader(data)  # read and store the data by header
            for row in reader:
                curr = Currency()
                curr.code = row['AlphabeticCode']
                curr._country = row['Country']
                curr._iso_country = row['isoCountry']
                curr._name = row['Currency']
                curr._euro_to = float(row['AgainstEuro'])
                curr._euro_from = float(row['EuroAgains'])
                self[curr.iso_country] = curr

    def __call__(self, isoCountry) -> Currency:
        '''Returns the Aircraft object of the given code.

        Args:
            isoCountry (str): Two letter country code, e.g. IE for Ireland'''
        if isoCountry not in self.keys():  # verify planeCode
            raise KeyError("Country code: '{}' unknown".format(isoCountry))
        return self[isoCountry]


###############################################################################
def test():
    curr = Currencies('curr.csv')
    print('Country: {}'.format(curr('US').country))
    print('ISO Currency Code: {}'.format(curr('US').code))
    print('Currency Name: {}'.format(curr('US').name))
    print('Value Against Euro: {} EUR'.format(curr('US').euro_to))
    print('Euro Value Againt {}: {} {}'.format(
        curr('US').name, curr('US').euro_from, curr('US').code))


if __name__ == '__main__':
    test()

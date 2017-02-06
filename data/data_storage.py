#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This module handles data storage. Reads/Writes data to data file.
'''
from data.fileIO import IO
import csv
import copy
# data headers, every new field must have these keys
HEADERS = ('mode',
           'airports',
           'travel_week',
           'aircraft',
           'shortest_route',
           'shortest_dist',
           'eco_route',
           'eco_route_cost')


###############################################################################
class DataStore(dict):
    '''This class reads and writes data to a data file'''
    def __init__(self, file_path):
        '''Constructor.

        Args:
            file_path (str): Path to data file.'''
        self._file_path = file_path
        self._io = IO(file_path)
        self.__read_data()

    def __read_data(self):
        '''Read data and sets self dictionary with travel weak'''
        reader = self._io.get_csv_dict()
        for row in reader:
            mode = row['mode']
            airports = row['airports']
            airports = airports.upper().split()
            travel_week = row['travel_week']
            aircraft = row['aircraft']
            shortest_route = row['shortest_route']
            shortest_dist = row['shortest_dist']
            eco_route = row['eco_route']
            eco_route_cost = row['eco_route_cost']
            self[travel_week] = {'mode': mode,
                                 'airports': airports,
                                 'travel_week': travel_week,
                                 'aircraft': aircraft,
                                 'shortest_route': shortest_route,
                                 'shortest_dist': shortest_dist,
                                 'eco_route': eco_route,
                                 'eco_route_cost': eco_route_cost}

    def add(self, data):
        '''Checks validity of data and adds data to current data.
        Note that if data already exists the record will be ignored.

        Args:
            data (dict): New data dict.'''
        # check if data exists quit function
        if data['travel_week'] in self.keys():
            return
        # check validity of data
        for key, value in data.items():
            if key not in HEADERS:
                raise KeyError('{} is not a valid header.'.format(key))
        if len(data) != len(HEADERS):
            raise Exception('Lenght of data does not match the headers')
        # update dict
        self[data['travel_week']] = data

    def save(self):
        '''Dumps the data to the data file.'''
        with open(self._file_path, 'w',
                  encoding='utf-8',
                  errors='ignore') as data:
            writer = csv.DictWriter(data,
                                    fieldnames=HEADERS,
                                    lineterminator='\n')
            writer.writeheader()
            # we make a copy to prevent modification of data on original obj
            dupl = copy.deepcopy(self)
            for key, value in dupl.items():
                # watch for writing string because reader deals with str
                if type(value['airports']) == list:
                    value['airports'] = ' '.join(value['airports'])
                writer.writerow(value)

    def map_data(self, data) -> dict:
        '''Maps an iterable to a dict with proper keys.

        Args:
            data (list): list of data, lenght must match headers.
        Returns:
            dict: mapped data.
        '''
        if len(data) != len(HEADERS):
            raise Exception('Lenght of data does not match the headers')
        res = {}
        for i in range(len(HEADERS)):
            res[HEADERS[i]] = data[i]
        return res

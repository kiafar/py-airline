#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base file IO module that wraps basic file handling methods.
@since:30/04/2016
@author:Tirdad Kiafar
"""
import os
import csv


class IO:
    '''Base class for file handling. Wraps basic file handling methods'''
    def __init__(self, file_path):
        '''Constructor

        Args:
            file_path (str): Path to file. Empty list if file not found'''
        if IO.exists(file_path) is not True:
            raise FileNotFoundError('file:'+file_path+' missing.')
        self._file_path = file_path

    def exists(file_path):
        '''A static method that checks file availability.

        Args:
            file_path (str): path to file.'''
        if os.path.exists(file_path):
            return True
        else:
            return False

    def get_csv_dict(self):
        '''Reads the csv file and returns the associated dictionary

        Returns:
            list: List of rows in csv file. rows are of type dict.'''
        with open(self._file_path, 'r',
                  encoding='utf-8',
                  errors='ignore') as data:
            reader = csv.DictReader(data)
            return list(reader)

    def get_csv(self):
        '''Reads the csv file and returns the associated dictionary

        Returns:
            list: List of rows in csv file.'''
        with open(self._file_path, 'r',
                  encoding='utf-8',
                  errors='ignore') as data:
            reader = csv.reader(data)
            return list(reader)


def test():
    io = IO(r'./aircrafts.csv')
    print(io.get_csv())

if __name__ == '__main__':
    test()

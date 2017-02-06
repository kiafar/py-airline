# -*- coding: utf-8 -*-
'''
Basic unittest for fuel management app.
@since:04/05/2016
@author:Tirdad Kiafar
'''
import unittest
from data.airport import AirportAtlas
from data.aircraft import Aircrafts
from data.fuelprice import FuelMap
from data.router import Route, ComplexRoute, ROUTE_DYNAMIC
AIRPORT_PATH = r'./data/airports.csv'
AIRCRAFT_PATH = r'./data/aircrafts.csv'
FUEL_PATH = r'./data/fuelprice.csv'


class BasicTestSuite(unittest.TestCase):
    """Basic test cases. Tests critical components like routing unit."""
    def setUp(self):
        '''Setting up needed classes'''
        self.airportAtlas = AirportAtlas(AIRPORT_PATH)
        self.aircrafts = Aircrafts(AIRCRAFT_PATH)
        self.fuelMap = FuelMap(FUEL_PATH)


class TestComponents(BasicTestSuite):
    '''Testing critical components.
    Aircrafts, FuelMap, AirportAtlas & ComplexRoute.'''
    def testAirports(self):
        dub = self.airportAtlas('DUB')
        self.assertEqual(round(dub.latitude, 2), 53.42,
                         'Wrong Airport Latitude')
        self.assertEqual(round(dub.longitude, 2), -6.27,
                         'Wrong Airport Longitude')

    def testAircraft(self):
        b757 = self.aircrafts('757-200')
        self.assertEqual(int(b757.fuel_capacity), 43403,
                         'Wrong Aircraft Fuel Capacity')

    def testFuelPrice(self):
        us = self.fuelMap('US')
        self.assertEqual(us.price, 0.2487,
                         'Wrong Fuel Price')

    def testRoute(self):
        self.route = ComplexRoute((self.airportAtlas('DUB'),
                                   self.airportAtlas('JFK'),
                                   self.airportAtlas('CCS'),
                                   self.airportAtlas('IKA'),
                                   self.airportAtlas('SYD')),
                                  self.aircrafts('757-200'),
                                  self.fuelMap,
                                  ROUTE_DYNAMIC)
        dub = (self.airportAtlas('DUB').latitude,
               self.airportAtlas('DUB').longitude)
        jfk = (self.airportAtlas('JFK').latitude,
               self.airportAtlas('JFK').longitude)
        self.assertEqual(int(Route.calcDistance(dub, jfk)), 5103,
                         'Wrong Distance Calculations')
        self.assertEqual(self.route.eco_route_cost, -1,
                         'Wrong Cost Calculations')

if __name__ == '__main__':
    unittest.main()

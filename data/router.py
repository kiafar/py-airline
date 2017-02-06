#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This module handles routing. Pairs of locations are passed through route class
constructor and optimal route is calculated by brute force method
'''
from math import pi, acos, sin, cos
from types import GeneratorType
from data.currency import Currencies
from data.airport import Airport, AirportAtlas
from data.aircraft import Aircraft, Aircrafts
from data.fuelprice import FuelObj, FuelMap
EARTH_RADIUS = 6371
ROUTE_STATIC = 'static'
ROUTE_DYNAMIC = 'dynamic'


###############################################################################
class Route:
    '''This class accepts iterables with lenght of two as points and claculates
    the optimum closed route.'''
    def __init__(self, points, closed=True, mode='dynamic'):
        '''Constructor. Pass points to the class using points argument.
        Args:
            points (tuple): an iterable with iterables of lenght two inside,
                presenting latitude and longitude. If the route is open
                point one will be the starting location
            closed (Optional[bool]): True if routing is ended at home, False if
                the route is open
            mode (str): "static" or "dynamic" routing, static has no analysis.
            '''
        # making sure points are valid
        self._points = self.__verifyPoints(points)
        # is routing closed?
        self._closed = closed
        # make a list of integers representing points for routing
        self._indexes = tuple(i for i in range(len(points)))
        # mode, static or dynamic, static is a straight path with no analysis
        self._mode = mode
        if self._mode == ROUTE_DYNAMIC:
            # distance matrix is a helper for calculating distances once
            self._distance_matrix = self.__createDistMatrix()
            # store normal routing combinations in memory, a routing sample is
            # (0,1,2,3,4,5,0) for a closed route
            self._normal_routes = Route.permutations(list(self._indexes[1:]))
            # self._normal_routes are generators, turn them to list
            self._normal_routes = list(self._normal_routes)
            # add home node (0) to the permutations
            self._normal_routes = self.__addHome(self._normal_routes)
            # finding special routes for return trips.
            self._special_routes = Route.specialPerms(list(self._indexes[1:]))
            # remove adjacent equal elements, e.g. (1,1,2,3,4,5)
            self._special_routes = Route.removeAdjacent(self._special_routes)
            # add home node (0) to the permutations
            self._special_routes = self.__addHome(self._special_routes)
            # comibning all the routes in one place
            self._possible_routes = self._normal_routes + self._special_routes
        elif self._mode == ROUTE_STATIC:
            # there is only one route possible
            self._normal_routes = [i for i in range(len(self._points))]
            self._distance_matrix = []
            if closed is True:
                self._normal_routes += [0]
            self._normal_routes = [self._normal_routes]
            self._special_routes = []
            self._possible_routes = self._normal_routes
        # calculate route distances and store them
        self._route_distances = self.__calcDistances()
        # find the shortest path
        self._opt_route_distance = min(self._route_distances)
        # store the index of that for locating the optimum route
        opt_idx = self._route_distances.index(self._opt_route_distance)
        # locate the optimum route
        self._opt_route = self._possible_routes[opt_idx]

    @property
    def points(self) -> tuple:
        return self._points

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def distance_matrix(self) -> tuple:
        return self._distance_matrix

    @property
    def indexes(self) -> tuple:
        return self._indexes

    @property
    def possible_routes(self) -> tuple:
        return self._possible_routes

    @property
    def route_distances(self) -> tuple:
        return self._route_distances

    @property
    def opt_route(self) -> tuple:
        return self._opt_route

    @property
    def opt_route_distance(self) -> float:
        return self._opt_route_distance

    def __len__(self):
        return len(self._points)

    def __verifyPoints(self, points) -> tuple:
        '''Verifies the points and check their lenght

        Args:
            points (tuple[float]): an iterable of lenght two, first element is
            latitude and the second one is longitude. e.g. (13.12, 130.15)
        '''
        res = []
        for pt in points:
            if len(pt) == 2:
                res.append(pt)
            else:
                raise ValueError('Lenght of '+str(pt)+' Should be Two.')
        return tuple(res)

    def __createDistMatrix(self) -> list:
        '''Creates distance matrix for points.

        Returns:
            List: A len(points)xlen(points) matrix of distances'''
        pts = self._points
        # setting up a 2D array with proper lenght for results
        res = [[0 for x in range(len(pts))] for x in range(len(pts))]
        for i in range(len(self._points)):
            for j in range(len(self._points)):
                res[i][j] = Route.calcDistance(pts[i], pts[j])
        return res

    def map_points(self, points) -> list:
        '''Maps a list of point indexes to existing points.

        Args:
            points (list): list of indexes.
        Returns:
            list: A list of tuples (points)'''
        res = []
        for pt in points:
            res.append(self._points[int(pt)])
        return res

    @staticmethod
    def permutations(lst) -> GeneratorType:
        '''
        Returns all possible (open) permutations for routing recursively.
        If the route is closed the last point will be the first point.

        Args:
            lst (list): A list of items

        Returns:
            list: possible permutations of the given list
        '''
        if len(lst) <= 1:
            # end of the line, no remaining permutation
            yield lst
        else:
            for (idx, first_elem) in enumerate(lst):
                # get the other elements
                the_rest = lst[:idx]+lst[idx+1:]
                # build up the permutations recursively
                for perm in Route.permutations(the_rest):
                    yield [first_elem]+perm

    @staticmethod
    def specialPerms(lst) -> list:
        '''
        Returns all possible (open) permutations including return trips.

        Args:
            lst (list): A list of items

        Returns:
            list: possible permutations of the given list
        '''
        res = []
        current = []
        # to duplicate every node
        for i in range(len(lst)):
            # get permutations and turn generator type to list
            current = list(Route.permutations([lst[i]]+lst))
            res += current
        return res

    @staticmethod
    def removeAdjacent(lst) -> list:
        '''Removes lists with adjacent equal elements'''
        res = []
        for i in lst:
            duplicate = False
            for idx, elem in enumerate(i):
                if idx != len(i)-1 and elem == i[idx+1]:
                    duplicate = True
                    break
            if duplicate is False:
                res.append(i)
        return res

    def __addHome(self, array) -> list:
        '''Adds first point to all permutations'''
        for i in range(len(array)):
            # add node 0 to the beggining of route
            array[i].insert(0, 0)
            # add node 0 to the end of route if route is closed
            if self._closed is True:
                array[i] += [0]
        return array

    @staticmethod
    def calcDistance(point1, point2) -> float:
        '''This static function returns the distance between two points in
        kilometers p1 and p2 are two tuples or lists containing latitude and
        longitude of start and destination points in order.

        Args:
            point1 (tuple[float]): tuple of lenght two with lat, lon inside
            point2 (tuple[float]): tuple of lenght two with lat, lon inside'''
        # check validity of points
        if len(point1) != 2 or len(point2) != 2:
            raise ValueError('Lenght of points must be 2.')
        phi1, phi2 = 2*pi/360*(90-point1[0]), 2*pi/360*(90-point2[0])
        theta1, theta2 = 2*pi/360*(point1[1]), 2*pi/360*(point2[1])
        exp1 = sin(phi1)*sin(phi2)*cos(theta1-theta2)
        exp2 = cos(phi1)*cos(phi2)
        # acos accepts values -1<= <=1, in some cases because of pythons
        # inaccurate floats the results could be like -1.00000000000001,
        # to fix this we round it to 12 decimal places
        exp3 = round(exp1+exp2, 12)
        return acos(exp3)*EARTH_RADIUS

    def __calcDistances(self) -> list:
        '''Calculates distances for all routes and returns a list of floats.'''
        res = []
        for i in self._possible_routes:
            dst = 0
            for j in range(len(i)-1):
                pt1 = self._points[i[j]]
                pt2 = self._points[i[j+1]]
                dst += Route.calcDistance(pt1, pt2)
            res.append(dst)
        return res


###############################################################################
class ComplexRoute(Route):
    '''Adds functionality of economic calculations to the route class'''

    def __init__(self, airports, aircraft, fuelmap, mode):
        '''Constructor'''
        super().__init__(self.__calc_points(airports), True, mode)
        self.__airports = airports  # needed for calculating economic route
        self.__aircraft = aircraft  # needed for calculating economic route
        self.__fuelmap = fuelmap  # needed for calculating economic route
        # calculate route costs, cheapest route and its details
        self._route_costs = []
        a, b, c, d = self.__calcRouteCosts()
        self._route_costs = a
        self._cost_details = b
        self._eco_route_cost = c
        self._eco_route_details = d
        # store the index of cheapest cost for locating cheapest pat
        if self._eco_route_cost > -1:  # if no valid route is present it is -1
            eco_idx = self._route_costs.index(min(self._route_costs))
            # locate cheapest path
            self._eco_route = self._possible_routes[eco_idx]
        else:  # all routes are invalid
            self._eco_route = []

    @property
    def airports(self):
        return self.__airports

    @property
    def aircraft(self):
        return self.__aircraft

    @property
    def route_costs(self) -> list:
        '''Return costs of the routes'''
        return self._route_costs

    @property
    def eco_details(self) -> list:
        '''Return cost details of routes'''
        return self._cost_details

    @property
    def eco_route(self) -> tuple:
        return self._eco_route

    @property
    def eco_route_cost(self) -> float:
        return self._eco_route_cost

    @property
    def eco_route_details(self) -> float:
        return self._eco_route_details

    def __calc_points(self, airports) -> list:
        res = []
        for i in airports:
            res.append((i.latitude, i.longitude))
        return res

    def __calcRouteCosts(self) -> tuple:
        routeCosts = []  # this will hold the cost of routes
        min_cost = -1  # to get cheapest route
        min_cost_details = []  # to get further details on eco route
        cost_details = []  # to get further details on route costs
        for i in range(len(self._possible_routes)):
            rt = self._possible_routes[i]
            cost = 0
            path_details = []  # temp path details holder
            # iterate through nodes of a route
            for j in range(len(rt)-1):
                p1, p2 = rt[j], rt[j+1]
                # get airports of pointsW
                a1, a2 = self.__airports[p1], self.__airports[p2]
                # get point lat, long
                p1, p2 = self._points[p1], self._points[p2]
                # aircraft fuels up to max at home
                if j == 0:
                    cost += self.__fuelmap(a1.iso_country).price * \
                        self.__aircraft.fuel_capacity
                # calculate distance of two airports
                dist = Route.calcDistance(p1, p2)
                # check if dist is not longer than aircraft range
                if dist > self.__aircraft.max_range:
                    cost = 0
                    path_details = [0]
                    break
                # calculate fuel consumption in litter
                fuel_consumed = self.__aircraft.consumption_rate * dist
                # get the fuel price of destination
                fuelPrice = self.__fuelmap(a2.iso_country).price
                # add detail of this path to details list
                path_details.append(fuel_consumed * fuelPrice)
                # add the price of this path to the whole price
                cost += fuel_consumed * fuelPrice
            # if path was not invalid subtract the remaining fuel cost
            if cost > 0:
                remainin_fuel = self.__aircraft.fuel_capacity - fuel_consumed
                # a2 is last (home country), remember we can disable it from
                # preferences so it is wise to use generic, not Ireland
                remaining_price = remainin_fuel * \
                    self.__fuelmap(a2.iso_country).price
                cost -= remaining_price
            # add cost to the list, if route is out of range 0 is added
            routeCosts.append(cost)
            # add path details to list, if route is invalid it
            # has 1 child which is 0
            cost_details.append(path_details)
            # check for minimum cost
            if min_cost == -1 and cost > 0:
                min_cost = cost
                min_cost_details = path_details
            elif cost > 0:
                if cost < min_cost:
                    # store the data
                    min_cost = cost
                    min_cost_details = path_details
        return routeCosts, cost_details, min_cost, min_cost_details


###############################################################################
def test():
    '''Test for Route class'''
    acd = Aircrafts('aircrafts.csv')  # Aircraft data
    apd = AirportAtlas('airports.csv')  # AirportAtlas data
    cud = Currencies('curr.csv')  # Currencies data
    ful = FuelMap('fuelprice.csv')  # Fuel prices
    airports = (apd('DUB'), apd('JFK'), apd('SYD'), apd('SXF'), apd('UFA'))
    rt = ComplexRoute(airports, cud, acd('747'), ful)
    dub = (apd('DUB').latitude, apd('DUB').longitude)
    jfk = (apd('JFK').latitude, apd('JFK').longitude)
    print('DUB-JFK(km):', Route.calcDistance(dub, jfk))
    print('Routing Nodes:\n{}\n'.format(rt.points))
    print('Distance Matrix:\n{}\n'.format(rt.distance_matrix))
    print('All possible Routes(including symmetrical '
          'routes):\n{}\n'.format(rt.possible_routes))
    print('Routes Distances(km):\n{}\n'.format(rt.route_distances))
    print('Shortest Path:\n{}\n'.format(rt.opt_route))
    print('Shortest Path Distance(km):\n{}\n'.format(rt.opt_route_distance))
    print('Most Economic Path:\n{}\n'.format(rt.eco_route))
    print('Most Economic Path Cost:\n{}\n'.format(rt.eco_route_cost))

if __name__ == '__main__':
    test()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
App main data analysis controler that deals with routes.
Part of the Fuel Management software.
@since:28/04/2016
@author:Tirdad Kiafar
"""
import tkinter as tk
from tkinter import ttk
from util import util
from data.router import ComplexRoute
from data.currency import Currency, Currencies


###############################################################################
class RouteFrame(ttk.Frame):
    '''App main data analysis controler that deals with routes.'''
    def __init__(self, master, airports, route_mode, currencies, aircraft,
                 fuelmap, mode='dynamic'):
        '''Constructor. This builds up the input frame.

        Args:
            master (tkinter.Toplevel): master tk window.
            airports (list): list of airports to be analysed.
            route_mode (str): static for single route, dynamic for analysis.
            aircraft (Aircraft): data holder for aircraft
            mode (str): "static" or "dynamic"'''
        # setting up the container
        ttk.Frame.__init__(self, master)
        # set class attributes
        self._master = master
        self._airports = airports
        self._route_mode = route_mode
        self._fuelmap = fuelmap
        self._mode = mode
        # make treeview take as much space as possible
        self.__grid_weight()
        # add treeview widget
        self.__addWidget()
        # setup router
        self._router = ComplexRoute(airports, aircraft, fuelmap, self._mode)
        # show first data row: possible routes
        self.__show_routes()
        # show second data row: shortest route
        self.__show_shortest()
        # show third data row: economic analysis
        self.__show_eco()

    def __grid_weight(self):
        '''configure row and column grid wight of parrent'''
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def __addWidget(self):
        '''Configures the treeview widget that diplays data'''
        # add vertical scrollbar
        self._vsb = ttk.Scrollbar(self, orient="vertical")
        # create treeview and limit its height
        self._trv_data = ttk.Treeview(self, height=3,
                                      yscrollcommand=lambda f, l: self.__scrl(
                                          self._vsb, f, l))
        # associate scrollbar with treeview
        self._vsb['command'] = self._trv_data.yview
        # add root items to treeview
        # all routes
        self._trv_data.insert('', tk.END, 'all', text='')
        # distance analysis
        self._trv_data.insert('', tk.END, 'distance', text='')
        # economic route and and route costs
        self._trv_data.insert('', tk.END, 'economy', text='')
        # change treeview rowheight
        util.ttk_tree_style(35, self._trv_data)
        # add treeview
        self._trv_data.grid(row=0, column=0, stick='nesw')
        self._vsb.grid(row=0, column=1, sticky='ns')

    def __scrl(self, sbar, first, last):
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

    def __show_routes(self):
        '''Shows fist row of data: number of routes and possible routes'''
        txt = 'Number of all posible routes: {}'.format(
            len(self._router.possible_routes))
        self._trv_data.item('all', text=txt)
        # add routes as the children of first treeview node
        idx = 0
        for route in self._router.possible_routes:
            # build node text gradually
            txt = ''
            for node in route:
                name = self._airports[int(node)].name
                # truncate long names
                name = name if len(name) < 20 else name[:19]+'..'
                txt += name+'> '
            # remove last two charachters of text e.g. "> "
            txt = txt[:-2]
            self._trv_data.insert('all', tk.END, 'route'+str(idx), text=txt)
            idx += 1

    def __show_shortest(self):
        '''Shows second row of data: shortest route and route distances'''
        txt = 'Shortest Route: {} km\n'.format(
            int(self._router.opt_route_distance))
        for node in self._router.opt_route:
            name = self._airports[int(node)].name
            # truncate long names
            name = name if len(name) < 20 else name[:19]+'..'
            txt += name + '> '
        # remove last two charachters of text e.g. "> "
        txt = txt[:-2]
        self._trv_data.item('distance', text=txt)
        # add routes as the children of second treeview node
        idx = 0
        for i in range(len(self._router.route_distances)):
            # build node text gradually
            txt = ''
            # add route preview (airport iata codes) e.g. DUB>JFK...
            for node in self._router.possible_routes[i]:
                txt += self._airports[int(node)].iata_code+'>'
            # replace last ">" with:
            txt = txt[:-1]+': '
            # add distance to txt
            txt += str(int(self._router.route_distances[i]))+' km'
            self._trv_data.insert(
                'distance', tk.END, 'shortest'+str(idx), text=txt)
            idx += 1

    def __show_eco(self):
        '''Shows third row of data: economic route and cost analysis.'''
        if self._router.eco_route_cost > -1:  # valid routes present
            txt = 'Most Economic Route Cost: {}€\n'.format(
                int(self._router.eco_route_cost))
        else:  # no valid route
            txt = 'No valid travel path found. Please change the aircraft.'
        er = self._router.eco_route
        # add second line of text, route details for second
        # e.g. DUB>JFK:2544€
        for i in range(len(er)-1):
            txt += self._airports[int(er[i])].iata_code + '>' + \
                self._airports[int(er[i+1])].iata_code + ':' + \
                str(int(self._router.eco_route_details[i])) + '€, '
        # remove last ", "
        txt = txt[:-2]
        self._trv_data.item('economy', text=txt)
        # add eco details as children of economy item
        idx = 0
        pr = self._router.possible_routes
        for i in range(len(self._router.route_costs)):
            # build node text gradually
            txt = ''
            for j in range(len(pr[i])-1):
                txt += self._airports[int(pr[i][j])].iata_code + '>' + \
                    self._airports[int(pr[i][j+1])].iata_code + ':'
                if self._router.route_costs[i] == 0:
                    # if the route is invalid its details is [0]
                    cost = '0'
                else:
                    # get specific path cost
                    cost = str(int(self._router.eco_details[i][j]))
                txt += cost + '€, '
            # add total cost
            if self._router.route_costs[i] == 0:
                # add "Invalid" for invalid routes
                txt += 'Invalid Route'
            else:
                txt += 'Total Cost: '+str(int(self._router.route_costs[i]))+'€'
            self._trv_data.insert('economy', tk.END, 'eco'+str(idx), text=txt)
            idx += 1

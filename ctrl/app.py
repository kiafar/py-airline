#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main fuel management application window and controller
@since:28/04/2016
@author:Tirdad Kiafar
"""
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from PIL import Image
import calendar
from util import util
from ctrl.toolbar import Toolbar
from ctrl.input_frame import InputFrame
from ctrl.route_frame import RouteFrame
from data.data_storage import DataStore
from data.settings import Settings
from data.aircraft import Aircrafts, Aircraft
from data.airport import AirportAtlas, Airport
from data.currency import Currencies, Currency
from data.fuelprice import FuelMap, FuelObj
from view.splashscreen import SplashScreen
from view.ttkcalendar import Calendar
from view.map import Map
from view.autoComplete import MyEntry
from view.winsettings import WinSettings
import view.splash as splash


###############################################################################
class App(tk.Tk):
    '''Main View/Controller object of the FuelManagement app.'''
    def __init__(self):
        '''Constructor. Initializing components of the screen.'''
        tk.Tk.__init__(self)
        # Loading settings
        self._s = Settings(file_path=r'./data/settings.ini')
        # show splash screen while loading data and constructing GUI
        splash_path = self._s.getStr('splash', 'ASSETS')
        splash_time = self._s.getFloat('splash_time', 'UI')
        with SplashScreen(self, splash_path, splash_time):
            # set app title & icon
            self.title(self._s.getStr('title', 'UI'))
            self.iconbitmap(self._s.getStr('icon', 'ASSETS'))
            # load data
            self.__load_data()
            # construct UI
            self.__addWidgets()
            # event binding
            self.__addEvents()
            # update settings file upon termination
            self.protocol('WM_DELETE_WINDOW', self.__close)
        # centering window, should be after splash to get updated sizes
        util.center(self)

    def __load_data(self):
        # Load data
        self._travel_data = DataStore(self._s.getStr('data', 'DATA'))
        # Load aircrafts
        self._aircrafts = Aircrafts(self._s.getStr('aircrafts', 'DATA'))
        # Load airports
        self._airports = AirportAtlas(self._s.getStr('airports', 'DATA'))
        # Load Currencies
        self._currencies = Currencies(self._s.getStr('currencies', 'DATA'))
        # Load fuel data
        self._fuelmap = FuelMap(self._s.getStr('fuelprices', 'DATA'))
        # Load marker images for map
        self.__load_markers()
        # this variable holds the data tabs (type RouteFrame) in notebook
        # the keys are travel weak (year+weak)
        self._tabs = {}

    def __addWidgets(self):
        # add toolbar on top
        self.__addtoolbar()
        # add a reference for preferences window, needed to check if its open
        self._win_settings = None
        # add a reference for about window, needed to check if its open
        self._win_about = None
        # add notebook (tabbed view)
        self.__addNotebook()
        # add airport tab to the notebook
        self.__addAirportsTab()
        # add aircraft combobox to the airports tab
        self.__addAircraft()
        # adding calendar
        self.__addCalendar()
        # add map
        if self._s.getBool('disable_map') is not True:
            self.__addMap()
        # add system message
        self.__addSysMsg()
        # add event handlers
        self.__addEvents()
        # set stretching behavior for grid
        self.columnconfigure(0, weight=1)  # toolbar, notebook, map
        self.columnconfigure(1, weight=0)  # calendar, message
        self.rowconfigure(0, weight=0)  # toolbar
        self.rowconfigure(1, weight=0)  # notebook, calendar
        self.rowconfigure(2, weight=1)  # map, message

    def __addtoolbar(self):
        '''Adds top toolbar and registers callbacks'''
        # toolbar button names
        names = self._s.getList('tool_buttons', 'UI')
        # icons associated with toolbar buttons
        icons = self._s.getList('tool_icons', 'ASSETS')
        icons = [tk.PhotoImage(file=icons[i]) for i in range(len(icons))]
        # Create toolbar
        self._toolbar = Toolbar(self, names, icons)
        # place toolbar
        self._toolbar.grid(row=0, column=0,
                           columnspan=2,
                           pady=10,
                           stick='nesw')

    def __addNotebook(self):
        '''Adds notebook(tabbed view) to the master'''
        self._notebook = ttk.Notebook(self)
        # placing notebook on master
        self._notebook.grid(row=1, column=0, stick='new')

    def __addAirportsTab(self):
        '''Adds input tab inside notebook.'''
        tags = self._s.getList('airport_entry_tags', 'UI')
        # if autocomplete option is set to work with names
        records = self._airports.names
        info = self._airports.codes
        secColWid = 50
        if self._s.getBool('airport_by_name') is False:
            # reverse the tags shown in autocomplete entry
            tags.reverse()
            records, info = info, records
            secColWid = 250
        self._frm_airports = InputFrame(self._notebook,
                                        tag_list=tags,
                                        record_list=records,
                                        info_list=info,
                                        secColWidth=secColWid)
        self._notebook.add(self._frm_airports, text='Data Entry')

    def __addAircraft(self):
        '''Adds aircraft entry to the aircraft tab.'''
        # add MyEntry
        self._ent_aircraft = MyEntry(self._frm_airports, secColWidth=80)
        # place entry
        self._ent_aircraft.grid(row=3, column=1, stick='nesw',
                                ipadx=5, ipady=5, padx=10, pady=10)
        # trigger auto complete
        self._ent_aircraft.initAutoComplete(['Aircraft', 'Code'],
                                            self._aircrafts.names,
                                            self._aircrafts.codes,
                                            'Aircraft')

    def __addCalendar(self):
        # creating a normal label to replace the labelFrame blue text widget
        lbl = ttk.Label(text=self._s.getStr('calendar_label', 'UI'))
        # adding a LabelFrame to wrap around calendar
        self._lbf_calendar = ttk.LabelFrame(self, labelwidget=lbl)
        self._lbf_calendar.grid(row=1, column=1, stick='nes', ipadx=5, padx=5)
        self._calendar = Calendar(self._lbf_calendar,
                                  firstweekday=calendar.MONDAY,
                                  selectiontype=Calendar.SELECT_WEEK)
        self._calendar.pack()

    def __addMap(self):
        self._map = Map(self, callback=self._on_map)
        self._map.grid(row=2, column=0, stick='nesw')

    def __addSysMsg(self):
        # creating a normal label to replace the labelFrame blue text widget
        lbl = ttk.Label(text=self._s.getStr('system_message', 'UI'))
        # adding a LabelFrame to wrap around calendar
        self._lbf_msg = ttk.LabelFrame(self, labelwidget=lbl)
        # put system message frame on colmn 0 if there is no map, otherwise 1
        col = 0 if self._s.getBool('disable_map') else 1
        self._lbf_msg.grid(row=2, column=col, stick='nesw', ipadx=5, padx=5)
        # creating a bold font for message text
        fnt = font.Font(family='Calibri', weight='bold')
        # build notice message up
        msg = ''
        for i in range(1, 3):
            msg += self._s.getStr('notice'+str(i), 'UI') + '\n\n'
        # if map is enabled add its message
        if self._s.getBool('disable_map') is False:
            msg += self._s.getStr('notice_map', 'UI')+'\n\n'
            wrap = 230
        else:
            wrap = 530
        # if first airport is in Ireland add its message
        if self._s.getBool('first_airport') is True:
            msg += self._s.getStr('notice_airport', 'UI')
        self._lbl_msg = ttk.Label(self._lbf_msg,
                                  wraplength=wrap,
                                  justify=tk.LEFT,
                                  font=fnt,
                                  text=msg)
        self._lbl_msg.pack()

    def __addEvents(self):
        # Toolbar on click events
        handlers = [self._on_airports,
                    self._on_route,
                    self._on_load,
                    self._on_save,
                    self._on_pref,
                    self._on_about]
        self._toolbar.bindings(handlers)

    def __add_tab(self, week) -> RouteFrame:
        '''Adds a data tab to the notebook.

        Args:
            week (str): Travel week. e.g. "2016 Week 13"
        Returns:
            RouteFrame: controller for routing.'''
        airports = []
        # extract airports
        for i in self._frm_airports._entries:
            # if airports are by name
            if self._s.getBool('airport_by_name'):
                ap = self._airports.get_by_name(i.get())
            else:  # if airports are by iata code
                ap = self._airports(i.get())
            airports.append(ap)
        # create controller/view analyser
        route_frame = RouteFrame(self,
                                 airports,
                                 self._frm_airports.var_path.get(),
                                 self._currencies,
                                 self._aircrafts.get_by_str(
                                     self._ent_aircraft.get()),
                                 self._fuelmap,
                                 mode=self._frm_airports.var_path.get())
        # display tab
        self._notebook.add(route_frame, text=week)
        # set focus on new tab
        util.set_notebook_focus(self._notebook, week)
        # add the object to tabs dict
        self._tabs[week] = route_frame
        return route_frame

    def __load_markers(self):
        '''Load markers for map'''
        self._markers = []
        # get marker image paths
        markers_paths = self._s.getList('markers', 'ASSETS')
        for path in markers_paths:
            self._markers.append(Image.open(path))

    def __draw_map(self, points):
        '''Draws a path on map'''
        # TODO: i couldnt find a way to clean the map so i make a new one
        if self._map.clean_canvas() is False:
            self._map.grid_remove()
            self._map = None
            self.__addMap()
        # extract map colors
        color = self._s.getList('map_colors', 'UI')
        # iterate through points
        for i in range(len(points)-1):
            # add marker to map for current point
            self._map.draw_marker(self._markers[i], points[i])
            self._map.draw_geodesic(points[i], points[i+1], 2, color[i])

    def __update_data(self, router, week):
        '''updates the data with router data. Does not check if data exists.

        Args:
            router (ComplexRoute): router controller.
            week (str): travel week.'''
        # extract airport codes to store
        airports = []
        for airp in router.airports:
            airports.append(airp.iata_code)
        # make data list and add update current data
        data = [router._mode,
                airports,
                week,
                router.aircraft,
                router.opt_route,
                router.opt_route_distance,
                router.eco_route,
                router.eco_route_cost]
        self._travel_data.add(self._travel_data.map_data(data))

    # Event handlers ----------------------------------------------------------
    def __close(self):
        '''Called upon app termination'''
        # save settings
        self._s.update()
        self.destroy()

    def _on_about(self):
        '''Show about window. If it is open does nothing.'''
        if self._win_about is not None:
            return
        s = splash.showSplash(self, self._s.getList('about_images', 'ASSETS'))
        self._win_about = s.window
        # close window on click and escape key press
        self._win_about.bind("<Button-1>", self.__close_win_about)
        self._win_about.bind("<Key>", self.__close_win_about)
        # forcing focuse on about window to intercept keypress
        self.after(1, lambda: self._win_about.focus_force())

    def __close_win_about(self, event):
        '''Closes win_about and release its reference.'''
        self._win_about.destroy()
        self._win_about = None

    def _on_airports(self):
        '''Show input window.'''
        self._notebook.select(self._frm_airports)

    def _on_pref(self):
        '''Show preferences window. If it is open brings it to top.'''
        # quit if window already open
        if self._win_settings is not None:
            self._win_settings.lift(self)
            self._win_settings.focus()
            return
        # extract current settings to show on preferences window
        defaults = {'airport_by_name': self._s.getStr('airport_by_name'),
                    'auto_save': self._s.getStr('auto_save'),
                    'first_airport': self._s.getStr('first_airport'),
                    'disable_map': self._s.getStr('disable_map')}
        self._win_settings = WinSettings(self, defaults)
        # bind event on window close to release reference
        self._win_settings.protocol('WM_DELETE_WINDOW', self.__close_win_pref)

    def __close_win_pref(self):
        '''Preferences window is closing. Update settings.
        Note that phisycal update is done just before app termination'''
        # Show warning if map or airport display change
        exp1 = self._win_settings._varDisableMap.get()
        exp2 = self._s.getStr('disable_map')
        exp3 = self._win_settings._varAirports.get()
        exp4 = self._s.getStr('airport_by_name')
        if exp1 != exp2 or exp3 != exp4:
            messagebox.showinfo(
                'Display Change',
                'Some changes will not take effect untill app is restarted'
            )
        self._s.setSetting('airport_by_name',
                           self._win_settings._varAirports.get())
        self._s.setSetting('auto_save',
                           self._win_settings._varAutoSave.get())
        self._s.setSetting('first_airport',
                           self._win_settings._varFirstAP.get())
        self._s.setSetting('disable_map',
                           self._win_settings._varDisableMap.get())
        self._win_settings.destroy()
        self._win_settings = None

    def _on_route(self, on_load=False):
        '''Show routing window. Only enabled if user is on input window.'''
        # reset styles for getting white background
        for i in self._frm_airports._entries:
            i.config(style='TEntry')
        self._ent_aircraft.config(style='TEntry')
        # reset notice message
        self._lbl_msg['text'] = ''
        # check input validity, if fail quit
        if self.__validateInput() is False:
            return
        # extract travel week out of calendar
        # tab text and data store key is year and week.e.g. 2016 Week 12
        week = self._calendar.selection
        # week is now isocalendar tuple, date[0]=year and date[1]=week
        week = str(week[0])+' Week '+str(week[1])
        # check if selected week is not already taken, and check for override
        if self.__validateTravelWeek(week) is False and on_load is False:
            self._lbl_msg['text'] = self._s.getStr('invalid_week', 'UI')
            return
        # reset calendar selection
        self._calendar._selection = None
        # add data tab to notebook and get a reference to router controller
        route_cont = self.__add_tab(week)
        # update notice text
        if on_load is True:  # data loaded
            txt = 'Data loaded for '
        else:  # data calculated
            txt = 'Routes calculated for '
        txt += 'Year '+week+'\n\n'
        if route_cont._router.eco_route_cost == -1:  # no possible route
            txt += 'No valid travel path found. It means either the selected '\
                'aircraft has limited flying range or a node is selected too'\
                ' far away..'
        self._lbl_msg['text'] = txt
        # save data if auto save is on
        if self._s.getBool('auto_save'):
            self.__update_data(route_cont._router, week=week)
            self._travel_data.save()
        # draw map if routing is successful and map enabled
        exp1 = len(route_cont._router.eco_route) != 0
        exp2 = self._s.getBool('disable_map') is False
        if exp1 and exp2:
            pass
            self.__draw_map(route_cont._router.map_points(
                route_cont._router.eco_route))

    def _on_save(self):
        '''Save output data. Only enabled in routing window.'''
        # update current data
        for week, cont in self._tabs.items():
            self.__update_data(cont._router, week)
            self._travel_data.save()

    def _on_load(self):
        '''Load data'''
        # check if user has selected travel time
        if self.__validateCalendar() is False:
            return
        # get selected week out of calendar
        week = self._calendar.selection
        week = str(week[0])+' Week '+str(week[1])
        # quit if there is no record associated with that date
        if week not in self._travel_data.keys():
            self._lbl_msg['text'] = self._s.getStr('no_record', 'UI')
            return
        # for shortcut: set fields and call on load event
        # note that in a big software this is not a good idea because we have
        # lots of custom settings associated with events but it works here
        data = self._travel_data[week]
        # add airports to fields
        for i in range(len(data['airports'])):
            if self._s.getBool('airport_by_name') is False:
                # insert codes directly
                ent = self._frm_airports._entries[i]
                ent.delete(0, tk.END)
                ent.insert(0, data['airports'][i])
            else:
                # get airport name and insert it
                code = data['airports']
                name = self._airports(data['airports'][i]).name
                ent = self._frm_airports._entries[i]
                ent.delete(0, tk.END)
                ent.insert(0, name)
            ent.config(foreground='#000')
        # add aircraft
        self._ent_aircraft.delete(0, tk.END)
        self._ent_aircraft.insert(0, data['aircraft'])
        self._ent_aircraft.config(foreground='#000')
        # set routing mode
        self._frm_airports.var_path.set(data['mode'])
        # simulate on route button
        self._on_route(on_load=True)

    def _on_map(self, lat, lon):
        '''When user clicks map this handler is called.
        On data input phase user can select airports by clicking map'''
        # find first empty input field
        for i in self._frm_airports._entries:
            exp1 = i.get() == ''
            exp2 = i.get().startswith('Airport')
            exp3 = i.get().startswith('Home ')
            # if entry text is empty or defauld (place holder)
            if exp1 or exp2 or exp3:
                i.delete(0, tk.END)
                if self._s.getBool('airport_by_name'):
                    ap = self._airports.find_closest(lat, lon).name
                else:
                    ap = self._airports.find_closest(lat, lon).iata_code
                i.insert(0, ap)
                i.config(foreground='#000')
                break

    # Validates user input ----------------------------------------------------

    def __validateTravelWeek(self, week) -> bool:
        '''Checks if the week already exists.

        Args:
            week (str): travel week to be checked.'''
        # If week is open in a notebook tab
        if week in self._tabs.keys():
            return False
        # If week is in found in data storage
        if week in self._travel_data.keys():
            return False
        return True

    def __validateInput(self) -> bool:
        '''Validates user input.

        Returns:
            bool: False if validation failed, else True'''
        # vacancy test
        if self.__validateVacancy() is False:
            return False
        # verification test
        elif self.__verifyFields() is False:
            return False
        # uniqueness test
        elif self.__verifyUniqueness() is False:
            return False
        # first airport being in Ireland test
        elif self.__validateFirstAirport() is False:
            return False
        # check if user has selected travel time
        elif self.__validateCalendar() is False:
            return False
        return True

    def __validateVacancy(self):
        '''check if airport fields are vacant'''
        incomplete = False
        for i in self._frm_airports._entries:
            exp1 = i.get() == ''
            exp2 = i.get().startswith('Airport')
            exp3 = i.get().startswith('Home ')
            # if entry text is empty or defauld (place holder)
            if exp1 or exp2 or exp3:
                # change the backgound color of entry
                util.ttk_style(i, '#FFCC99')
                incomplete = True
        # check if aircraft field is vacant
        if self._ent_aircraft.get() in ['', 'Aircraft']:
            # change the backgound color of entry
            util.ttk_style(self._ent_aircraft, '#FFCC99')
            incomplete = True
        if incomplete:
            msg = self._s.getStr('notice_incomplete', 'UI')
            self._lbl_msg['text'] = msg
        return not incomplete

    def __verifyFields(self):
        '''verify input data'''
        invalid = False
        for i in self._frm_airports._entries:
            if self._s.getBool('airport_by_name') is True:
                if self._airports.get_by_name(i.get()) is None:
                    util.ttk_style(i, '#F7B3DA')
                    invalid = True
            else:  # airports are by code
                try:
                    self._airports(i.get().upper())
                except KeyError:
                    util.ttk_style(i, '#F7B3DA')
                    invalid = True
        # validate aircraft
        valid_airc = False
        ent_aircraft = self._ent_aircraft.get()
        for code, aircraft in self._aircrafts.items():
            if ent_aircraft.lower() == str(aircraft).lower():
                valid_airc = True
        if valid_airc is False:
            util.ttk_style(self._ent_aircraft, '#F7B3DA')
            invalid = True
        if invalid:
            msg = self._s.getStr('notice_invalid', 'UI')
            self._lbl_msg['text'] = msg
        return not invalid

    def __verifyUniqueness(self):
        '''check if all airports are unique'''
        unique = True
        if self._s.getBool('airport_by_name'):
            lst = [self._airports.get_by_name(i.get())
                   for i in self._frm_airports._entries]
        else:
            lst = [self._airports(i.get())
                   for i in self._frm_airports._entries]
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j:
                    # for this we need to overload airport __eq__&__ne__
                    if lst[i] == lst[j]:
                        util.ttk_style(self._frm_airports._entries[j],
                                       '#ADEAEA')
                        unique = False
        if unique is False:
            self._lbl_msg['text'] = self._s.getStr('notice_unique', 'UI')
        return unique

    def __validateFirstAirport(self):
        # If first airport is not set to be in Ireland return True
        if self._s.getBool('first_airport') is False:
            return True
        if self._s.getBool('airport_by_name'):
            a = self._airports.get_by_name(
                self._frm_airports._entries[0].get())
        else:
            a = self._airports(self._frm_airports._entries[0].get())
        if a.iso_country != 'IE':
            util.ttk_style(self._frm_airports._entries[0], '#C1FFC1')
            self._lbl_msg['text'] = self._s.getStr('notice_airport', 'UI')
            return False
        return True

    def __validateCalendar(self):
        '''Checks if travel week is selected'''
        if self._calendar.selection is None:
            self._lbl_msg['text'] = self._s.getStr('notice_week', 'UI')
            return False
        return True

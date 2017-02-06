#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings top level window.
@since:30/04/2016
@author:Tirdad Kiafar
"""
import tkinter as tk
from tkinter import ttk
from util import util


###############################################################################
class WinSettings(tk.Toplevel):
    '''A tkinter toplevel window that wraps settings of fuel management app'''
    def __init__(self, master=None, defaults={}):
        '''Constructor.
        
        Args:
            master (tkinter.widget): Parent of the window.
            defaults (dict): dictionary of default value. Must have these keys:
                "airport_by_name","auto_save","disable_map"'''
        tk.Toplevel.__init__(self, master)
        # getting screen dimentions
        scrW = self.winfo_screenwidth()
        scrH = self.winfo_screenheight()
        # Calculate positioning for window with estimated dimentions
        Xpos = (scrW - 330) // 2
        Ypos = (scrH - 200) // 2
        # center current window
        self.geometry('+{}+{}'.format(Xpos, Ypos))
        # set window title
        self.title('Preferences')
        self._defaults = defaults
        self.resizable(width=tk.FALSE, height=tk.FALSE)
        # add StingVars for widgets
        self.__addVars()
        # add widgets
        self.__addWidgets()
        # placing widgets on window
        self.__placeWidgets()
        # setting default (current) values
        self.__setDefaults()
        # set focus to this window
        self.focus()
        # bringing window to top
        self.lift(master)

    def __addWidgets(self):
        '''Adds tkinter widgets to the window.'''
        self.__addFrmAirports()
        self.__addChecks()

    def __addVars(self):
        # StringVar holding the value of "Get Airports By"
        self._varAirports = tk.StringVar()        
        # StringVars associated with checkboxes
        self._varAutoSave = tk.StringVar()
        self._varDisableMap = tk.StringVar()
        self._varFirstAP = tk.StringVar()

    def __addFrmAirports(self):
        # create a normal label to replace the labelFrame blue text widget
        lbl = ttk.Label(self, text="Input Airports By")
        # add a LabelFrame to wrap around calendar
        self._frm_airports = ttk.LabelFrame(self, labelwidget=lbl)
        # add radio buttons
        self._rad_byName = ttk.Radiobutton(self._frm_airports,
                                           text='By Airport Name',
                                           value='True',
                                           variable=self._varAirports)
        self._rad_byCode = ttk.Radiobutton(self._frm_airports,
                                           text='By Airport IATA Code',
                                           value='False',
                                           variable=self._varAirports)

    def __addChecks(self):
        # creating checkboxes
        self._chk_autosave = ttk.Checkbutton(self,
                                             text='Auto Save Data',
                                             onvalue='True',
                                             offvalue='False',
                                             variable=self._varAutoSave)
        tx = 'Force First Airport in Ireland'
        self._chk_firstAP = ttk.Checkbutton(self,
                                            text=tx,
                                            onvalue='True',
                                            offvalue='False',
                                            variable=self._varFirstAP)
        self._chk_disablemap = ttk.Checkbutton(self,
                                               text='Disable Map',
                                               onvalue='True',
                                               offvalue='False',
                                               variable=self._varDisableMap)

    def __placeWidgets(self):
        '''Places widgets on window.'''
        self._rad_byName.pack(side=tk.LEFT, padx=10, pady=5)
        self._rad_byCode.pack(side=tk.LEFT, padx=10, pady=5)
        self._frm_airports.grid(row=0, column=0, padx=10, pady=5, stick='nesw')        
        self._chk_autosave.grid(row=1, column=0, padx=10, pady=5, stick='nesw')
        self._chk_firstAP.grid(row=2, column=0, padx=10, pady=5, stick='nesw')
        self._chk_disablemap.grid(row=3, column=0,
                                  padx=10, pady=5, stick='nesw')

    def __setDefaults(self):
        '''Setting default (current) values.'''
        self._varAirports.set(self._defaults['airport_by_name'])
        self._varFirstAP.set(self._defaults['first_airport'])
        self._varAutoSave.set(self._defaults['auto_save'])
        self._varDisableMap.set(self._defaults['disable_map'])


###############################################################################
def test():
    root = tk.Tk()
    defaults = {'airport_by_name': 'True',
                'auto_save': 'True',
                'disable_map': 'False',
                'first_airport': 'True'}
    win = WinSettings(root, defaults)
    root.mainloop()

if __name__ == '__main__':
    test()

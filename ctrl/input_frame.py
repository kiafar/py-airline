#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Manages airports input frame.
Part of the Fuel Management software.
@since:28/04/2016
@author:Tirdad Kiafar
"""
import tkinter as tk
from tkinter import ttk
from view.autoComplete import MyEntry


###############################################################################
class InputFrame(ttk.Frame):
    '''The user input frame.'''
    def __init__(self, master, **kwargs):
        '''Constructor.
        This builds up the input frame.

        Args:
            master (tkinter.Toplevel): master tk window.
        Keyword Args:
            tag_list (tuple): a tuple of headers for records.
            record_list (tuple): a tuple of records in first column.
            info_list (tuple): a tuple of record info,
                lenght must match record list.
            secColWidth (int): Width of the second column of Entries.'''
        # setting up the container
        ttk.Frame.__init__(self, master)
        # extracting auto complete data from kwargs
        self._tag_list = kwargs.get('tag_list', ('Records', 'Info'))
        self._record_list = kwargs.get('record_list', [])
        self._info_list = kwargs.get('info_list', [])
        self._secColWidth = kwargs.get('secColWidth', 45)
        # setting width stretch portion of frame, note that we are using grid
        for i in range(2):
            self.columnconfigure(i, weight=1)
        # adding radio buttons
        self.var_path = tk.StringVar()
        self.__addRadios()
        # programatically select dynamic path
        self.var_path.set('dynamic')
        # adding custom entries
        self._entries = []
        self.__addEntries()
        # setting stick and padding for widgets
        for widget in self.grid_slaves():
            # avoiding y padding on radio buttons
            pady = 10 if type(widget) != ttk.Radiobutton else 0
            widget.grid_configure(stick='nsew',
                                  ipadx=5,
                                  ipady=5,
                                  padx=10,
                                  pady=pady)

    def __addRadios(self):
        self._rad_dynamic = ttk.Radiobutton(self,
                                            variable=self.var_path,
                                            value='dynamic',
                                            text='Dynamic Path')
        self._rad_static = ttk.Radiobutton(self,
                                           variable=self.var_path,
                                           value='static',
                                           text='Static Path')
        self._rad_dynamic.grid(row=0, column=0)
        self._rad_static.grid(row=0, column=1)

    def __addEntries(self):
        '''Add entries to the frame.'''
        for i in range(5):
            # Place holder of auto complete entry
            strPlaceHolder = 'Home Airport' if i == 0 else 'Airport'+str(i)
            entry = MyEntry(self, secColWidth=self._secColWidth)
            # storing reference for later use
            self._entries.append(entry)
            # placing entry
            entry.grid(row=int(i/2)+1, column=i % 2)
            # trigger auto complete
            entry.initAutoComplete(self._tag_list,
                                   self._record_list,
                                   self._info_list,
                                   strPlaceHolder)

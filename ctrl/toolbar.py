#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Toolbar class. Creates a flat toolbar with the given names and icons.
@since:28/04/2016
@author:Tirdad Kiafar
"""
import tkinter as tk
from tkinter import font
from tkinter import ttk


###############################################################################
class Toolbar(ttk.Frame):
    '''Top toolbar of FuelManagement App'''
    def __init__(self, master, names, icons=[]):
        '''Constructor. Initializing components of the toolbar.
        Uses function invocation for events.

        Args:
            master(Tk): tkinter container.
            names(list): List of button names.
            icons(list): List of PhotoImages to add to the buttons.'''
        # checking data validity
        if icons:
            if len(icons) != len(names):
                raise Exception('Lenght mismatch: names and icons')
        ttk.Frame.__init__(self, master)
        # store buttons, button and names
        self._buttons = []
        self._names = names
        self._icons = icons
        # add buttons
        self.__addButtons()

    def bindings(self, handlers):
        '''Binds events to toolbar buttons'''
        if len(self._names) != len(handlers):
            raise Exception('Lenght mismatch on: names and handlers')
        self._handlers = handlers
        # binding handlers to buttons
        for i in self._buttons:
            i.config(command=handlers[self._buttons.index(i)])

    def __addButtons(self):
        '''Adds buttons to the frame.'''
        # creating a bold font for button text
        fnt = font.Font(family='Calibri', weight='bold')
        # iterating over names and creating buttons
        for i in range(len(self._names)):
            but = tk.Button(self,
                            text=self._names[i],
                            relief='flat',
                            font=fnt,
                            padx=10)
            # placing the button on container which is the frame
            but.pack(side=tk.LEFT, fill=tk.X, expand=True)
            # adding icons if available
            if self._icons:
                but.config(image=self._icons[i], compound=tk.LEFT, padx=10)
            # storing a reference to the button
            self._buttons.append(but)

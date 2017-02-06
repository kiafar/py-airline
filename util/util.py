#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility functions. These functions are generally purposed to do general
operations on different components and thus could potentialy be part of
a specific class, however for this program there was no need to develop
those classes.
@since:30/04/2016
@author:Tirdad Kiafar
"""
from math import pi, sin, cos, acos
from tkinter import ttk


def get_abs_pos(widget, level=-1) -> tuple:
    '''Returns the absolute position of a tkinter widget.

    Args:
        widget (tkinter.Widget): the tkinter widget.
        level (int): depth level of parents to be calculated.
            If -1 it will go all the way up to root.
    Returns:
        tuple: (x, y) positions.'''
    x = y = 0
    level = 9999 if level == -1 else level
    master = widget
    while master is not None and level > -1:
        x += master.winfo_x()
        y += master.winfo_y()
        master = master.master
        level -= 1
    return x, y


def center(toplevel):
    '''Places a toplevel tkinter window at center of screen. From:
    http://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter

    Args:
        toplevel (tkinter.toplevel): tkinter window.'''
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(i) for i in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def ttk_style(widget, color) -> str:
    '''Makes a style for items for ttk.Entry to override background color.

    Args:
        widget (ttk.Entry): the ttk entry widget to apply background color.
        color (str): background color to be applied. e.g. "#ffffff"
    Returns:
        str: style name created.'''
    style = ttk.Style()
    # on windows 8.1 with tcl/tk 8.6 this line generates error, anyway
    # as far as it gets excecuted is enough to change background color. From:
    # http://stackoverflow.com/questions/17635905/ttk-entry-background-colour
    try:
        style.element_create("plain.field", "from", "clam")
    except:
        pass
    style.layout("Missing.TEntry",
                 [('Entry.plain.field', {'children': [(
                     'Entry.background', {'children': [(
                          'Entry.padding', {'children': [(
                              'Entry.textarea', {'sticky': 'nswe'})],
                                            'sticky': 'nswe'})],
                                          'sticky': 'nswe'})],
                                          'border': '2', 'sticky': 'nswe'})])
    style.configure('Missing.TEntry',
                    fieldbackground=color)
    widget.config(style='Missing.TEntry')
    return "Missing.TEntry"


def ttk_tree_style(rowheight, widget):
    '''Makes a custom style for a ttk treeview and sets it

    Args:
        rowheight (int): new row height. default is 20.
        widget (ttk.Treeview): widget to be changed.'''
    style = ttk.Style()
    style.configure('Custom.Treeview',
                    rowheight=rowheight)
    widget.config(style='Custom.Treeview')
    return "Missing.TEntry"


def set_notebook_focus(notebook, text) -> bool:
    '''Sets focus to a tab in a ttk.Notebook with given text label

    Args:
        notebook (ttk.Notebook): ttk notebook widget.
        text (str): label of the tab to be selected.
    Returns:
        bool: True if successful, otherwise False'''
    # get a list of tab ids
    tabs = notebook.tabs()
    for i in tabs:
        if notebook.tab(notebook.index(i), 'text') == text:
            notebook.select(notebook.index(i))
            return True
    return False
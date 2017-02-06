#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MyEntry is an extension of ttk.Entry that adds autocomplete functionality.
The features have been developed with regards to Windows defualt text view.
@author:Tirdad Kiafar
"""
import tkinter as tk
from tkinter import ttk
from util import util
__version__ = '16.03.28'


class MyEntry(ttk.Entry):
    '''Subclass of ttk Entry that adds autocomplete functionality'''
    def __init__(self, master=None, widget=None, **kwargs):
        '''Creates a ttk Entry widget with auto complete feature

        Keyword Args:
            secColWidth (int): Width of the second column.'''
        # instance attributes
        # protected attributes
        self._record_list = ()
        self._info_list = ()
        self._tag_list = ()
        self._default_text = kwargs.pop('defaultText', '')
        # private attributes
        self.__hits = []
        self.__hitsInfo = []
        self.__hitIdx = 0
        self.__position = 0
        self.__treeview = 0
        self.__secColWidth = kwargs.pop('secColWidth', 45)
        self.__isTreeviewUp = False  # for popop treeview
        # unique way of initializing tk widgets instead of super
        ttk.Entry.__init__(self, master, widget, **kwargs)
        self.bind('<KeyPress>', self.__keyPress)
        # this is needed to update the tree view
        self.bind('<KeyRelease>', self.__keyRelease)
        self.bind('<Control-Key-a>', self.__selectAll)
        # just in case caps lock is on
        self.bind('<Control-Key-A>', self.__selectAll)
        self.bind('<FocusOut>', self.__FocusOut)
        self.bind('<FocusIn>', self.__FocusIn)

    def initAutoComplete(self, tag_list=('record', 'info'),
                         record_list=(), info_list=(), default_text=''):
        '''
        Initializes auto completion.

        Args:
            tag_list (tuple): a tuple of headers for records.
            record_list (tuple): a tuple of records in first column.
            info_list (tuple): a tuple of record info,
                lenght must match record list.
            default_text (str): a helper string. shown when entry is empty.
        '''
        self.delete(0, tk.END)  # clear text
        self.tag_list = tag_list
        self.record_list = record_list
        self.default_text = default_text
        # we dont set _info_list directly cuz
        self.info_list = info_list
        self.__hits = []
        self.__hitIdx = 0
        __position = 0
        self.__set_default_text()

    # getter/Setters
    @property
    def default_text(self):
        return self._default_text

    @default_text.setter
    def default_text(self, default_text=''):
        self._default_text = default_text

    @property
    def tag_list(self):
        return self._tag_list

    @tag_list.setter
    def tag_list(self, tag_list=('data', 'info')):
        self._tag_list = tag_list

    @property
    def record_list(self):
        return self._record_list

    @record_list.setter
    def record_list(self, record_list=()):
        if self._info_list:
            if len(self._info_list) != len(record_list):
                raise Exception('record_list and info_list lenght mismatch')
        self._record_list = record_list

    @property
    def info_list(self):
        return self._info_list

    @info_list.setter
    def info_list(self, info_list=()):
        if self._record_list:
            if len(self._record_list) != len(info_list):
                raise Exception('info_list and record_list lenght mismatch')
        self._info_list = info_list

    @property
    def default_text(self):
        return self._default_text

    @default_text.setter
    def default_text(self, default_text=()):
        self._default_text = default_text

    def __selectAll(self, event):
        self.selection_range(0, tk.END)
        # for solving issue of insert marker in the middle put it at the end
        self.icursor(tk.END)
        return 'break'

    def __FocusOut(self, event=None):
        self.__set_default_text()
        if self.__isTreeviewUp:
            self.__treeview.place_forget()
            self.__hits = []
            self.__isTreeviewUp = False

    def __set_default_text(self):
        if self.get().strip() == '':
            self.delete(0, tk.END)
            self.insert(0, self._default_text)
            self.config(foreground='#777')

    def __FocusIn(self, event=None):
        # set back style if it is changed (for background color)
        if self['style'] != 'TEntry':
            self.config(style='TEntry')
        if self.get() == self._default_text:
            self.delete(0, tk.END)
            # reseting foreground and background color
            self.config(foreground='#000')

    def __keyRelease(self, event):
        self.__treeviewUpdate()

    def __keyPress(self, event):
        '''Event handler for the keypress events on the widget'''
        # store the insert mark position, if user changes the position-
        # manually this is useful
        self.__position = self.index(tk.INSERT)
        if event.keysym == 'Return':  # Enter
            self.__treeClicked()  # shortcut to the same functionality
            self.__FocusOut()  # for consistancy of UI behaviour
        elif event.keysym == 'BackSpace':
            # if there is a selection, remove it to emulate windows text fields
            if self.selection_present():
                self.__deleteSelection(self.get())
                return 'break'
            else:  # no selection present
                text = self.get()
                text = text[:self.__position-1]+text[self.__position:]
                self.__updateHits(text)
                self.__treeviewUpdate()
        # if there is a selection, remove it to emulate windows text fields
        elif event.keysym == 'Delete':
            if self.selection_present():
                if self.index(tk.INSERT) != self.index(tk.END):
                    self.__deleteSelection(self.get())
                    return 'break'
        elif event.keysym == 'Left':
            self.selection_clear()
        elif event.keysym == 'Right':
            if self.selection_present():
                if self.index(tk.SEL_LAST) == self.index(tk.END):
                    self.icursor(self.index(tk.SEL_LAST))
                self.selection_clear()
        elif event.keysym == 'Down':
            self.__cycle(next=True)
        elif event.keysym == 'Up':
            self.__cycle(next=False)
        # if input character is not empty (ctrl-alt-shift) and is in-
        # range of acceptable characters (from 'space' to 'z')
        elif len(event.char) > 0 and 32 <= ord(event.char) <= 122:
            self.insert(tk.INSERT, event.char.lower())
            position = self.__cleanSelect()
            if position == -1:
                # when all the text is selected with ctrl+a, position-
                # is -1. fix for that
                self.__position = position = 0
            # this function has a key press binding that happens before-
            # widget is updated. we take care of that here
            self.icursor(self.__position+1)
            self.__autoComplete(position)
            self.__treeviewUpdate()
            return 'break'

    def __deleteSelection(self, text):
        sel_first = self.index(tk.SEL_FIRST)
        sel_last = self.index(tk.SEL_LAST)
        txt = text[:sel_first]+text[sel_last:]
        self.delete(0, tk.END)
        self.insert(0, txt)
        self.__updateHits(txt)
        self.__treeviewUpdate()
        self.icursor(self.__position)  # return cursor where it was
        return txt

    def __autoComplete(self, position=0):
        '''core auto complete function. position is the
        index of first character of last selection'''
        hits = self.__updateHits()
        if self.__hits:
            self.__hitIdx = self.__hitIdx % len(self.__hits)
            if self.get():
                self.delete(0, tk.END)  # clean the entry
            self.insert(0, self.__hits[self.__hitIdx])
            self.select_range(position+1, tk.END)
            self.icursor(self.__position+1)

    def __updateHits(self, current_text=''):
        if not current_text:
            current_text = self.get()
        hits = []
        hitinfo = []
        for rec, info in zip(self._record_list, self._info_list):
            if rec.lower().startswith(current_text.lower()):
                hits.append(rec)
                hitinfo.append(info)
        if hits != self.__hits:  # if hit list is renewed
            self.__hitIdx = 0
            self.__hits = hits
            self.__hitsInfo = hitinfo
        return hits

    def __cycle(self, next=False):
        if self.__hits is None:  # no cyling if __hits is empty
            return
        if self.selection_present():
            position = self.index(tk.SEL_FIRST)
        else:
            position = self.__position
        self.delete(0, tk.END)  # clean the entry
        self.__hitIdx = self.__hitIdx + (1 if next else -1)
        if self.__hits:
            self.__hitIdx %= len(self.__hits)  # deal with out of bound indexes
        self.insert(0, self.__hits[self.__hitIdx])
        self.select_range(position, tk.END)
        self.icursor(self.__position)

    def __cleanSelect(self):
        '''deletes the selection and returns its starting position for
        autocomplete positioning'''
        if self.selection_present():
            position = self.index(tk.SEL_FIRST)-1
            self.delete(tk.SEL_FIRST, tk.SEL_LAST)  # del selection
        else:
            position = self.__position
        return position

    def __treeviewUpdate(self):
        if self.get() == '':
            try:
                self.__treeview.place_forget()
            except:
                pass
            self.__isTreeviewUp = False
        else:
            if self.__hits:
                if not self.__treeview:
                    self.__treeview = ttk.Treeview(columns=('data', 'info'))
                    self.__treeview.heading('data',
                                            text=self._tag_list[0])
                    self.__treeview.heading('info',
                                            text=self._tag_list[1])
                    # this removes the main column which has a left padding
                    self.__treeview['show'] = 'headings'
                    # binding single click event
                    self.__treeview.bind("<1>", self.__treeClicked)
                    # remove all the children
                self.__treeview.delete(*self.__treeview.get_children())
                for i in range(len(self.__hits)):
                    self.__treeview.insert('', tk.END, str(i))
                    self.__treeview.set(str(i), 'data', self.__hits[i])
                    self.__treeview.set(str(i), 'info', self.__hitsInfo[i])
                # for some reason setting this line increases widget width
                # gradually. so we are going the set the width after this
                self.__treeview.config(
                    height=10 if len(self.__hits) > 9 else len(self.__hits))
                # self.winfo_width() returns 3 extra pixels
                wd = self.__secColWidth
                self.__treeview.column('data', width=self.winfo_width()-wd-3)
                self.__treeview.column('info', width=wd, anchor=tk.CENTER)
                # focusing on the current item
                self.__treeview.selection_set(str(self.__hitIdx))
                # get the absolute position of self
                x, y = util.get_abs_pos(self, 2)
                self.__treeview.place(x=x, y=y+self.winfo_height())
                self.__isTreeviewUp = True
            else:
                if self.__isTreeviewUp:
                    self.__treeview.place_forget()
                    self.__isTreeviewUp = False

    def __treeClicked(self, event=None):
        if event:
            item = event.widget.identify_row(event.y)
        else:
            item = self.__treeview.selection()[0]
        if not item:  # user clicked on header
            return
        # getting the data and info of the first column of the selected row
        data = self.__treeview.item(item, 'values')[0]
        info = self.__treeview.item(item, 'values')[1]
        self.delete(0, tk.END)  # clean the entry
        self.insert(0, data)
        self.__hits = [data]
        self.__hitsInfo = [info]
        self.__hitIdx = 0
        self.__treeviewUpdate()
        # apply the focus to the main entry after 1 milisecond
        self.after(1, lambda: self.focus_force())


def test():
    '''testing the AutoComplete class'''
    tags = ('Windows Versions', 'Code')
    data = ('Windows 1.01', 'Windows 1.02', 'Windows 1.03', 'Windows 1.04',
            'Windows 2.03', 'Windows 2.10', 'Windows 2.11', 'Windows 3.0',
            'Windows 3.1', 'Windows NT 3.1', 'Windows for Workgroups 3.11',
            'Windows 3.2', 'Windows NT 3.5', 'Windows NT 3.51', 'Windows 95',
            'Windows NT 4.0', 'Windows 98', 'Windows 2000', 'Windows ME',
            'Windows XP', 'Windows XP Professional x64', 'Windows Vista',
            'Windows 7', 'Windows 8', 'Windows 8.1', 'Windows 10')
    info = ('1.01', '1.02', '1.03', '1.04', '2.03', '2.10', '2.11', '3.0',
            '3.1', 'NT 3.1', '3.11', '3.2', 'NT 3.5', 'NT 3.51', '4.0',
            'NT 4.0', '4.10', 'NT 5.0', '4.90', 'NT 5.1', 'NT 5.2', 'NT 6.0',
            'NT 6.1', 'NT 6.2', 'NT 6.3', 'NT 10.0')
    root = tk.Tk()
    root.title('Entry With Autocomplete')
    root.minsize(300, 300)
    entry = MyEntry(root, secColWidth=150)
    entry.initAutoComplete(tags, data, info, 'Windows Versions')
    entry.pack(fill=tk.X, padx=5, pady=5)
    entry.focus()
    entry1 = MyEntry(root)
    entry1.initAutoComplete(tags, data, info, 'Windows Versions')
    entry1.pack(fill=tk.X, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    test()

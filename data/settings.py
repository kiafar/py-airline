#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setting storage/writer for fuel management app.
@since:30/04/2016
@author:Tirdad Kiafar
"""
from configparser import ConfigParser
from data.fileIO import IO


###############################################################################
class Settings():
    '''Reads/Writes settings.'''

    def __init__(self, file_path=r'./settings.ini'):
        '''Constructor'''
        self._file_path = file_path
        self.__defaultSection = 'SETTINGS'
        self._config = ConfigParser()
        # create the file if it doesnt exist
        if IO.exists(file_path) is False:
            self.__createCongifFile()
        self._config.read(file_path)

    @property
    def defaultSection(self) -> str:
        '''Default section to be called upon object calling.'''
        return self.__defaultSection

    @defaultSection.setter
    def defaultSection(self, section):
        self.__defaultSection = section

    def sections(self) -> list:
        '''Returns sections in config file

        Returns:
            list: List of sections in config file.'''
        return self._config.sections()

    def getSection(self, section=None) -> dict:
        '''Returns a setting in default section.

        Args:
            section (str): Name of the section. If None: defaultSection.
        Returns:
            str: String value of setting.'''
        dic = {}
        sect = section if section else self.__defaultSection
        options = self._config.options(sect)
        for option in options:
            try:
                dic[option] = self._config.get(section, option)
                if dic[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dic[option] = None
        return dic

    def getStr(self, name, section=None) -> str:
        '''Returns an individual setting in the given section.

        Args:
            name (str): setting name.
            section (str): section of the setting. If None: defaultSection
        Returns:
            str: String value of setting. Empty string if name not found.'''
        sect = section if section else self.__defaultSection
        return self._config.get(sect, name)

    def getInt(self, name, section=None) -> int:
        '''Returns an individual setting in the given section.

        Args:
            name (str): setting name.
            section (str): section of the setting. If None: defaultSection
        Returns:
            int: int value of setting. 0 if name not found.'''
        sect = section if section else self.__defaultSection
        return int(float(self._config.get(sect, name)))

    def getFloat(self, name, section=None) -> float:
        '''Returns an individual setting in the given section.

        Args:
            name (str): setting name.
            section (str): section of the setting. If None: defaultSection
        Returns:
            float: float value of setting. 0.0 if name not found.'''
        sect = section if section else self.__defaultSection
        return float(self._config.get(sect, name))

    def getBool(self, name, section=None) -> bool:
        '''Returns an individual setting in the given section.

        Args:
            name (str): setting name.
            section (str): section of the setting. If None: defaultSection
        Returns:
            bool: True or False.'''
        sect = section if section else self.__defaultSection
        val = self._config.get(sect, name)
        return True if val == 'True' else False

    def getList(self, name, section=None) -> list:
        '''Returns a list inside an individual setting in the given section.

        Args:
            name (str): setting name.
            section (str): section of the setting. If None: defaultSection
        Returns:
            list: list of values.'''
        sect = section if section else self.__defaultSection
        return self._config.get(sect, name).split(',')

    def setSetting(self, name, value, section=None):
        '''Updates a setting in the given section, creates it if missing.
        Note that this does not update the file physically,
        call update() for that.

        Args:
            name (str): Setting name.
            value (str): The value associated with the name.
            section (str): section of setting. If None: defaultSection'''
        sect = section if section else self.__defaultSection
        self._config.set(sect, name, str(value))

    def setSettingList(self, name, value, section=None):
        '''Updates a setting with a list in the given section,
        creates it if missing. Note that this does not update the file
        physically, call update() for that.

        Args:
            name (str): Setting name.
            value (list): The list associated with the name.
            section (str): section of setting. If None: defaultSection'''
        sect = section if section else self.__defaultSection
        value = ','.join(value)
        self._config.set(sect, name, str(value))

    def update(self):
        '''Dumps data into config file.'''
        with open(self._file_path, 'w') as configfile:
            self._config.write(configfile)

    def __createCongifFile(self):
        '''Creates a confing file with default values.'''
        # Populate config object
        # adding sections
        self._config.add_section('SETTINGS')
        self._config.add_section('UI')
        self._config.add_section('ASSETS')
        self._config.add_section('DATA')
        # Settings
        self.setSetting('airport_by_name', True)
        self.setSetting('auto_save', False)
        self.setSetting('first_airport', True)
        self.setSetting('disable_map', False)
        self.setSetting('currency', 'EUR')
        # UI
        self.setSetting('title', 'Fuel Management System', 'UI')
        self.setSetting('splash_time', '2.0', 'UI')
        tool_buttons = ['DATA ENTRY',
                        'ROUTE',
                        'LOAD',
                        'SAVE',
                        'PREFERENCES',
                        'ABOUT']
        self.setSettingList('tool_buttons', tool_buttons, 'UI')
        self.setSetting('calendar_label', 'Travel Week', 'UI')
        self.setSetting('system_message', 'Notice', 'UI')
        msg1 = 'Please fill the airports and click "ROUTE" to generate report.'
        msg2 = 'You can choose the "Static Path" option to Enter a straight ' \
            'path without analysis. In this case order of airports matters.'
        msg_map = 'You can improve responsiveness of the application ' \
            'greatly by disabling the map from preferences'
        msg_ap = 'Please note that the first airport should be in Ireland. ' \
            'You can disable this from preferences.'
        msg_incm = 'Please fill in the orange missing fields.'
        msg_invalid_ap = 'Please fill in valid data in the pink fields.'
        msg_not_unique = 'Please input unique airports in blue fields.'
        msg_week = 'Please select travel week from the calendar.'
        msg_invalid_week = 'Selected travel time already exists. Please ' \
            'select another week.'
        msg_no_redord = 'No record with the given travel time found. ' \
            'Please select another week'
        map_colors = ['dodgerblue', 'coral', 'aqua',
                      'limegreen', 'plum', 'tomato']
        self.setSetting('notice1', msg1, 'UI')
        self.setSetting('notice2', msg2, 'UI')
        self.setSetting('notice_map', msg_map, 'UI')
        self.setSetting('notice_airport', msg_ap, 'UI')
        self.setSetting('notice_incomplete', msg_incm, 'UI')
        self.setSetting('notice_invalid', msg_invalid_ap, 'UI')
        self.setSetting('notice_unique', msg_not_unique, 'UI')
        self.setSetting('notice_week', msg_week, 'UI')
        self.setSetting('invalid_week', msg_invalid_week, 'UI')
        self.setSetting('no_record', msg_no_redord, 'UI')
        airport_entry_tags = ['Airport Name', 'Code']
        self.setSettingList('airport_entry_tags', airport_entry_tags, 'UI')
        self.setSettingList('map_colors', map_colors, 'UI')
        # Assets
        self.setSetting('icon', r'./assets/logo_small.ico', 'ASSETS')
        self.setSetting('splash', r'./assets/splash.png', 'ASSETS')
        icons = [r'./assets/airp.png',
                 r'./assets/route.png',
                 r'./assets/load.png',
                 r'./assets/save.png',
                 r'./assets/pref.png',
                 r'./assets/about.png']
        self.setSettingList('tool_icons', icons, 'ASSETS')
        about_images = [r'./assets/about.gif',
                        r'./assets/about1.jpg',
                        r'./assets/about2.jpg',
                        r'./assets/about3.jpg']
        markers = [r'./assets/marker1.png',
                   r'./assets/marker2.png',
                   r'./assets/marker3.png',
                   r'./assets/marker4.png',
                   r'./assets/marker5.png',
                   r'./assets/marker6.png']
        self.setSettingList('about_images', about_images, 'ASSETS')
        self.setSettingList('markers', markers, 'ASSETS')
        # Data
        self.setSetting('aircrafts', r'./data/aircrafts.csv', 'DATA')
        self.setSetting('data', r'./data/traveldata.csv', 'DATA')
        self.setSetting('airports', r'./data/airports.csv', 'DATA')
        self.setSetting('currencies', r'./data/currencies.csv', 'DATA')
        self.setSetting('fuelprices', r'./data/fuelprice.csv', 'DATA')
        # Dump settings into config file
        self.update()


###############################################################################
def test():
    sett = Settings(file_path=r'./settings.ini')
    print('Section in '+sett._file_path+':'+str(sett.sections())+'\n')
    print('Section "SETTINGS":\n'+str(sett.getSection('SETTINGS'))+'\n')
    print('"auto_save" in "settings" section: '+sett.getStr('auto_save',
                                                            'SETTINGS'))

if __name__ == '__main__':
    test()

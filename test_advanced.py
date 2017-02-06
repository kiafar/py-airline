# -*- coding: utf-8 -*-
'''
Advanced unittest for fuel management app.
Initiates the application, sts up needed settings and runs some tests.
@since:04/05/2016
@author:Tirdad Kiafar
'''
import unittest
from ctrl.app import App


class AdvancedTestSuite(unittest.TestCase):
    '''Advanced test cases for Fuel Management app.
    Initiates the application, sets up needed settings and runs some tests.'''

    def setUp(self):
        '''Sets up requirements. Kicks off Application.'''
        self.app = App()


class TestFuelApplication(AdvancedTestSuite):
    '''Run advanced testing by setting needed variables inside application.'''
    def testInvalidHomeAirport(self):
        '''Tests:Empty fields, First airport home, Invalid input'''
        self.app._s.setSetting('first_airport', 'True')
        self.app._s.setSetting('airport_by_name', 'False')
        # empty fields test
        self.app._on_route()
        self.assertEqual(self.app._lbl_msg['text'],
                         self.app._s.getStr('notice_incomplete'), 'UI')
        # first airport not home test
        code = ['JFK',
                'IKA',
                'DUB',
                'SYD',
                'MHR']
        i = 0
        for ent in self.app._frm_airports._entries:
            ent.delete(0, 'end')
            ent.insert(0, code[i])
            i += 1
        self.app._ent_aircraft.delete(0, 'end')
        self.app._ent_aircraft.insert(0, 'Airbus A321')
        self.app._on_route()
        self.assertEqual(self.app._lbl_msg['text'],
                         self.app._s.getStr('notice_airport', 'UI'))
        # invalid input test
        self.app._s.setSetting('first_airport', 'False')
        ent = self.app._frm_airports._entries[1]
        ent.delete(0, 'end')
        ent.insert(0, 'Nonsense')
        self.assertEqual(self.app._lbl_msg['text'],
                         self.app._s.getStr('notice_unique', 'UI'))


if __name__ == '__main__':
    unittest.main()

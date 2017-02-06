#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Fuel Management Software Main Module.
@since:28/04/2016
@author:Tirdad Kiafar
'''
from ctrl.app import App
import os
if os.name == 'nt':
    import ctypes
myappid = 'tkiafar.fuelmanagement.1.0.0'


def main():
    # Create Application main controller which extends root tkinter object.
    root = App()
    # trying to register app window on taskbar on windows
    if os.name == 'nt':
        # SetCurrentProcessExplicitAppUserModelID function:
        # Specifies a unique application-defined Application User Model ID
        # (AppUserModelID) that identifies the current process to the taskbar.
        # This identifier allows an application to group its associated
        # processes and windows under a single taskbar button.
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # Entering Mainloop
    root.mainloop()

if __name__ == '__main__':
    main()

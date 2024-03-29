#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SplashScreen is an elegant tkinter splash screen.
From:
http://code.activestate.com/recipes/576936/
@author:Ronald Longo
"""
import time
import tkinter as tk
__version__ = '2.00'


class SplashScreen:
    '''Hides the root window and shows a splashscreen.'''
    def __init__(self, root, file, wait):
        '''Constructor.
        usage: with SplashScreen(master, filepath, min_wait_time):
        
        Args:
            root (tkinter.Tk): master window
            file (str): path to splash image file
            wait (float): minimum seconds to show spash.
                if "with" operation takes longer,the splash will remain
                untill "with" quits'''
        self.__root = root
        self.__file = file
        self.__wait = wait + time.clock()

    def __enter__(self):
        # Hide the root while it is built.
        self.__root.withdraw()
        # Create components of splash screen.
        window = tk.Toplevel(self.__root)
        canvas = tk.Canvas(window)
        splash = tk.PhotoImage(master=window, file=self.__file)
        # Get the screen's width and height.
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        # Get the images's width and height.
        imgW = splash.width()
        imgH = splash.height()
        # Compute positioning for splash screen.
        Xpos = (scrW - imgW) // 2
        Ypos = (scrH - imgH) // 2
        # Configure the window showing the logo.
        window.overrideredirect(True)
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        # Setup canvas on which image is drawn.
        canvas.configure(width=imgW, height=imgH, highlightthickness=0)
        canvas.grid()
        # Show the splash screen on the monitor.
        canvas.create_image(imgW // 2, imgH // 2, image=splash)
        window.update()
        # Save the variables for later cleanup.
        self.__window = window
        self.__canvas = canvas
        self.__splash = splash

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure that required time has passed.
        now = time.clock()
        if now < self.__wait:
            time.sleep(self.__wait - now)
        # Free used resources in reverse order.
        del self.__splash
        self.__canvas.destroy()
        self.__window.destroy()
        # Give control back to the root program.
        self.__root.update_idletasks()
        self.__root.deiconify()


def test():
    # running test
    root = tk.Tk()
    with SplashScreen(root, r'../assets/splash.png', 3.0):
        time.sleep(4)
    root.mainloop()

if __name__ == '__main__':
    test()
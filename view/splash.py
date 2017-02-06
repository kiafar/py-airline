#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Splash module generates custom splash screens with animated gifs.
Aimed at providing modern splash/about/tips screens.
@since:26/03/2016
@author:Tirdad Kiafar
"""
import tkinter as tk
from PIL import Image, ImageTk
import functools
__version__ = '160327'


###############################################################################
class Splash:
    '''A toplevel tk window that contains an animated gif'''
    def __init__(self, root, frames, duration=25, **kwargs):
        '''Cunstructor, initiates borderless window and sets up a gif playback.

        Args:
            root (tkinter.TK): Master tkinter window.
            frames (ImageTk.PhotoImage): Frames of animated gif.
            duration (Optional[int]): Duration of each frame in milisec.

        Keyword Args:
            alpha (float): Transparency of splash window, between 0 and 1.
            ontop (bool): If True window will stay on top of ther windows.
        '''
        self._root = root
        self.__frames = frames
        self.__duration = duration
        self.__index = 0
        # Creating components of splash
        window = tk.Toplevel(self._root)
        label = tk.Label(window)
        # Getting the screen dimentions
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        # Get the image dimentions
        imgW = self.__frames[0].width()
        imgH = self.__frames[0].height()
        # Calculate positioning for splash window
        Xpos = (scrW - imgW) // 2
        Ypos = (scrH - imgH) // 2
        # Configure the window
        window.overrideredirect(True)
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        # Setup label that contains images
        # removing label border for pure images
        label.configure(width=imgW, height=imgH,
                        borderwidth=0, highlightthickness=0)
        label.pack()
        # Save the variables for animation use
        self._label = label
        self._window = window
        # getting extra attributes from kwargs
        alpha = kwargs.get('alpha', 1)
        ontop = kwargs.get('ontop', False)
        # setting optional attributes
        if ontop is True:
            self._window.wm_attributes("-topmost", 1)
        self._window.attributes("-alpha", alpha)
        # triger the animation
        self.__animate()

    def __animate(self):
        '''Handles animation for frames'''
        # get the new image from stackS
        img = self.__frames[self.__index]
        # put the image inside the label
        self._label.config(image=img)
        self.__index += 1
        self.__index = self.__index % len(self.__frames)
        # set a delayed callback for next frame
        self._label.after(self.__duration, self.__animate)

    @property
    def window(self):
        '''The toplevel window of the class.'''
        return self._window

    def destroy(self):
        '''Remove the window and free the resources for garbage collector.'''
        self._window.destroy()


###############################################################################
class SplashComplex(Splash):
    '''
    Extends splash functionality with extra graphics. for usage see the test
    function at the end of source module.
    '''
    def __init__(self, root, frames, duration=25, **kwargs):
        '''
        Constructor

        **kwargs:
            header (ImageTk.PhotoImage): Header graphics. sticks to top middle.
            footer (List[ImageTk.Image]): Footer graphics that sticks to bottom
                middle edge.
            footer_delay (int): Delay of changing footer graphics in milisec.
        '''
        super().__init__(root, frames, duration, **kwargs)
        # getting extra graphics from kwargs
        self._footer_delay = kwargs.get('footer_delay', 4000)
        self.__header = kwargs.get('header', None)
        self.__footer = kwargs.get('footer', None)
        # setting up extra images if available
        if self.__header:
            self.__head_label = tk.Label(self._window)
            self.__head_label.config(image=self.__header)
            self.__head_label.place(relx=.5, anchor='n')
            self.__head_label.configure(borderwidth=0, highlightthickness=0)
        if self.__footer:
            self.__foot_label = tk.Label(self._window)
            self.__foot_idx = 0
            img = ImageTk.PhotoImage(self.__footer[self.__foot_idx])
            self.__foot_label.config(image=img)
            self.__foot_label.image = img
            self.__foot_label.place(relx=.5, rely=1, anchor='s')
            self.__foot_label.configure(borderwidth=0, highlightthickness=0)
            # setting up cycling between footer graphics
            self.__foot_label.after(self._footer_delay, self.__animateFooter)

    def __animateFooter(self):
        self.__foot_idx += 1
        self.__foot_idx %= len(self.__footer)
        self.__foot_label.after(self._footer_delay, self.__animateFooter)
        self.__footer_blend = 0
        self.__footer_fade()

    def __footer_fade(self):
        if self.__footer_blend < 1:
            img1 = self.__footer[self.__foot_idx-1]
            img2 = self.__footer[self.__foot_idx]
            self.__footer_blend += .15
            # python float inaccuracy could be problematic here
            if self.__footer_blend > 1:
                self.__footer_blend = 1
            newImg = Image.blend(img1, img2, self.__footer_blend)
            newImg = ImageTk.PhotoImage(newImg)
            self.__foot_label.config(image=newImg)
            self.__foot_label.image = newImg
            self._window.after(16, self.__footer_fade)


########################################################################
def showSplash(master, images) -> SplashComplex:
    '''Constructs a splash screen.

    Args:
        omages (list): list of paths, first is background,
            second is header, the rest are footer.
    Returns:
        SplashComplex: splash window.'''
    if len(images) < 2:
        raise Exception('"images" must have at least 2 children')
    img = Image.open(images[0])
    # extract frames from animated gif
    imgSequence = []
    try:
        while True:
            imgSequence.append(img.copy())
            img.seek(len(imgSequence))  # seek to next frame
    except EOFError:
        pass  # stack us empty, sequence is dumped
    # try to read gif duration if present
    try:
        duration = img.info['duration']
    except KeyError:
        duration = 25
    # building frames of images, first need to make first frame-
    # initialize an image instance for operations
    firstImage = imgSequence[0].convert('RGBA')
    frames = [ImageTk.PhotoImage(firstImage)]
    # add the remaining images
    imageData = imgSequence[0]
    for image in imgSequence[1:]:
        imageData.paste(image)
        frame = imageData.convert('RGBA')
        frames.append(ImageTk.PhotoImage(frame))
    # add header image
    header = Image.open(images[1])
    header = ImageTk.PhotoImage(header)
    # add footer images
    footer = []
    for i in range(2, len(images)):
        footer_image = Image.open(images[i])
        footer.append(footer_image)
    window = SplashComplex(master, frames, duration, alpha=.85, ontop=True,
                           header=header, footer=footer, footer_delay=4500)
    # put window on top
    window.window.attributes("-topmost", True)
    return window

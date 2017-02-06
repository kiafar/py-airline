#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Map Module provides map rendering with extra functionalities.
@since:28/03/2016
@author:Tirdad Kiafar
"""
from mpl_toolkits.basemap import Basemap
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import tkinter as tk
from tkinter import ttk
# for loading the pictures
from PIL import Image
# for drawing pictures on map (our custom markers in this case)
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import datetime


class Map(ttk.Frame):
    '''A ttk frame of world map with lots of functionalities.'''
    def __init__(self, master=None, **kwargs):
        '''Constructor. Adds basemap to the frame.

        Args:
            master (tkinter.Widget): tkinter master container

        Keyword Args:
            fig_background (str): figure background. e.g. "white"
            callback (function): a callback function for clicking.
                must have two arguments (lat, lon)'''
        # initialize super class
        ttk.Frame.__init__(self, master)
        # add figure to wrap map
        figure = Figure(figsize=(10, 5))
        # add map container
        self._axes = figure.add_subplot(111, frameon=False)
        # create basemap object
        self._map = Basemap(projection='cyl',
                            llcrnrlat=-90,
                            urcrnrlat=90,
                            llcrnrlon=-180,
                            urcrnrlon=180,
                            resolution='c',
                            ax=self._axes)
        # draw line around conties
        self._map.drawcountries(linewidth=0.3)
        # draw coast lines
        coasts = self._map.drawcoastlines(zorder=1, color='white', linewidth=0)
        # remove rivers
        coasts_paths = coasts.get_paths()
        ipolygons = range(90)
        for ipoly in range(len(coasts_paths)):
            r = coasts_paths[ipoly]
            # Convert into lon/lat vertices
            polygon_vertices = [(vertex[0], vertex[1]) for (vertex, code) in
                                r.iter_segments(simplify=False)]
            px = [polygon_vertices[i][0] for i in range(len(polygon_vertices))]
            py = [polygon_vertices[i][1] for i in range(len(polygon_vertices))]
            if ipoly in ipolygons:
                self._map.plot(px, py, linewidth=.3, zorder=3, color='black')
        # draw meridians and parallels on map
        self.__drawAxes()
        # add canvas to the
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        # add click callback to canvas
        self._callback = kwargs.get('callback')
        figure.canvas.callbacks.connect('button_press_event', self._on_click)
        # make the sub plot take as much space as possible
        figure.tight_layout()
        # set background color if present, else set transparent
        if kwargs.get('fig_background'):
            figure.patch.set_facecolor(kwargs.get('fig_background'))
        else:
            figure.patch.set_alpha(0.0)  # transparent figure background
        # showing canvas
        self.canvas.show()
        # placing canvas
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                         fill=tk.BOTH,
                                         expand=1)
        self._artist = None

    def _on_click(self, event):
        if event.inaxes is not None:
            if self._callback is not None:
                self._callback(event.ydata, event.xdata)

    def __drawAxes(self):
        '''Draws meridians and parallels on map, in both self._axes.'''
        self._map.drawmeridians(np.arange(30, 331, 30), linewidth=0.3,)
        self._map.drawparallels(np.arange(-60, 61, 30), linewidth=0.3)

    def draw_geodesic(self, point1, point2, linewidth=2, color='b'):
        '''draw geodesic route between two points.

        Args:
            point1 (tuple): latitude, longitude
            point2 (tuple): latitude, longitude'''
        lat1, lon1 = point1
        lat2, lon2 = point2
        self._map.drawgreatcircle(lon1, lat1,
                                  lon2, lat2,
                                  linewidth=linewidth,
                                  color=color)

    def draw_marker(self, markerImage, point):
        '''draw marker image on specific point of map.

        Args:
            markerImage (image): PIL image file of marker. use Image.open
            point (tuple): (latitude, longitude) of insertion point.'''
        lon, lat = point
        # drawing picture on map
        imheight = markerImage.size[1]
        marker = np.array(markerImage)
        im = OffsetImage(marker, zoom=1)
        ab = AnnotationBbox(im,
                            (lat, lon+imheight/4),
                            xycoords='data',
                            frameon=False)
        self._artist = ab
        self._axes.add_artist(ab)

    def shadeNight(self, alpha=.1, dtime=None):
        '''Shades night on map based on a given datetime.

        Args:
            alpha (float): shading opacity. from 0 to 1.
            dtime (datetime): specific date/time to shade map.'''
        self._map.nightshade(dtime if dtime else datetime.utcnow(),
                             alpha=alpha)

    def clean_canvas(self):
        '''Unfortunately I could not clear canvas, so this functions says if
        something is drawn on map. then we dispose map and create another'''
        if self._artist is not None:
            return False
        return True

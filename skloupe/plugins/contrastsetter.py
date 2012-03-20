import matplotlib.pyplot as plt
from skimage.filter import canny
from skimage.util.dtype import dtype_range
from skimage.exposure import histogram

import numpy as np

from .base import Plugin
from ..widgets.slider import Slider


__all__ = ['ContrastSetter']


class ContrastSetter(Plugin):
    """Plugin to manualy adjust the contrast of an image.
    Ony linear adjustment are possible. Source image is not modified.

    Parameters
    ----------
    image_window : ImageViewer instance.
        Window containing image used in measurement.
    
    """

    def __init__(self, image_window):

        figure, axes = plt.subplots(nrows=3, figsize=(6, 1))
        ax_histo, ax_low, ax_high = axes
        self.ax_histo = ax_histo
        Plugin.__init__(self, image_window, figure=figure)
        
        hmin, hmax = dtype_range[self.image.dtype.type]
        if hmax > 255:
            bins = int(hmax - hmin)
        else:
            bins = 256
        print bins
        
        self.hist, self.bin_centers = histogram(self.image.data, bins)
        low_value, high_value = self.bin_centers[[0, -1]]
        clip = low_value, high_value

        self.slider_high = Slider(ax_high, clip, label='Maximum',
                                  value=high_value, on_release=self.update_image)
        self.slider_low = Slider(ax_low, clip, label='Minimum',
                                  value=low_value, on_release=self.update_image)

        self.connect_event('key_press_event', self.on_key_press)
        self.connect_event('scroll_event', self.on_scroll)

        self.original_image = self.imgview.image.copy()
        self.update_image()
        self.redraw()
        
        print self.help

    @property
    def help(self):
        helpstr = ("ContrastSetter plugin\n"
                   "---------------------\n"
                   "+ and - keys or mouse scroll\n"
                   "also change the contrast\n")
        return helpstr
        
    @property
    def low(self):
        return self.slider_low.value
    
    @property
    def high(self):
        return self.slider_high.value

    def update_image(self, event = None):
        self.draw_colorbar()
        self.draw_histogram()
        self.imgview.image = self.original_image.clip(self.low, self.high)
        self.imgview.redraw()
        self.redraw()


    def draw_histogram(self):
        hist_lines = self.ax_histo.step(self.bin_centers, self.hist, 
                                        color = 'k', alpha = 0.5)
    def draw_colorbar(self):
        self.colorbar = np.linspace(self.low, self.high,
                                    256).reshape((1,256))
        extent = (self.low, self.high,
                  self.ax_histo.axis()[2], self.ax_histo.axis()[3])
        self.ax_histo.imshow(self.colorbar, aspect = 'auto',
                             extent = extent)

    def reset(self):
        self.slider_high.value = self.bin_centers
        low_value, high_value = self.bin_centers[[0, -1]]
        self.update_image()

    def _expand_bonds(self, event):
        if not event.inaxes: return
        center = (self.high + self.low) / 2.
        span = self.high - self.low
        low = min(self.slider_low.value - span / 20.,
                  self.slider.valmin)
        high = max(self.slider_high.value + span / 20.,
                   self.slider_high.valmax)
        

    def _restrict_bonds(self, event):
        if not event.inaxes: return
        center = (self.high + self.low) / 2.
        span = self.high - self.low
        low = min(self.slider_low.value + span / 20.,
                  self.slider._high.value - span / 20.)
        high = max(self.slider_high.value - span / 20.,
                   self.slider_low.value + span / 20.)
        
    def on_scroll(self, event):
        if not event.inaxes: return
        if event.button == 'up':
            self._expand_bonds()
        elif event.button == 'down':
            self._restrict_bonds()

    def on_key_press(self, event):
        if not event.inaxes: return
        elif event.key == '+':
            self._expand_bonds()
        elif event.key == '-':
            self._restrict_bonds()
        elif event.key == 'r':
            self.reset()

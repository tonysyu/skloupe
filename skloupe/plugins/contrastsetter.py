import matplotlib.pyplot as plt
from skimage.util.dtype import dtype_range
from skimage.exposure import histogram
from numpy import linspace, zeros, ones

from .base import Plugin
from ..widgets.slider import Slider


__all__ = ['ContrastSetter']


class ContrastSetter(Plugin):
    """Plugin to manualy adjust the contrast of an image.
    Ony linear adjustments are possible. Source image is not modified.

    Parameters
    ----------
    image_window : ImageViewer instance.
        Window containing image used in measurement.

    """

    def __init__(self, image_window):
        figure = plt.figure(figsize=(6.5, 2))
        ax_hist = plt.subplot2grid((6, 1), (0, 0), rowspan=4)
        ax_low = plt.subplot2grid((6, 1), (4, 0), rowspan=1)
        ax_high = plt.subplot2grid((6, 1), (5, 0), rowspan=1)
        self.ax_hist = ax_hist

        Plugin.__init__(self, image_window, figure=figure)

        hmin, hmax = dtype_range[self.image.dtype.type]
        if hmax > 255:
            bins = int(hmax - hmin)
        else:
            bins = 256
        self.hist, self.bin_centers = histogram(self.image.data, bins)
        low_value, high_value = self.bin_centers[[0, -1]]
        clip = low_value, high_value

        ax_hist.step(self.bin_centers, self.hist, color='r', lw=2, alpha=1.)
        self.ax_hist.set_xlim(low_value, high_value)
        self.ax_hist.set_xticks([])
        self.ax_hist.set_yticks([])

        self.slider_high = Slider(ax_high, clip, label='Max',
                                  value=high_value,
                                  on_release=self.update_image)
        self.slider_low = Slider(ax_low, clip, label='Min',
                                 value=low_value,
                                 on_release=self.update_image)
        self.slider_low.slidermax = self.slider_high
        self.slider_high.slidermin = self.slider_low

        self.connect_event('key_press_event', self.on_key_press)
        self.connect_event('scroll_event', self.on_scroll)
        self.original_image = self.imgview.image.copy()
        self.update_image()
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

    def update_image(self, event=None):
        self.draw_colorbar()
        self.imgview.climits = (self.low, self.high)
        self.imgview.redraw()
        self.redraw()

    def draw_colorbar(self):
        colorbar = linspace(self.low, self.high,
                            256).reshape((1,256))
        cbar_extent = (self.low,
                       self.high,
                       self.ax_hist.axis()[2],
                       self.ax_hist.axis()[3])
        black_rectangle = zeros((1,2))
        black_extent = (self.ax_hist.axis()[0],
                        self.low,
                        self.ax_hist.axis()[2],
                        self.ax_hist.axis()[3])
        white_rectangle = ones((1,2)) * self.bin_centers[-1]
        white_extent = (self.high,
                        self.ax_hist.axis()[1],
                        self.ax_hist.axis()[2],
                        self.ax_hist.axis()[3])
        if len(self.ax_hist.images) > 2:
            del self.ax_hist.images[-3:]
        self.ax_hist.imshow(black_rectangle, aspect='auto',
                             extent=black_extent)
        self.ax_hist.imshow(white_rectangle, aspect='auto',
                             extent=white_extent,
                             vmin=self.bin_centers[0],
                             vmax=self.bin_centers[-1])
        self.ax_hist.imshow(colorbar, aspect='auto',
                             extent=cbar_extent)

    def reset(self):
        low, high = self.bin_centers[[0, -1]]
        self.slider_low.value = low
        self.slider_high.value = high
        self.update_image()

    def _expand_bonds(self, event):
        if not event.inaxes: return
        span = self.high - self.low
        low = max(self.slider_low.value - span / 20.,
                  self.slider_low.valmin)
        high = min(self.slider_high.value + span / 20.,
                   self.slider_high.valmax)
        self.slider_low.value = low
        self.slider_high.value = high
        self.update_image()

    def _restrict_bonds(self, event):
        if not event.inaxes: return
        span = self.high - self.low
        low = self.slider_low.value + span / 20.
        high = self.slider_high.value - span / 20.
        self.slider_low.value = low
        self.slider_high.value = high
        self.update_image()

    def on_scroll(self, event):
        if not event.inaxes: return
        if event.button == 'up':
            self._expand_bonds(event)
        elif event.button == 'down':
            self._restrict_bonds(event)

    def on_key_press(self, event):
        if not event.inaxes: return
        elif event.key == '+':
            self._expand_bonds(event)
        elif event.key == '-':
            self._restrict_bonds(event)
        elif event.key == 'r':
            self.reset()

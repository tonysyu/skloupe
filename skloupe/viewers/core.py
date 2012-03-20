"""
Basic viewers for viewing images and image collections.
"""
import matplotlib.pyplot as plt

from ..utils import figimage
from ..widgets.slider import Slider


__all__ = ['imshow', 'ImageViewer', 'CollectionViewer']


class ImageViewer(object):
    """Window for displaying images.

    This window is a simple container object that holds a Matplotlib axes
    for showing images. This doesn't subclass the Matplotlib axes (or figure)
    because there be dragons.
    """

    def __init__(self, image, **kwargs):
        self._image = image.copy()
        self.fig, self.ax = figimage(image, **kwargs)
        self.ax.autoscale(enable=False)

        self.canvas = self.fig.canvas
        if len(self.ax.images) > 0:
            self._imgplot = self.ax.images[0]
            self._img = self._imgplot.get_array()
        else:
            raise ValueError("No image found in figure")

        self.ax.format_coord = self._format_coord

        self._axes_artists = [self.ax.artists,
                              self.ax.collections,
                              self.ax.images,
                              self.ax.lines,
                              self.ax.patches,
                              self.ax.texts]

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self.ax.images[0].set_array(image)

    def connect_event(self, event, callback):
        cid = self.canvas.mpl_connect(event, callback)
        return cid

    def disconnect_event(self, callback_id):
        self.canvas.mpl_disconnect(callback_id)

    def add_artist(self, artist):
        self.ax.add_artist(artist)

    def remove_artist(self, artist):
        """Disconnect all artists created by this widget."""
        # There's probably a smarter way to do this.
        for artist_list in self._axes_artists:
            if artist in artist_list:
                artist_list.remove(artist)

    def redraw(self):
        self.canvas.draw_idle()

    def _format_coord(self, x, y):
        # callback function to format coordinate display in toolbar
        x = int(x + 0.5)
        y = int(y + 0.5)
        try:
            return "%s @ [%4i, %4i]" % (self.image[y, x], x, y)
        except IndexError:
            return ""

    def show(self):
        plt.show()


class CollectionViewer(ImageViewer):

    def __init__(self, image_collection, **kwargs):
        self.image_collection = image_collection
        self.index = 0
        self.num_images = len(self.image_collection)

        first_image = image_collection[0]
        ImageViewer.__init__(self, first_image, **kwargs)

        h_old = self.fig.get_figheight()
        h_new = h_old + 0.5
        self.fig.set_figheight(h_new)
        self.ax.set_position([0, 1 - h_old/h_new, 1, h_old/h_new])
        ax_slider = self.fig.add_axes([0.1, 0, 0.8, 0.5 / h_new])
        idx_range = (0, self.num_images-1)
        self.slider = Slider(ax_slider, idx_range, on_slide=self.update_image,
                             value=0, value_fmt='%i')
        self.connect_event('key_press_event', self.on_keypressed)

    def set_image(self, image):
        self.image = image
        self.fig.canvas.draw()

    def update_image(self, index):
        index = int(round(index))

        if index == self.index:
            return

        # clip index value to collection limits
        index = max(index, 0)
        index = min(index, self.num_images-1)

        self.index = index
        self.slider.value = index
        self.set_image(self.image_collection[index])

    def on_keypressed(self, event):
        key = event.key
        if str(key) in '0123456789':
            index = 0.1 * int(key) * self.num_images
            self.update_image(index)
        elif key == 'right':
            self.update_image(self.index + 1)
        elif key == 'left':
            self.update_image(self.index - 1)
        elif key == 'end':
            self.update_image(self.num_images - 1)
        elif key == 'home':
            self.update_image(0)


def imshow(image, **kwargs):
    """Return ImageViewer for input image.

    Keyword arguments are passed on to Matplotlib's `imshow` function
    """
    image_window = ImageViewer(image, **kwargs)
    return image_window


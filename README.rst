==========================
Image viewer for `skimage`
==========================

`skloupe` provides an image viewing interface based on matplotlib_ and is
closely affiliated with skimage_. The name is a combination of SciKits_
(toolkits for scientific python) and "loupe_" (a magnifying glass used to look
at images).

Some of the functionality for viewing image collection was borrowed from
Christoph Gohlke's TIFFFile_ imshow.


Requirements
============

* numpy_
* matplotlib_
* skimage_


Installation from source
========================

`skloupe` may be installed globally using::

   $ git clone git@github.com:tonysyu/skloupe.git
   $ cd skloupe
   $ python setup.py install

or locally using::

   $ python setup.py install --prefix=${HOME}

If you prefer, you can use it without installing, by adding the parent
directory of this file to your `python path`.


Known Issues
============

- When using matplotlib with the Qt4Agg backend, plugins don't call the
  `close_event` correctly [1]_, and so the widget will not get cleaned up.
- `CollectionViewer` is incorrectly sized on the Qt4Agg backend because
  of a resizing bug in Matplotlib [2]_.


.. [1] https://github.com/matplotlib/matplotlib/pull/716
.. [2] https://github.com/matplotlib/matplotlib/pull/756


.. _numpy: http://numpy.scipy.org/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _skimage: http://scikits-image.org/
.. _SciKits: http://scikits.appspot.com/
.. _loupe: http://en.wikipedia.org/wiki/Loupe
.. _TIFFFile: http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html
.. _python path: http://stackoverflow.com/a/302261/260303


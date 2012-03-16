=============================
Contribute to `scikits-loupe`
=============================

It's easy to contribute to `scikits-loupe`; just fork the project on github::

    $ git clone git@github.com:tonysyu/skloupe.git

For the most part, we'll follow the same `development workflow`_ as numpy. So
after you've cloned the repos, just make some changes to the code (preferably
to a branch_) and the submit a `pull request`_. Also, we'll try to follow the
`numpy documentation standard`_.


Organization
============

`scikits-loupe` is organized into the following subpackages:

utils
   Basic utilities shared by other subpackages.
widgets
   Basic interactive tools used to interact with viewers. For example a slider
   widget to adjust the value of a parameter.
viewers
   Image and image collection viewers.
plugins
   Tools that can be attached to a viewer for image analysis and manipulation.
   For example, a tool to adjust the contrast of an image.

The order of this list is important: a subpackage can import from any
subpackage preceding it in this list, but not those after it. For example,
a function in `viewers` can use functions in `utils` and `widgets` but not in
`plugins`.


Todo
====

- Add interface (menu?) for connecting a Plugin to an ImageWindow.
- Add check for image collections in `imshow` and divert to `CollectionViewer`.
- Add `CompareViewer` for comparing two images side-by-side.


Open Questions
==============

- Is `ImageViewer.show` the best way to start the mainloop or would a normal
  function be better?
- Rename `CollectionViewer` to `StackViewer`?


.. _development workflow:
   http://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html
.. _branch:
   http://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html#making-a-new-feature-branch
.. _pull request:
   http://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html#asking-for-merging
.. _numpy documentation standard:
   https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


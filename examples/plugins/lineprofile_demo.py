from skimage import data
from skloupe.viewers import ImageViewer
from skloupe.plugins import LineProfile

image = data.camera()
# Note: Widget must be assigned to a variable so it isn't garbage collected
# Maybe LineProfile should save a reference of itself in ImageWindow
# and then clear itself when closed.
view = ImageViewer(image)
lp = LineProfile(view, limits='dtype')
view.show()


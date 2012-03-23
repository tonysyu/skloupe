from skimage import data
from skloupe.viewers import ImageViewer
from skloupe.plugins import LineProfile

image = data.camera()
view = ImageViewer(image)
LineProfile(view, limits='dtype')
view.show()


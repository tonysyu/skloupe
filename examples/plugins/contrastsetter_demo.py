from skimage import data
from skloupe.viewers import ImageViewer
from skloupe.plugins import ContrastSetter

image = data.coins()
view = ImageViewer(image)
ContrastSetter(view)
view.show()

import skimage
from skimage import data
from skloupe.viewers import ImageViewer
from skloupe.plugins import EdgeDetector

image = skimage.img_as_float(data.camera())
view = ImageViewer(image)
ed = EdgeDetector(view)
view.show()


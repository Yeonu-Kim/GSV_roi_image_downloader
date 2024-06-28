import asyncio
from streetview.download import get_panorama
from streetview.util import crop_bottom_and_right_black_border

image = get_panorama("UNqHEyVqW31ghtcio_OLrA", multi_threaded=True)
cropped_image = crop_bottom_and_right_black_border(image)

cropped_image.save('image.jpg', "jpeg")

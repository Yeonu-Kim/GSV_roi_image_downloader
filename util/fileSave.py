import numpy as np
import PIL
from PIL import Image

def saveImg(image: PIL.ImageFile, idx: int, turn: int):
    image.save(f"./output/image/{turn}/GSV_{idx}.jpeg")

def saveMask(imgArray: np.array, idx: int, turn: int):
    imgArray = imgArray*255
    image = Image.fromarray(imgArray.astype(np.uint8))
    image.save(f"./output/mask/{turn}/Mask_{idx}.png")
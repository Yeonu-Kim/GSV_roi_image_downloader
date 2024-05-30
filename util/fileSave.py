import numpy as np
import PIL
from PIL import Image

def saveImg(image: PIL.ImageFile, pano_id:str, turn: int, path: str):
    image.save(f"{path}/{pano_id}_{turn}.jpeg")

def saveMask(imgArray: np.array, idx: int, turn: int, path: str):
    imgArray = imgArray*255
    image = Image.fromarray(imgArray.astype(np.uint8))
    image.save(f"{path}/mask/{turn}/Mask_{idx}.png")
import numpy as np
import PIL
from PIL import Image
from config import CONFIG

def saveImg(image: PIL.ImageFile, pano_id:str):
    image.save(f"{CONFIG.SAVE_DIR}/{pano_id}.jpeg")

def saveMask(imgArray: np.array, idx: int, turn: int):
    imgArray = imgArray*255
    image = Image.fromarray(imgArray.astype(np.uint8))
    image.save(f"{CONFIG.SAVE_DIR}/mask/{turn}/Mask_{idx}.png")
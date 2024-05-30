import requests
import sys, os
from PIL import Image
import json
import io
import numpy as np
import matplotlib.pyplot as plt
import skimage

sys.path.append(os.pardir)

def loadImg(lat:float, lon:float, APIkey:str, fov:int, directionNum:int, turn: int):
    heading = 360/directionNum*turn
    url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&location={lat},{lon}&fov={fov}&heading={heading}&return_error_code=true&key={APIkey}"

    response = requests.get(url)
    status = response.status_code

    bytes_data = response.content
    image = Image.open(io.BytesIO(bytes_data)) if status == 200 else None
        
    return status, image

def loadLocalImg(path:str):
    imageOriginal = skimage.io.imread(path)
    image = skimage.transform.resize(imageOriginal, (320, 1024))
    image = image[:, :, :3]
    image = skimage.img_as_ubyte(image)
    return image

def loadMetadata(lat:float, lon:float, APIkey:str):
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lon}&return_error_code=true&key={APIkey}"

    response = requests.get(url)
    status = response.status_code
    # print(response.status_code)
    # print(response.json())

    return response.json()
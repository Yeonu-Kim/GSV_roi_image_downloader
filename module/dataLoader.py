import requests
import sys, os
from PIL import Image
import json
import io
import numpy as np
import matplotlib.pyplot as plt
import skimage
import hashlib
import hmac
import base64
import urllib.parse as urlparse
from config import CONFIG

sys.path.append(os.pardir)

def signUrl(input_url=None, secret=None):
    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()

def loadImg(lat:float, lon:float, turn: int):
    heading = 360/CONFIG.DIRECTION_NUM*turn
    unsignedUrl = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&location={lat},{lon}&fov={CONFIG.FOV}&heading={heading}&return_error_code=true&key={CONFIG.API_KEY}"
    url = signUrl(unsignedUrl, CONFIG.SIGNATURE)

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

def loadMetadata(lat:float, lon:float):
    unsignedUrl = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lon}&return_error_code=true&key={CONFIG.API_KEY}"
    url = signUrl(unsignedUrl, CONFIG.SIGNATURE)
    response = requests.get(url)
    status = response.status_code
    # print(status)
    # print(response.status_code)
    # print(response.json())

    return status, response.json()
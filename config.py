import json

# Load secret data from .secret folder
with open(".secret/common.json", "r") as f:
    secretData = json.load(f)

class CONFIG:
    HOME_DIR = r"/home/ywk0524/GSV_image_download"
    SAVE_DIR = r"/home/ywk0524/GSV_image_download/output"

    API_KEY = secretData['API_KEY']

    FOV = 120
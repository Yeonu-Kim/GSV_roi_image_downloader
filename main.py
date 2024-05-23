import os
import numpy as np
import pandas as pd
import json
import csv
from config import CONFIG
from module.dataLoader import loadImg
from util.visualize import showHist, showImg
from util.fileSave import saveImg, saveMask
from skyDetector.predict import predictSkyRatio
from module.pointGenerator import pointListGen

# Check path
# os.chdir(CONFIG.HOME_DIR)

def makeResult(turn):
    # Make lat and lon list using config
    pointList = pointListGen(CONFIG.BASE_POINT_LIST)
    dataLen = len(pointList)

    # Make dataframe using pandas
    data = {
        'lat': [],
        'lon': [],
        'sky_ratio': []
    }
    df = pd.DataFrame(data)

    # Load GSV images and depthmap
    for idx, point in enumerate(pointList):
        lat = point[0]
        lon = point[1]
        print(f"이미지 분석 중... {idx+1}/{dataLen}")

        # Load an image from GSV API
        status, image = loadImg(lat, lon, CONFIG.API_KEY, CONFIG.FOV, turn)
        if status == 200:
            # showImg(image)
            # Calculate sky ratio of the image
            skyRatio, mask = predictSkyRatio(image)
            # Save GSV images and mask results every 500*nth time
            if idx % 500 == 0:
                saveImg(image, idx, turn)
                saveMask(mask, idx, turn)
            print(f"천공률: {skyRatio}")
            # Add data to pandas dataframe
            df.loc[len(df.index)] = [lat, lon, skyRatio]

    df.to_csv(f"./sky_ratio_result_{turn}.csv", na_rep='Unknown')

for idx in range(1, 3):
    makeResult(idx)



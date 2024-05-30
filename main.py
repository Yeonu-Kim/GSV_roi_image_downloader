import os
from tqdm import tqdm
import numpy as np
import pandas as pd
import json
import csv
from config import CONFIG
from module.dataLoader import loadImg, loadMetadata
from util.visualize import showHist, showImg
from util.fileSave import saveImg, saveMask
from util.validator import isAlreadyDownloaded
from module.pointGenerator import pointListGen

# Check path
# os.chdir(CONFIG.HOME_DIR)

def makeResult():
    # Make lat and lon list using config
    pointList = pointListGen()

    # Make dataframe using pandas
    metaIndex = {}
    metaDf = pd.DataFrame(columns=['lat', 'lon', 'panoId', 'date'])

    # Load GSV images and depthmap
    for idx, point in enumerate(tqdm(pointList)):
        lat = point[0]
        lon = point[1]
        # print(f"lat: {lat}, lon: {lon}")

        # Load an image from GSV API
        metadataResponse = loadMetadata(lat, lon, CONFIG.API_KEY)
        if metadataResponse['status'] == 'OK':
            lat = metadataResponse['location']['lat']
            lon = metadataResponse['location']['lng']
            panoId = metadataResponse['pano_id']
            date = metadataResponse['date']

            panoIdList = list(metaDf['panoId'])

            # Check the data is already downloaded
            if isAlreadyDownloaded(panoId, panoIdList):
                continue
            # print(f"lat: {lat}, lon: {lon}, panoId: {panoId}, date: {date}")
            metaDf.loc[len(metaDf)] = [lat, lon, panoId, date]
            for turn in range(CONFIG.DIRECTION_NUM):
                status, image = loadImg(lat, lon, CONFIG.API_KEY, CONFIG.FOV, CONFIG.DIRECTION_NUM, turn)
                if status == 200:
                    # showImg(image)
                    saveImg(image, metadataResponse['pano_id'], turn, CONFIG.SAVE_DIR)
        # if idx == 5:
        #     break

    metaDf.to_csv(f"{CONFIG.SAVE_DIR}/metadata/metadata.csv", na_rep='Unknown')

if __name__ == "__main__":
    makeResult()
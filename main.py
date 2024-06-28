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
import logging
from time import sleep
import traceback
from streetview.streetview.download import get_panorama
from streetview.streetview.util import crop_bottom_and_right_black_border

# Check path
# os.chdir(CONFIG.HOME_DIR)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def loadMetadata():
    pointList = pointListGen()
    metaDf = pd.DataFrame(columns=['lat', 'lon', 'panoId', 'date'])

    for idx, point in enumerate(tqdm(pointList)):
        lat, lon = point
        retries = 10  # Number of retries for connection errors

        while retries > 0:
            try:
                status, metadataResponse = loadMetadata(lat, lon)
                if status == 200:
                    lat = metadataResponse['location']['lat']
                    lon = metadataResponse['location']['lng']
                    panoId = metadataResponse['pano_id']
                    date = metadataResponse['date']

                    if panoId not in metaDf['panoId'].values:
                        metaDf.loc[len(metaDf)] = [lat, lon, panoId, date]

                break  # Exit retry loop if successful

            except KeyError as e:
                break  # Skip to the next point

            except ConnectionError as e:
                logging.error(f"ConnectionError: {e}")
                retries -= 1
                if retries > 0:
                    logging.info("Retrying after connection error...")
                    sleep(5)  # Wait before retrying
                else:
                    logging.error("Max retries exceeded. Moving to the next point.")
                    break

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                logging.error(traceback.format_exc())
                break  # Skip to the next point

    metadata_path = os.path.join(CONFIG.SAVE_DIR, "metadata", "metadata.csv")
    metaDf.to_csv(metadata_path, na_rep='Unknown')
    logging.info(f"Metadata saved to {metadata_path}")

# 3784 + 6534 + 8460 + 9668 + 11196 + 69907 + 10587 = 57226
def loadImage():
    metaDf = pd.read_csv('./output/metadata/valid_points.csv').dropna()
    pointList = np.array(metaDf.loc[:, 'panoId'])

    for idx, point in enumerate(tqdm(pointList[57226:77226])):
        panoId = point
        retries = 10  # Number of retries for connection errors

        while retries > 0:
            try:
                image = get_panorama(panoId, multi_threaded=True)
                cropped_image = crop_bottom_and_right_black_border(image)
                saveImg(cropped_image, panoId)
                break  # Exit retry loop if successful

            except KeyError as e:
                break  # Skip to the next point

            except ConnectionError as e:
                logging.error(f"ConnectionError: {e}")
                retries -= 1
                if retries > 0:
                    logging.info("Retrying after connection error...")
                    sleep(5)  # Wait before retrying
                else:
                    logging.error("Max retries exceeded. Moving to the next point.")
                    break

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                logging.error(traceback.format_exc())
                break  # Skip to the next point

if __name__ == "__main__":
    # loadMetadata()
    loadImage()

# GSV_roi_data_downloader

## Download GSV images of my roi by fixed interval


### How to use?

#### 1. Set "config.py" file to suit your purpose

You can set below elements in config file.

```
# Basic Setting
API KEY : Please write your GSV API key. If you want to control it under gitignore environment, you can make ".secret/common.json" and write your API_KEY.
HOME_DIR: Directory name of your root dir
OUTPUT_DIR: Directory name of your output dir

# GSV image Setting
FOV : fov of your images
DIRECTION_NUM : How many times do you want to get a picture per one location

# GSV metadata Setting


```

<br />

#### 2. Download coordinate CSV file from Google Earth Engine

If you can check you roi in "Unique_ADM2_NAMES.csv" file, please copy the "gee_auto.js" to you GEE console.

If you cannot find your roi in the above file, please copy the "gee_manually.js" to you GEE console.

In manual version, you have to make polygon(roi) using GEE.

You can download the csv file to your Google Drive.


<br/>

#### 3. Upload coordinate CSV file to "data" directory

You have to upload you csv file to data directory.

After that, please run the main.py. You can get a images to "OUTPUT_DIR" directory and metadata would be saved at "OUTPUT_DIR/metadata.csv".

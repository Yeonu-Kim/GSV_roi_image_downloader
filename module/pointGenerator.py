import os
import numpy as np
import pandas as pd

def getPointData(coor_df: pd.DataFrame) -> np.array:
    newPoint = np.stack((np.array(coor_df['lat']), np.array(coor_df['lon'])), axis=1)
    return newPoint

def pointListGen() -> np.array:
    pointList = np.array([])
    with os.scandir('./data') as fileList:
        for targetFile in fileList:
            coorDf = pd.read_csv(targetFile)
            newPoint = getPointData(coorDf)
            pointList = np.append(pointList, newPoint)
    
    pointList = pointList.reshape(-1, 2)

    return pointList
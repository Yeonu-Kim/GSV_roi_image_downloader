import numpy as np

def pointListGen(basePointList: list):
    pointList = np.array([[]])

    for idx, basePoint in enumerate(basePointList):
        lat_left, lat_right, lon_down, lon_up = basePoint

        latList = np.arange(lat_left, lat_right, 0.001)
        lonList = np.arange(lon_down, lon_up, 0.001)

        latGrid, lonGrid = np.meshgrid(latList, lonList)
        # Flatten 2d array to 1d array
        latGrid = latGrid.ravel()
        lonGrid = lonGrid.ravel()

        # Make grid coordinates
        pointListParts = np.column_stack([latGrid.T, lonGrid.T])
        if idx == 0:
            pointList = pointListParts
        else:
            pointList = np.block([[pointList], [pointListParts]])

    return pointList
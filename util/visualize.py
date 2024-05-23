import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

def showHist(data:np.array):
    plt.hist(data)
    plt.show()

def showImg(img:bytes):
    plt.imshow(img)
    plt.show()
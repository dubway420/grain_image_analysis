# import required packages
import numpy as np
from skimage import io, color, measure
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt
import pandas as pd

# define functions:
## sub-functions:
### label_grains: identifies and labels grains in image
def label_grains(image_file):
    # read file, open as image and slightly crop
    image = io.imread(image_file)
    cropby = 10 # crops image by a set number of pixels in all directions to tidy up straggling boundaries
    image = image[cropby:np.shape(image)[0]-cropby,cropby:np.shape(image)[1]-cropby]
    
    # convert image to grayscale
    grayim = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # convert grayscale to black and white image
    (thresh, bwim) = cv2.threshold(grayim, np.max(grayim)-5, np.max(grayim), cv2.THRESH_BINARY)

    # label each individual grain
    s = np.array([[0, 1, 0],[1, 1, 1],[0, 1, 0]])
    labeled_mask, num_labels = ndimage.label(bwim, structure=s)
    
    return labeled_mask, bwim

colorlist = ['rosybrown','firebrick','tomato','lightsalmon','chocolate','sandybrown','burlywood','goldenrod','lemonchiffon','lightgreen','darkseagreen','mediumseagreen','lightseagreen','steelblue','royalblue','mediumpurple','mediumorchid','lightpink']

### sumProduct: a function for calculting the sum product
def sumProduct(list1, list2):
    return sum(map(lambda x, y: x * y, list1, list2))

## main functions: 
### grain_list: 2 outputs (a list of grain areas and diameters, an average area-weighted mean and std)
def grain_list(image_file,pix_len,sca_len):
    # obtained labeled image and dilated image data
    labeled_mask, bwim = label_grains(image_file)
    
    # obtained coloured image of labeled grains
    labeled_image = color.label2rgb(labeled_mask, bg_label=0, colors=colorlist)
    
    # identify each grain and measure their properties (units = pixels)
    clusters = measure.regionprops(labeled_mask, bwim)
    
    # calculate conversion between pixels and unit of scalebar
    conv = sca_len/pix_len
    
    # append array with each grain's area and equivalent diameter (i.e., the diameter assuming the grain face is a 2d circle)
    areas, eqdia = [], []
    for prop in clusters:
        area = prop.area*conv
        areas.append(round(area,2))
        dia = ((4*prop.area*conv)/np.pi)**(1/2)
        eqdia.append(round(dia,2))
        
    mean = sumProduct(eqdia,areas)/sum(areas) # calculate area-weighted mean for equivalent circle diameter of grains
    std = (sumProduct([(val - mean)**2 for val in eqdia],areas)/((sum(areas)*(len(areas)-1))/(len(areas))))**(1/2) # calc std of area-weighted mean
    
    plt.figure(figsize=(12,12))
    io.imshow(labeled_image) # print image of labeled grains
    plt.title('Area-weighted mean equivalent circle diameter = '+str(round(mean,1))+' ± '+str(round(std,1)), fontsize=18)
    
    return pd.DataFrame({'Area':areas,'EqDia':eqdia}), [round(mean,1), round(std,2)] # output list of grain areas and diameters, output mean + std

### Gd: a conversion of grain diameter in microns to ASTM grain size
def Gd(d): 
    l = ((math.pi/4)*(d**2))**(1/2)
    return -3.2877-(6.6439*math.log10(l*10**(-3)))

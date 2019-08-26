# lungs-finder

##### Library for lungs detection on CXR images

![](https://user-images.githubusercontent.com/11778655/27996147-765dfba8-64e4-11e7-81ca-9ea25b5d072d.png)

## Requirements:
- Python 3;
- OpenCV3.


## Installation:
`git clone git@github.com:Miffka/lungs-finder.git`
`cd lungs-finder && pip3 install -e .`


```
You can test your dataset using lungs_viewer.py.
It is a program that is displayed on the screenshot above.
Usage: lungs_viewer.py /your/dataset True
The last parameter defines whether labels will be displayed or not.
```

## Usage

### Function `get_lungs`

```
import cv2
import lungs_finder as lf

image = cv2.imread(YOUR_PNG_IMAGE_PATH, 0)
image = cv2.equalizeHist(image)
image = cv2.medianBlur(image, 3)
image = cv2.resize(image, (512, 512)) # resize to small scale is crucial

# Returns lungs (as is with padding)
found_lungs = lf.get_lungs(image, padding=20)

# Returns lung coordinates (x, y, width, height)
x, y, width, height = lf.get_lungs(image, padding=20, return_image=False)

# Tries to find square with lungs
found_lungs_square = lf.get_lungs(image, padding=20, square=True)

# Returns coordinates of square with lungs
x_sq, y_sq, width_sq, height_sq = lf.get_lungs(image, padding=20, square=True, return_image=False)

fig, ax = plt.subplots(1, 2, figsize=(10,10))

if found_lungs is not None:
    ax[0].imshow(found_lungs, cmap=mpl.cm.gray)
if found_lungs_square is not None:
    ax[1].imshow(found_lungs_square, cmap=mpl.cm.gray)
```

### Visualize HOG, HAAR, LBP methods of finding lungs

```
from itertools import product
import os
import os.path as osp
import cv2

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import lungs_finder as lf

def show_lungs(img_path, resize=512):
    image = cv2.imread(img_path, 0)
    image = cv2.equalizeHist(image)
    image = cv2.medianBlur(image, 3)
    image = cv2.resize(image, (resize, resize))
    found_lungs = lf.get_lungs(image, padding=20)
    found_lungs_square = lf.get_lungs(image, padding=20, square=True)

    fig, ax = plt.subplots(1,3, figsize=(15, 5))
    ax[0].imshow(image, cmap=mpl.cm.gray)
    ax[1].imshow(cv2.resize(found_lungs, (resize, resize)), cmap=mpl.cm.gray)
    ax[2].imshow(cv2.resize(found_lungs_square, (resize, resize)), cmap=mpl.cm.gray)


    for (side, method), color in zip(product(['right', 'left'],
                                             ['hog', 'lbp', 'haar']),
                                     ['yellow', 'red', 'blue']*2):
        out = eval(f'lf.find_{side}_lung_{method}')(image)
        if out is not None:
            x, y, width, height = out
            rect = Rectangle((x, y), width, height, fill=False, edgecolor=color)
            ax[0].add_patch(rect)

    fig.suptitle(osp.basename(img_path))
    plt.show();

for i, file in enumerate(os.listdir(osp.join(PATH_TO_YOUR_PNG_FILES))):
    show_lungs(osp.join(PATH_TO_YOUR_PNG_FILES, file), resize=512)
    if i > 50:
        break
```

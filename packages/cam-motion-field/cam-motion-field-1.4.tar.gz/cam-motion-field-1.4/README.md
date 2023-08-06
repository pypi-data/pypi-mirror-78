# Cam_motion_field

### Description
This package provides quick and easy way to compute camera motion field given
two consecutive images.

### Install
```
pip install cam-motion-field
```
 
### Usage
```python
from cam_motion_field import get_cam_flow
import cv2
image1_file = "PATH/TO/THE/FIRST/IMAGE/FILE"
image2_file = "PATH/TO/THE/SECOND/IMAGE/FILE"
ncol = 10
nrow = 10
grid_size = (ncol, nrow)

img1 = cv2.imread(image1_file, 0)
img2 = cv2.imread(image2_file, 0)
# origins.shape = (10,10,2)
# displacements.shape = (10,10,2)
origins, displacements = get_cam_flow(img1, img2, grid_size[0], grid_size[1])
```
The above example defines a 10x10 grid and returns 100 origins and
displacement points. Both origins and displacements are absolute coordinates!

######  Parameters:
    Parameters
    ----------
    image1 : numpy array
        image1 a grayscale image
    image2 : numpy array
        image2 a grayscale image
    n_rows : int
        number of rows in the grid
    n_cols : int
        number of columns in the grid

## Example
Examples where generated using the example.py. This gif shows two images where either the camera moved forward or some zoom effect took place

<img src="https://github.com/stamas02/cam_motion_field/blob/master/data/image_anim.gif" width="400"/>

The resuts are:
5x5 Grid

<img src="https://github.com/stamas02/cam_motion_field/blob/master/data/motion_filed_5x5.jpg" width="400"/>

10x10 Grid

<img src="https://github.com/stamas02/cam_motion_field/blob/master/data/motion_filed_10x10.jpg" width="400"/>

20x20 Grid

<img src="https://github.com/stamas02/cam_motion_field/blob/master/data/motion_filed_20x20.jpg" width="400"/>


Notice that 20x20 has many zero displacements. This happens when the grid is too fine and no good features are detected
in the cell. 

import numpy as np
from .optical_flow import get_displacements
import cv2

_k_params = dict(
    winSize=(15, 15),
    maxLevel=4,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)

_feature_params = dict(maxCorners=1000000, qualityLevel=0.1, minDistance=7, blockSize=7)

def get_cam_flow(image1, image2, n_rows, n_cols, k_params=_k_params, feature_params=_feature_params):
    """ Calculate an optical flow for each image block defined by grid.

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
    k_params: dictionary, Optional
        cv2.calcOpticalFlowPyrLK parameters. For more information visit
        https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html
    _feature_params: dictionary, Optional
        cv2.goodFeaturesToTrack parameter. for more information please visit
        https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html


    Return
    ------
        A numpy array of shape (n_rows, n_cols, 2) where each image block is assigned with
        an 2D vector representing its average displacement.
    """
    # Get image blocks
    origins, displacements = get_displacements(image1, image2, k_params, feature_params)

    h, w = image1.shape
    row_pixel_indexes = np.linspace(0, h, n_rows + 1, dtype=np.int)
    col_pixel_indexes = np.linspace(0, w, n_cols + 1, dtype=np.int)
    block_dispalcements = []
    block_origins = []

    # Going through all the grid cells
    for y0, y1 in zip(row_pixel_indexes, row_pixel_indexes[1::]):
        for x0, x1 in zip(col_pixel_indexes, col_pixel_indexes[1::]):
            cx = x0 + (x1 - x0) // 2
            cy = y0 + (y1 - y0) // 2
            # search for those origins within the current grid cell
            idx = np.where((origins[:, 0] > x0) & (origins[:, 0] <= x1) & (origins[:, 1] > y0) & (origins[:, 1] <= y1))[
                0]
            if len(idx) == 0:  # if no origin was found assign a zero displacement
                block_dispalcement = np.array([cx, cy])
            else:
                block_dispalcement = np.mean((displacements[idx] - origins[idx]) + np.array([cx, cy]), axis=0,
                                             dtype=np.int)
            block_dispalcements.append(block_dispalcement)
            block_origins.append(np.array([cx, cy]))

    block_dispalcements = np.array(block_dispalcements).reshape(n_rows, n_cols, 2).astype(np.int)
    block_origins = np.array(block_origins).reshape(n_rows, n_cols, 2).astype(np.int)

    return block_origins, block_dispalcements

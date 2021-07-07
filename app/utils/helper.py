from typing import Dict, Union, List

import numpy as np


def normalize_coordinates(coords: np.array, original_image: np.array) -> List[Union[float, int]]:
    """ Normalizes coordinate values from pixels to values between 0 and 1

    :param coords: array of coordinates where values are alternating between x and y:
                   [left, top, right, bottom]
    :param original_image: array of image data
    """
    original_image_size = list(reversed(original_image.shape[:2]))
    return [c / original_image_size[i % 2] for i, c in enumerate(coords)]


def create_bounding_box(left, top, right, bottom) -> Dict[str, Union[float, int]]:
    """ Creates a dict for storing a bounding box in the database
    """
    return dict(l=left, t=top, r=right, b=bottom)

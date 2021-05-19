def normalize_coordinates(coords, original_image):
    """ Normalizes coordinate values from pixels to values between 0 and 1

    :param coords: array of coordinates where values are alternating between x and y
    :param original_image:
    """
    original_image_size = list(reversed(original_image.shape[:2]))
    return [c / original_image_size[i % 2] for i, c in enumerate(coords)]

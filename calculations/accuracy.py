import numpy as np


def compare(predicted_data, real_data):
    """Compare predicted image with real image.

    Args:
        predicted_data: numpy array, int32 - [height, width].
            Array of the prediction.
        real_data: numpy array, int32 - [height, width].
            Array of the real.

    Returns:
        result: float32.
            Similarity of the images.
    """
    height, width = predicted_data.shape[:2]

    match_pixels = (predicted_data == real_data).flatten()
    result = match_pixels[match_pixels]
    result = 100.0 * result.shape[0] / (height * width)
    return result

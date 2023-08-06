import numpy as np
import scipy.optimize as optimize


def _z_translation_fn(data, parameter, focal_length=150):
    x = data[:, 0]
    y = data[:, 1]
    f = focal_length
    new_data = np.array(data)
    new_data[:, 0] = x + f * (np.arctan(x / f)) * (1 + (x ** 2 / f ** 2)) * parameter
    new_data[:, 1] = y + f * (np.arctan(y / f)) * (1 + (y ** 2 / f ** 2)) * parameter

    return new_data.flatten()


def estimate_z_transition(origins, displacements, focal_length=150):
    """  Estimate the amount of camera transition on the z axis based on optical flow.

    Note: both the origin and displacement vectors must be centered prior to calling this method.
    This means that a hypothetical origin at the center of the image must have the coordinate: (0,0).

    Parameters
    ----------
    origins: numpy array,
        Set of origin vectors. Shape must be (nr_of_points, 2). MUST BE ZERO CENTERED AND SCALED!
    displacements: numpy array,
        Set of displacement vectors (coordinates). Shape must be (nr_of_points, 2)
    focal_length: int,
        the focal length of the camera which took the images.

    Returns
    -------
        - The estimated amount of transition on the z axis of the camera.
    """

    func = lambda data, parameter: _z_translation_fn(data, parameter, focal_length)

    param, pcov = optimize.curve_fit(func, origins, displacements.flatten())
    return param[0]

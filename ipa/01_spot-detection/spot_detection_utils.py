from scipy.ndimage import gaussian_filter
from skimage.util import img_as_float32, img_as_uint
from skimage.measure import centroid
from scipy.optimize import curve_fit

import numpy as np


def get_spot(img, coords, size=21):
    half_size = size // 2

    assert 0 <= coords[0] - half_size, "Spot is too close to image boundary."
    assert 0 <= coords[1] - half_size, "Spot is too close to image boundary."
    assert coords[0] + half_size < img.shape[0], "Spot is too close to image boundary."
    assert coords[1] + half_size < img.shape[1], "Spot is too close to image boundary."
    
    start_y = coords[0] - half_size
    start_x = coords[1] - half_size
    return img[start_y: start_y + size, start_x: start_x + size], start_y, start_x


def gauss_2d(bg, amp, mu_x, mu_y, sig_x, sig_y):
    def fun(coords):
        return amp * np.exp(
            -0.5 * ( 
            ( (coords[:, 1] - mu_x)**2 )/( sig_x**2 ) + 
            ( (coords[:, 0] - mu_y)**2 )/( sig_y**2 )
            )
        ) + bg
    
    return fun


def eval_gauss_2d(x, bg, amp, mu_x, mu_y, sig_x, sig_y):
    return gauss_2d(bg=bg, amp=amp, mu_x=mu_x, mu_y=mu_y, sig_x=sig_x, sig_y=sig_y)(x)


def subpixel_localization_2d(spot_img, spacing):
    init_params = [
        spot_img.min(), 
        spot_img.max(), 
        spot_img.shape[1]/2 * spacing[1], 
        spot_img.shape[0]/2 * spacing[0],
        1,
        1
    ]

    yy = np.arange(spot_img.shape[0]) * spacing[0] 
    xx = np.arange(spot_img.shape[1]) * spacing[1]
    y, x = np.meshgrid(yy, xx, indexing="ij")
    coords_yx = np.stack([y.ravel(), x.ravel()], -1)

    bounds = [
            (0, init_params[1] * 0.5, init_params[2] - 3 * spacing[1], init_params[3] - 3 * spacing[0], -3, -3),
            (init_params[0] * 2, init_params[1] * 2, init_params[2] + 3 * spacing[1], init_params[3] + 3 * spacing[0], 3, 3),
        ]
    
    popt, pcov = curve_fit(
        eval_gauss_2d,
        coords_yx,
        spot_img.ravel(),
        p0=init_params,
        bounds=bounds
    )

    return popt
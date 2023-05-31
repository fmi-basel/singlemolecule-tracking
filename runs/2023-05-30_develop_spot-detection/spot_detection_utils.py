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


def get_cov_matrix(img):
    def cov(x, y, i):
        return np.sum(x * y * i) / np.sum(i)

    extends = [np.arange(dim_size) for dim_size in img.shape]

    grids = np.meshgrid(
        *extends,
        indexing="ij",
    )
    cen = centroid(img)
    y = grids[0].ravel() - cen[0] 
    x = grids[1].ravel() - cen[1] 

    cxx = cov(x, x, img.ravel())
    cyy = cov(y, y, img.ravel())
    cxy = cov(x, y, img.ravel())

    return np.array([[cxx, cxy], [cxy, cyy]])


def gauss_2d(amp, mu_x, mu_y, cxx, cxy, cyy):
    def fun(coords):
        cov_inv = np.linalg.inv(np.array([[cxx, cxy], [cxy, cyy]]))
        exponent = -0.5 * (
            cov_inv[0, 0] * (coords[:, 1] - mu_x) ** 2
            + 2 * cov_inv[0, 1] * (coords[:, 1] - mu_x) * (coords[:, 0] - mu_y)
            + cov_inv[1, 1] * (coords[:, 0] - mu_y) ** 2
        )

        return amp * np.exp(exponent)

    return fun

def gauss_2d_eval_fun(x, amp, mu_x, mu_y, cxx, cxy, cyy):
    return gauss_2d(amp=amp, mu_x=mu_x, mu_y=mu_y, cxx=cxx, cxy=cxy, cyy=cyy)(x)


def subpixel_localization(spot_img):
    cov = get_cov_matrix(spot_img)
    init_params = [spot_img.max(), spot_img.shape[1]//2, spot_img.shape[0]//2, cov[0,0], cov[0, 1], cov[1, 1]]

    yy = np.arange(spot_img.shape[0]) 
    xx = np.arange(spot_img.shape[1]) 
    y, x = np.meshgrid(yy, xx, indexing="ij")
    coords_yx = np.stack([y.ravel(), x.ravel()], -1)

    popt, pcov = curve_fit(
        gauss_2d_eval_fun,
        coords_yx,
        spot_img.ravel(),
        p0=init_params,
        bounds=[
            (0, init_params[1] - 3, init_params[2] - 3, init_params[3] * 0.5, -np.inf, init_params[5] * 0.5),
            (init_params[0] * 2, init_params[1] + 3, init_params[2] + 3, init_params[3] * 1.5, np.inf, init_params[5] * 1.5),
        ]
    )

    return popt[2], popt[1]

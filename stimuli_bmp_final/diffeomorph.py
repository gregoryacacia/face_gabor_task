#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy.ndimage import map_coordinates
def diffeomorph_face(img, max_offset=50, iterations=3, aggressive=False):
    """
    Method from:
    Stojanoski, B., & Cusack, R. (2014). Time to wave good-bye to phase
    scrambling: Creating controlled scrambled images using diffeomorphic
    transformations. Journal of Vision, 14(12), 6. doi:10.1167/14.12.6
    """
    def _diffeo_morpher(size, max_distort, iterations=6):
        [yi, xi] = np.meshgrid(range(size), range(size))
        ph = np.random.random((iterations, iterations, 4)) * 2 * np.pi
        a = np.random.random((iterations, iterations)) * 2 * np.pi
        xn = np.zeros(size)
        yn = np.zeros(size)
        for xc in range(iterations):
            for yc in range(iterations):
                ac = a[xc, yc]
                cos_xc = np.cos(xc * xi / size * 2 * np.pi + ph[xc, yc, 0])
                cos_yc = np.cos(yc * yi / size * 2 * np.pi + ph[xc, yc, 1])
                xn = xn + ac * cos_xc * cos_yc
                cos_xc = np.cos(xc * xi / size * 2 * np.pi + ph[xc, yc, 2])
                cos_yc = np.cos(yc * yi / size * 2 * np.pi + ph[xc, yc, 3])
                yn = yn + ac * cos_xc * cos_yc
        xn /= np.mean(xn ** 2) ** 0.5
        yn /= np.mean(yn ** 2) ** 0.5
        return max_distort * xn, max_distort * yn
    size = img.shape[0]
    [yi, xi] = np.meshgrid(range(size), range(size))
    cx, cy = _diffeo_morpher(img.shape[0], max_offset, iterations)
    if aggressive:
        cx2, cy2 = _diffeo_morpher(img.shape[0], max_offset, iterations)
        cx = cx2 - cx
        cy = cy2 - cy
    cx += xi
    cy += yi
    return map_coordinates(img, [cx.ravel(), cy.ravel()], order=3,
                           mode='nearest').reshape(cx.shape)
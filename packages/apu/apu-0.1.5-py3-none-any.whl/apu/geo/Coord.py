""" coordination transformation """

from typing import List, Tuple
import numpy as np

def m2pix(height: float,
          extention: float,
          radius: float,# = 6_378_137 ,
          distorsion_scaling: float = 1.) -> float:
    """ convert from meter in pixel

    Arguments:
        height(float): image height
        extention(float): latitude extention of image in pixel
        radius(float): planet radius in metern
        distorsion_scaling(float): Scaling factor for
                                  distortion between 0. and 1.

    Returns:
        float: conversionsfactor pix/m
    """

    return (180. / np.pi) * height * \
            distorsion_scaling / extention / radius

def km2pix(height: float,
           extention: float,
           radius: float = 6_378.137,
           distorsion_scaling: float = 1.) -> float:
    """ convert from kilometer in pixel

    Arguments:
        height(float): image height
        extention(float): latitude extention of image in pixel
        radius(float): planet radius in kilometer default is
                       the earth radius (6_378.137km)
        distorsion_scaling(float): Scaling factor for
                                  distortion between 0. and 1.

    Returns:
        float: conversionsfactor pix/m
    """

    assert 0.0 < distorsion_scaling <= 1.0, \
        f"apu.geo.Coord: distorsion_scaling {distorsion_scaling} has to" +\
         " be in the interval ]0,1]"

    return m2pix(height=height,
                 extention=extention,
                 radius=radius*1000.0,
                 distorsion_scaling=distorsion_scaling) / 1000.0

def pix2carree(pixel: List[float],
               area: List[Tuple[float]],
               image_size: List[int],
               origin: str = "upper") -> tuple:
    """ Convert image pixel position to Carree lat/long
        ASSAMTION: central median is 0 => (long [-180,180[)

    Arguments:
        pixel(List[float]): (u,v) coordinate in image
        area(List[Tuple[float]]): ((u,v)_min, (u,v)_max) the area in the image
                    to search in
        image_size(List[int]): image size in width and height
        origin(str): image convention. where is the image origin.
                'upper' means the origin [0,0] is in the upper left corner
                'lower' means that the image origin is in the lower left corner

    Returns:
        tuple: (lat, lon) coordinates in a Plate Carree image
    """

    lat = (pixel[0] / image_size[0]) * (area[1][0] - area[0][0]) + area[0][0]
    lon = (pixel[1] / image_size[1]) * (area[1][1] - area[0][1])
    lon = lon + area[0][1] if origin == "lower" else area[0][1] - lon

    return (lat, lon)

# pylint: disable=C0103
def carree2pix(coord: List[float],
               area: List[Tuple[float]],
               image_size: List[int],
               origin: str = "upper") -> tuple:
    """ Convert Carree lat/long to image poxel position

    Arguments:
        coord(List[float]): (lat, lon) coordinate in image
        area(List[Tuple[float]]): ((u,v)_min, (u,v)_max) the area in the image
                    to search in
        image_size(List[int]): image size in width and height
        origin(str): image convention. where is the image origin.
                'upper' means the origin [0,0] is in the upper left corner
                'lower' means that the image origin is in the lower left corner

    Returns:
        tuple: (u, v) pixel coordinate
    """

    u = image_size[0] * (coord[0] - area[0][0]) / (area[1][0] - area[0][0])
    v = image_size[1] / (area[1][1] - area[0][1])
    v = v * (coord[1] - area[0][1]) if origin == "lower" else \
        v * (area[1][1] - coord[1])

    return (u, v)

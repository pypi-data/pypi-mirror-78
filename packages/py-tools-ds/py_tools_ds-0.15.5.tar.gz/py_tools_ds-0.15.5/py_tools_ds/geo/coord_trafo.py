# -*- coding: utf-8 -*-

# py_tools_ds
#
# Copyright (C) 2019  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import pyproj
import numpy as np
from shapely.ops import transform
from typing import Union  # noqa F401  # flake8 issue

try:
    from osgeo import osr
    from osgeo import gdal
except ImportError:
    import osr
    import gdal

__author__ = "Daniel Scheffler"


def transform_utm_to_wgs84(easting, northing, zone, south=False):
    """Transform an UTM coordinate to lon, lat, altitude."""
    UTM = pyproj.Proj(proj='utm', zone=abs(zone), ellps='WGS84', south=(zone < 0 or south))
    return UTM(easting, northing, inverse=True)


def get_utm_zone(longitude):
    """Get the UTM zone corresponding to the given longitude."""
    return int(1 + (longitude + 180.0) / 6.0)


def transform_wgs84_to_utm(lon, lat, zone=None):
    """ returns easting, northing, altitude. If zone is not set it is derived automatically.
    :param lon:
    :param lat:
    :param zone:
    """
    if not (-180. <= lon <= 180. and -90. <= lat <= 90.):
        raise ValueError((lon, lat), 'Input coordinates for transform_wgs84_to_utm() out of range.')

    UTM = pyproj.Proj(proj='utm', zone=get_utm_zone(lon) if zone is None else zone, ellps='WGS84')
    return UTM(lon, lat)


def transform_any_prj(prj_src, prj_tgt, x, y):
    """Transforms X/Y data from any source projection to any target projection.

    :param prj_src:     GDAL projection as WKT string or EPSG code ('epsg:1234' or <EPSG_int>)
    :param prj_tgt:     GDAL projection as WKT string or EPSG code ('epsg:1234' or <EPSG_int>)
    :param x:
    :param y:
    :return:
    """
    transformer = pyproj.Transformer.from_crs(pyproj.CRS.from_user_input(prj_src),
                                              pyproj.CRS.from_user_input(prj_tgt),
                                              always_xy=True)
    return transformer.transform(x, y)


def transform_coordArray(prj_src, prj_tgt, Xarr, Yarr, Zarr=None):
    """Transforms geolocation arrays from one projection into another.
    HINT: This function is faster than transform_any_prj but works only for geolocation arrays.

    :param prj_src:     WKT string
    :param prj_tgt:     WKT string
    :param Xarr:        np.ndarray of shape (rows,cols)
    :param Yarr:        np.ndarray of shape (rows,cols)
    :param Zarr:        np.ndarray of shape (rows,cols)
    :return:
    """
    drv = gdal.GetDriverByName('MEM')
    geoloc_ds = drv.Create('geoloc', Xarr.shape[1], Xarr.shape[0], 3, gdal.GDT_Float64)
    geoloc_ds.GetRasterBand(1).WriteArray(Xarr)
    geoloc_ds.GetRasterBand(2).WriteArray(Yarr)
    if Zarr is not None:
        geoloc_ds.GetRasterBand(3).WriteArray(Zarr)

    def strip_wkt(wkt):
        return wkt\
            .replace('\n', '')\
            .replace('\r', '')\
            .replace(' ', '')

    transformer = gdal.Transformer(None, None, ['SRC_SRS=' + strip_wkt(prj_src),
                                                'DST_SRS=' + strip_wkt(prj_tgt)])
    status = transformer.TransformGeolocations(geoloc_ds.GetRasterBand(1),
                                               geoloc_ds.GetRasterBand(2),
                                               geoloc_ds.GetRasterBand(3))

    if status:
        raise Exception('Error transforming coordinate array:  ' + gdal.GetLastErrorMsg())

    Xarr = geoloc_ds.GetRasterBand(1).ReadAsArray()
    Yarr = geoloc_ds.GetRasterBand(2).ReadAsArray()

    if Zarr is not None:
        Zarr = geoloc_ds.GetRasterBand(3).ReadAsArray()
        return Xarr, Yarr, Zarr
    else:
        return Xarr, Yarr


def mapXY2imXY(mapXY, gt):
    # type: (tuple, Union[list, tuple]) -> Union[tuple, np.ndarray]
    """Translates given geo coordinates into pixel locations according to the given image geotransform.

    :param mapXY:   <tuple, np.ndarray> The geo coordinates to be translated in the form (x,y) or as np.ndarray [Nx1].
    :param gt:      <list> GDAL geotransform
    :returns:       <tuple, np.ndarray> image coordinate tuple X/Y (column, row) or np.ndarray [Nx2]
    """
    if isinstance(mapXY, np.ndarray):
        if mapXY.ndim == 1:
            mapXY = mapXY.reshape(1, 2)
        assert mapXY.shape[1] == 2, 'An array in shape [Nx2] is needed. Got shape %s.' % mapXY.shape
        imXY = np.empty_like(mapXY)
        imXY[:, 0] = (mapXY[:, 0] - gt[0]) / gt[1]
        imXY[:, 1] = (mapXY[:, 1] - gt[3]) / gt[5]
        return imXY
    else:
        return (mapXY[0] - gt[0]) / gt[1], (mapXY[1] - gt[3]) / gt[5]


def imXY2mapXY(imXY, gt):
    # type: (tuple, Union[list, tuple]) -> Union[tuple, np.ndarray]
    """Translates given pixel locations into geo coordinates according to the given image geotransform.

    :param imXY:    <tuple, np.ndarray> The image coordinates to be translated in the form (x,y) or as np.ndarray [Nx1].
    :param gt:      <list> GDAL geotransform
    :returns:       <tuple, np.ndarray> geo coordinate tuple X/Y (mapX, mapY) or np.ndarray [Nx2]
    """
    if isinstance(imXY, np.ndarray):
        if imXY.ndim == 1:
            imXY = imXY.reshape(1, 2)
        assert imXY.shape[1] == 2, 'An array in shape [Nx2] is needed. Got shape %s.' % imXY.shape
        imXY = np.empty_like(imXY)
        imXY[:, 0] = gt[0] + imXY[:, 0] * abs(gt[1])
        imXY[:, 1] = gt[3] - imXY[:, 1] * abs(gt[5])
        return imXY
    else:
        return (gt[0] + imXY[0] * abs(gt[1])), (gt[3] - imXY[1] * abs(gt[5]))


def mapYX2imYX(mapYX, gt):
    return (mapYX[0] - gt[3]) / gt[5], (mapYX[1] - gt[0]) / gt[1]


def imYX2mapYX(imYX, gt):
    return gt[3] - (imYX[0] * abs(gt[5])), gt[0] + (imYX[1] * gt[1])


def pixelToMapYX(pixelCoords, path_im=None, geotransform=None, projection=None):
    assert path_im or geotransform and projection, \
        "pixelToMapYX: Missing argument! Please provide either 'path_im' or 'geotransform' AND 'projection'."
    if geotransform and projection:
        gt, proj = geotransform, projection
    else:
        ds = gdal.Open(path_im)
        gt, proj = ds.GetGeoTransform(), ds.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(proj)
    # Set up the coordinate transformation object
    ct = osr.CoordinateTransformation(srs, srs)

    mapYmapXPairs = []
    pixelCoords = [pixelCoords] if not type(pixelCoords[0]) in [list, tuple] else pixelCoords

    for point in pixelCoords:
        # Translate the pixel pairs into untranslated points
        u_mapX = point[0] * gt[1] + gt[0]
        u_mapY = point[1] * gt[5] + gt[3]
        # Transform the points to the space
        (mapX, mapY, holder) = ct.TransformPoint(u_mapX, u_mapY)
        # Add the point to our return array
        mapYmapXPairs.append([mapY, mapX])

    return mapYmapXPairs


def pixelToLatLon(pixelPairs, path_im=None, geotransform=None, projection=None):
    """The following method translates given pixel locations into latitude/longitude locations on a given GEOTIF
    This method does not take into account pixel size and assumes a high enough
    image resolution for pixel size to be insignificant

    :param pixelPairs:      Image coordinate pairs to be translated in the form [[x1,y1],[x2,y2]]
    :param path_im:         The file location of the input image
    :param geotransform:    GDAL GeoTransform
    :param projection:      GDAL Projection
    :returns:               The lat/lon translation of the pixel pairings in the form [[lat1,lon1],[lat2,lon2]]
    """
    assert path_im or geotransform and projection, \
        "GEOP.pixelToLatLon: Missing argument! Please provide either 'path_im' or 'geotransform' AND 'projection'."
    if geotransform and projection:
        gt, proj = geotransform, projection
    else:
        ds = gdal.Open(path_im)
        gt, proj = ds.GetGeoTransform(), ds.GetProjection()

    # Create a spatial reference object for the dataset
    srs = osr.SpatialReference()
    srs.ImportFromWkt(proj)
    # Set up the coordinate transformation object
    srsLatLong = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs, srsLatLong)
    # Go through all the point pairs and translate them to pixel pairings
    latLonPairs = []
    for point in pixelPairs:
        # Translate the pixel pairs into untranslated points
        ulon = point[0] * gt[1] + gt[0]
        ulat = point[1] * gt[5] + gt[3]
        # Transform the points to the space
        (lon, lat, holder) = ct.TransformPoint(ulon, ulat)
        # Add the point to our return array
        latLonPairs.append([lat, lon])

    return latLonPairs


def latLonToPixel(latLonPairs, path_im=None, geotransform=None, projection=None):
    """The following method translates given latitude/longitude pairs into pixel locations on a given GEOTIF
    This method does not take into account pixel size and assumes a high enough
    image resolution for pixel size to be insignificant

    :param latLonPairs:     The decimal lat/lon pairings to be translated in the form [[lat1,lon1],[lat2,lon2]]
    :param path_im:         The file location of the input image
    :param geotransform:    GDAL GeoTransform
    :param projection:      GDAL Projection
    :return:            The pixel translation of the lat/lon pairings in the form [[x1,y1],[x2,y2]]
    """
    assert path_im or geotransform and projection, \
        "GEOP.latLonToPixel: Missing argument! Please provide either 'path_im' or 'geotransform' AND 'projection'."
    if geotransform and projection:
        gt, proj = geotransform, projection
    else:
        ds = gdal.Open(path_im)
        gt, proj = ds.GetGeoTransform(), ds.GetProjection()
    # Load the image dataset
    # Create a spatial reference object for the dataset
    srs = osr.SpatialReference()
    srs.ImportFromWkt(proj)
    # Set up the coordinate transformation object
    srsLatLong = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srsLatLong, srs)
    # Go through all the point pairs and translate them to latitude/longitude pairings
    pixelPairs = []
    for point in latLonPairs:
        # Change the point locations into the GeoTransform space
        (point[1], point[0], holder) = ct.TransformPoint(point[1], point[0])
        # Translate the x and y coordinates into pixel values
        x = (point[1] - gt[0]) / gt[1]
        y = (point[0] - gt[3]) / gt[5]
        # Add the point to our return array
        pixelPairs.append([int(x), int(y)])
    return pixelPairs


def lonlat_to_pixel(lon, lat, inverse_geo_transform):
    """Translates the given lon, lat to the grid pixel coordinates in data array (zero start)"""
    # transform to utm
    utm_x, utm_y, utm_z = transform_wgs84_to_utm(lon, lat)
    # apply inverse geo tranform
    pixel_x, pixel_y = gdal.ApplyGeoTransform(inverse_geo_transform, utm_x, utm_y)
    pixel_x = int(pixel_x) - 1  # adjust to 0 start for array
    pixel_y = int(pixel_y) - 1  # adjust to 0 start for array
    return pixel_x, abs(pixel_y)  # y pixel is likly a negative value given geo_transform


def transform_GCPlist(gcpList, prj_src, prj_tgt):
    """

    :param gcpList:     <list> list of ground control points in the output coordinate system
                                to be used for warping, e.g. [gdal.GCP(mapX,mapY,mapZ,column,row),...]
    :param prj_src:     WKT string
    :param prj_tgt:     WKT string
    :return:
    """
    return [gdal.GCP(*(list(transform_any_prj(prj_src, prj_tgt, GCP.GCPX, GCP.GCPY)) +
                       [GCP.GCPZ, GCP.GCPPixel, GCP.GCPLine]))  # Python 2.7 compatible syntax
            for GCP in gcpList]


def reproject_shapelyGeometry(shapelyGeometry, prj_src, prj_tgt):
    """Reprojects any shapely geometry from one projection to another.

    :param shapelyGeometry: any shapely geometry instance
    :param prj_src:         GDAL projection as WKT string or EPSG code ('epsg:1234' or <EPSG_int>)
    :param prj_tgt:         GDAL projection as WKT string or EPSG code ('epsg:1234' or <EPSG_int>)
    """
    project = pyproj.Transformer.from_proj(
        pyproj.CRS.from_user_input(prj_src),
        pyproj.CRS.from_user_input(prj_tgt),
        always_xy=True)

    return transform(project.transform, shapelyGeometry)  # apply projection

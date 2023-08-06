# -*- coding: utf-8 -*-

# sensormapgeo, Transform remote sensing images between sensor and map geometry.
#
# Copyright (C) 2020  Daniel Scheffler (GFZ Potsdam, danschef@gfz-potsdam.de)
#
# This software was developed within the context of the EnMAP project supported
# by the DLR Space Administration with funds of the German Federal Ministry of
# Economic Affairs and Energy (on the basis of a decision by the German Bundestag:
# 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.
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

"""Module to transform 2D arrays between sensor and map geometry."""

from typing import Union, List, Tuple, Optional
import os
import warnings
from tempfile import TemporaryDirectory
from time import sleep

import numpy as np
import gdal
from pyproj import CRS
from py_tools_ds.geo.coord_trafo import transform_coordArray, transform_any_prj
from py_tools_ds.geo.coord_calc import corner_coord_to_minmax, get_corner_coordinates
from py_tools_ds.geo.coord_grid import find_nearest
from py_tools_ds.io.raster.writer import write_numpy_to_image
from py_tools_ds.processing.shell import subcall_with_output

# NOTE: In case of ImportError: dlopen: cannot load any more object with static TLS,
#       one could add 'from pykdtree.kdtree import KDTree' here (before pyresample import)
from pyresample.geometry import AreaDefinition, SwathDefinition, create_area_def
from pyresample.bilinear import resample_bilinear
from pyresample.kd_tree import resample_nearest, resample_gauss, resample_custom


class SensorMapGeometryTransformer(object):
    def __init__(self,
                 lons: np.ndarray,
                 lats: np.ndarray,
                 resamp_alg: str = 'nearest',
                 radius_of_influence: int = 30,
                 **opts) -> None:
        """Get an instance of SensorMapGeometryTransformer.

        :param lons:    2D longitude array corresponding to the 2D sensor geometry array
        :param lats:    2D latitude array corresponding to the 2D sensor geometry array

        :Keyword Arguments:  (further documentation here: https://pyresample.readthedocs.io/en/latest/swath.html)
            - resamp_alg:           resampling algorithm ('nearest', 'bilinear', 'gauss', 'custom')
            - radius_of_influence:  <float> Cut off distance in meters (default: 30)
                                    NOTE: keyword is named 'radius' in case of bilinear resampling
            - sigmas:               <list of floats or float> [ONLY 'gauss'] List of sigmas to use for the gauss
                                    weighting of each channel 1 to k, w_k = exp(-dist^2/sigma_k^2). If only one channel
                                    is resampled sigmas is a single float value.
            - neighbours:           <int> [ONLY 'bilinear', 'gauss'] Number of neighbours to consider for each grid
                                    point when searching the closest corner points
            - epsilon:              <float> Allowed uncertainty in meters. Increasing uncertainty reduces execution time
            - weight_funcs:         <list of function objects or function object> [ONLY 'custom'] List of weight
                                    functions f(dist) to use for the weighting of each channel 1 to k. If only one
                                    channel is resampled weight_funcs is a single function object.
            - fill_value:           <int or None> Set undetermined pixels to this value (default: 0).
                                    If fill_value is None a masked array is returned with undetermined pixels masked
            - reduce_data:          <bool> Perform initial coarse reduction of source dataset in order to reduce
                                    execution time
            - nprocs:               <int>, Number of processor cores to be used
            - segments:             <int or None> Number of segments to use when resampling.
                                    If set to None an estimate will be calculated
            - with_uncert:          <bool> [ONLY 'gauss' and 'custom'] Calculate uncertainty estimates
                                    NOTE: resampling function has 3 return values instead of 1: result, stddev, count
        """
        # validation
        if lons.ndim != 2:
            raise ValueError('Expected a 2D longitude array. Received a %dD array.' % lons.ndim)
        if lats.ndim != 2:
            raise ValueError('Expected a 2D latitude array. Received a %dD array.' % lats.ndim)
        if lons.shape != lats.shape:
            raise ValueError((lons.shape, lats.shape), "'lons' and 'lats' are expected to have the same shape.")

        self.resamp_alg = resamp_alg
        self.opts = dict(radius_of_influence=radius_of_influence,
                         sigmas=(radius_of_influence / 2))
        self.opts.update(opts)

        if resamp_alg == 'bilinear':
            del self.opts['radius_of_influence']
            self.opts['radius'] = radius_of_influence

        # NOTE: If pykdtree is built with OpenMP support (default) the number of threads is controlled with the
        #       standard OpenMP environment variable OMP_NUM_THREADS. The nprocs argument has no effect on pykdtree.
        if 'nprocs' in self.opts:
            if self.opts['nprocs'] > 1:
                os.environ['OMP_NUM_THREADS'] = '%d' % opts['nprocs']
            del self.opts['nprocs']

        self.lats = lats
        self.lons = lons
        self.swath_definition = SwathDefinition(lons=lons, lats=lats)
        # use a projection string for local coordinates (https://gis.stackexchange.com/a/300407)
        # -> this is needed for bilinear resampling
        self.swath_definition.proj_str = '+proj=omerc +lat_0=51.6959777875 +lonc=7.0923165808 +alpha=-20.145 ' \
                                         '+gamma=0 +k=1 +x_0=50692.579 +y_0=81723.458 +ellps=WGS84 ' \
                                         '+towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
        self.area_extent_ll = [np.min(lons), np.min(lats), np.max(lons), np.max(lats)]
        self.area_definition: Optional[AreaDefinition] = None

    def _get_target_extent(self, tgt_epsg: int):
        if tgt_epsg == 4326:
            tgt_extent = self.area_extent_ll
        else:
            corner_coords_ll = [[self.lons[0, 0], self.lats[0, 0]],  # UL_xy
                                [self.lons[0, -1], self.lats[0, -1]],  # UR_xy
                                [self.lons[-1, 0], self.lats[-1, 0]],  # LL_xy
                                [self.lons[-1, -1], self.lats[-1, -1]],  # LR_xy
                                ]
            tgt_extent = _corner_coords_lonlat_to_extent(corner_coords_ll, tgt_epsg)

        return tgt_extent

    def compute_areadefinition_sensor2map(self,
                                          data: np.ndarray,
                                          tgt_prj: Union[int, str],
                                          tgt_extent: Tuple[float, float, float, float] = None,
                                          tgt_res: Tuple[float, float] = None) -> AreaDefinition:
        """Compute the area_definition to resample a sensor geometry array to map geometry.

        :param data:        numpy array to be warped to sensor or map geometry
        :param tgt_prj:     target projection (WKT or 'epsg:1234' or <EPSG_int>)
        :param tgt_extent:  extent coordinates of output map geometry array (LL_x, LL_y, UR_x, UR_y) in the tgt_prj
                            (automatically computed from the corner positions of the coordinate arrays)
        :param tgt_res:     target X/Y resolution (e.g., (30, 30))
        :return:
        """
        # get the target extent if not given
        # (this also makes sure that create_area_def does not return a DynamicAreaDefinition)
        tgt_epsg = CRS(tgt_prj).to_epsg()
        tgt_extent = tgt_extent or self._get_target_extent(tgt_epsg)

        if tgt_res:
            # add 1 px buffer around out_extent to avoid cutting the output image
            xmin, ymin, xmax, ymax = tgt_extent
            tgt_extent = (xmin - tgt_res[0], ymin - tgt_res[1], xmax + tgt_res[0], ymax + tgt_res[1])

            # get the area definition
            # NOTE: This would return a DynamicAreaDefinition if the extent is not provided
            #       -> could be transformed to an AreaDefinition by using its .freeze() method and
            #          passing LonLats and resolution
            area_definition = \
                create_area_def(area_id='',
                                projection='EPSG:%d' % CRS(tgt_prj).to_epsg(),
                                area_extent=tgt_extent,
                                resolution=tgt_res)

            out_res = (area_definition.pixel_size_x, area_definition.pixel_size_y)
            if tgt_res and tgt_res != out_res:
                warnings.warn('With respect to the Lon/Lat arrays the pixel size was set to %s instead of the desired '
                              '%s. Provide a target extent where the coordinates are multiples of the pixel sizes to '
                              'avoid this.' % (str(out_res), str(tgt_res)), UserWarning)

        else:
            def raiseErr_if_empty(gdal_ds):
                if not gdal_ds:
                    raise Exception(gdal.GetLastErrorMsg())
                return gdal_ds

            with TemporaryDirectory() as td:
                path_xycoords = os.path.join(td, 'xy_coords.bsq')
                path_xycoords_vrt = os.path.join(td, 'xy_coords.vrt')
                path_data = os.path.join(td, 'data.bsq')
                path_datavrt = os.path.join(td, 'data.vrt')
                path_data_out = os.path.join(td, 'data_out.bsq')

                # write X/Y coordinate array
                if tgt_epsg == 4326:
                    xy_coords = np.dstack([self.swath_definition.lons,
                                           self.swath_definition.lats])
                    # xy_coords = np.dstack([self.swath_definition.lons[::10, ::10],
                    #                        self.swath_definition.lats[::10, ::10]])
                else:
                    xy_coords = np.dstack(list(transform_coordArray(CRS(4326).to_wkt(), CRS(tgt_epsg).to_wkt(),
                                                                    self.swath_definition.lons,
                                                                    self.swath_definition.lats)))
                write_numpy_to_image(xy_coords, path_xycoords, 'ENVI')

                # create VRT for X/Y coordinate array
                ds_xy_coords = gdal.Open(path_xycoords)
                drv_vrt = gdal.GetDriverByName("VRT")
                # noinspection PyUnusedLocal
                vrt = raiseErr_if_empty(drv_vrt.CreateCopy(path_xycoords_vrt, ds_xy_coords))
                del ds_xy_coords, vrt

                # create VRT for one data band
                mask_band = np.ones((data.shape[:2]), np.int32)
                write_numpy_to_image(mask_band, path_data, 'ENVI')
                ds_data = gdal.Open(path_data)
                vrt = raiseErr_if_empty(drv_vrt.CreateCopy(path_datavrt, ds_data))
                vrt.SetMetadata({"X_DATASET": path_xycoords_vrt,
                                 "Y_DATASET": path_xycoords_vrt,
                                 "X_BAND": "1",
                                 "Y_BAND": "2",
                                 "PIXEL_OFFSET": "0",
                                 "LINE_OFFSET": "0",
                                 "PIXEL_STEP": "1",
                                 "LINE_STEP": "1",
                                 "SRS": CRS(tgt_epsg).to_wkt(),
                                 }, "GEOLOCATION")
                vrt.FlushCache()
                del ds_data, vrt

                subcall_with_output("gdalwarp '%s' '%s' "
                                    '-geoloc '
                                    '-t_srs EPSG:%d '
                                    '-srcnodata 0 '
                                    '-r near '
                                    '-of ENVI '
                                    '-dstnodata none '
                                    '-et 0 '
                                    '-overwrite '
                                    '-te %s '
                                    '%s' % (path_datavrt, path_data_out, tgt_epsg,
                                            ' '.join([str(i) for i in tgt_extent]),
                                            ' -tr %s %s' % tgt_res if tgt_res else '',),
                                    v=True)

                # get output X/Y size
                ds_out = raiseErr_if_empty(gdal.Open(path_data_out))

                x_size = ds_out.RasterXSize
                y_size = ds_out.RasterYSize
                out_gt = ds_out.GetGeoTransform()

                # noinspection PyUnusedLocal
                ds_out = None
                # avoid NotADirectoryError, possibly due to a race condition on Windows
                sleep(.1)

            # add 1 px buffer around out_extent to avoid cutting the output image
            x_size += 2
            y_size += 2
            out_gt = list(out_gt)
            out_gt[0] -= out_gt[1]
            out_gt[3] += abs(out_gt[5])
            out_gt = tuple(out_gt)
            xmin, xmax, ymin, ymax = corner_coord_to_minmax(get_corner_coordinates(gt=out_gt, cols=x_size, rows=y_size))
            out_extent = xmin, ymin, xmax, ymax

            # get area_definition
            area_definition = AreaDefinition(area_id='',
                                             description='',
                                             proj_id='',
                                             projection=CRS(tgt_prj),
                                             width=x_size,
                                             height=y_size,
                                             area_extent=list(out_extent),
                                             )

        return area_definition

    def _resample(self,
                  data: np.ndarray,
                  source_geo_def: Union[AreaDefinition, SwathDefinition],
                  target_geo_def: Union[AreaDefinition, SwathDefinition]) -> np.ndarray:
        """Run the resampling algorithm.

        :param data:            numpy array to be warped to sensor or map geometry
        :param source_geo_def:  source geo definition
        :param target_geo_def:  target geo definition
        :return:
        """
        if self.resamp_alg == 'nearest':
            opts = {k: v for k, v in self.opts.items() if k not in ['sigmas']}
            result = resample_nearest(source_geo_def, data, target_geo_def, **opts).astype(data.dtype)

        elif self.resamp_alg == 'bilinear':
            opts = {k: v for k, v in self.opts.items() if k not in ['sigmas']}
            with warnings.catch_warnings():
                # suppress a UserWarning coming from pyresample v0.15.0
                warnings.filterwarnings('ignore', category=UserWarning,
                                        message='You will likely lose important projection information when converting '
                                                'to a PROJ string from another format.')
                result = resample_bilinear(data, source_geo_def, target_geo_def, **opts).astype(data.dtype)

        elif self.resamp_alg == 'gauss':
            opts = {k: v for k, v in self.opts.items()}

            # ensure that sigmas are provided as list if data is 3-dimensional
            if data.ndim != 2:
                if not isinstance(opts['sigmas'], list):
                    opts['sigmas'] = [opts['sigmas']] * data.ndim
                if not len(opts['sigmas']) == data.ndim:
                    raise ValueError("The 'sigmas' parameter must have the same number of values like data.ndim."
                                     "n_sigmas: %d; data.ndim: %d" % (len(opts['sigmas']), data.ndim))

            result = resample_gauss(source_geo_def, data, target_geo_def, **opts).astype(data.dtype)

        elif self.resamp_alg == 'custom':
            opts = {k: v for k, v in self.opts.items()}
            if 'weight_funcs' not in opts:
                raise ValueError(opts, "Options must contain a 'weight_funcs' item.")
            result = resample_custom(source_geo_def, data, target_geo_def, **opts).astype(data.dtype)

        else:
            raise ValueError(self.resamp_alg)

        return result

    @staticmethod
    def _get_gt_prj_from_areadefinition(area_definition: AreaDefinition) -> (Tuple[float, float, float,
                                                                                   float, float, float], str):
        gt = area_definition.area_extent[0], area_definition.pixel_size_x, 0, \
             area_definition.area_extent[3], 0, -area_definition.pixel_size_y
        prj = area_definition.crs.to_wkt()

        return gt, prj

    def to_map_geometry(self, data: np.ndarray,
                        tgt_prj: Union[str, int] = None,
                        tgt_extent: Tuple[float, float, float, float] = None,
                        tgt_res: Tuple = None,
                        tgt_coordgrid: Tuple[Tuple, Tuple] = None,
                        area_definition: AreaDefinition = None) -> Tuple[np.ndarray, tuple, str]:
        """Transform the input sensor geometry array into map geometry.

        :param data:            numpy array (representing sensor geometry) to be warped to map geometry
        :param tgt_prj:         target projection (WKT or 'epsg:1234' or <EPSG_int>)
        :param tgt_extent:      extent coordinates of output map geometry array (LL_x, LL_y, UR_x, UR_y) in the tgt_prj
        :param tgt_res:         target X/Y resolution (e.g., (30, 30))
        :param tgt_coordgrid:   target coordinate grid ((x, x), (y, y)):
                                if given, the output extent is moved to this coordinate grid
        :param area_definition: an instance of pyresample.geometry.AreaDefinition;
                                OVERRIDES tgt_prj, tgt_extent and tgt_res; saves computation time
        """
        if self.lons.ndim > 2 >= data.ndim:
            raise ValueError(data.ndim, "'data' must at least have %d dimensions because of %d longiture array "
                                        "dimensions." % (self.lons.ndim, self.lons.ndim))

        if data.shape[:2] != self.lons.shape[:2]:
            raise ValueError(data.shape, 'Expected a sensor geometry data array with %d rows and %d columns.'
                             % self.lons.shape[:2])

        if tgt_coordgrid:
            tgt_res = _get_validated_tgt_res(tgt_coordgrid, tgt_res)

        # get area_definition
        if area_definition:
            self.area_definition = area_definition
        else:
            if not tgt_prj:
                raise ValueError(tgt_prj, 'Target projection must be given if area_definition is not given.')

            tgt_epsg = CRS(tgt_prj).to_epsg()
            tgt_extent = tgt_extent or self._get_target_extent(tgt_epsg)

            if tgt_coordgrid:
                tgt_extent = _move_extent_to_coordgrid(tgt_extent, *tgt_coordgrid)

            self.area_definition = self.compute_areadefinition_sensor2map(
                data, tgt_prj=tgt_prj, tgt_extent=tgt_extent, tgt_res=tgt_res)

        # resample
        data_mapgeo = self._resample(data, self.swath_definition, self.area_definition)
        out_gt, out_prj = self._get_gt_prj_from_areadefinition(self.area_definition)

        # output validation
        if not data_mapgeo.shape[:2] == (self.area_definition.height, self.area_definition.width):
            raise RuntimeError('The computed map geometry output does not have the expected number of rows/columns. '
                               'Expected: %s; output: %s.'
                               % (str((self.area_definition.height, self.area_definition.width)),
                                  str(data_mapgeo.shape[:2])))
        if data.ndim > 2 and data_mapgeo.ndim == 2:
            raise RuntimeError('The computed map geometry output has only one band instead of the expected %d bands.'
                               % data.shape[2])

        return data_mapgeo, out_gt, out_prj

    def to_sensor_geometry(self, data: np.ndarray,
                           src_prj: Union[str, int],
                           src_extent: Tuple[float, float, float, float]) -> np.ndarray:
        """Transform the input map geometry array into sensor geometry

        :param data:        numpy array (representing map geometry) to be warped to sensor geometry
        :param src_prj:     projection of the input map geometry array (WKT or 'epsg:1234' or <EPSG_int>)
        :param src_extent:  extent coordinates of input map geometry array (LL_x, LL_y, UR_x, UR_y) in the src_prj
        """
        # get area_definition
        self.area_definition = AreaDefinition('', '', '',  CRS(src_prj), data.shape[1], data.shape[0],
                                              list(src_extent))

        # resample
        data_sensorgeo = self._resample(data, self.area_definition, self.swath_definition)

        # output validation
        if not data_sensorgeo.shape[:2] == self.lats.shape[:2]:
            raise RuntimeError('The computed sensor geometry output does not have the same X/Y dimension like the '
                               'coordinates array. Coordinates array: %s; output array: %s.'
                               % (self.lats.shape, data_sensorgeo.shape))

        if data.ndim > 2 and data_sensorgeo.ndim == 2:
            raise RuntimeError('The computed sensor geometry output has only one band instead of the expected %d bands.'
                               % data.shape[2])

        return data_sensorgeo


def _corner_coords_lonlat_to_extent(corner_coords_ll: List, tgt_epsg: int):
    corner_coords_tgt_prj = [transform_any_prj(4326, tgt_epsg, x, y)
                             for x, y in corner_coords_ll]
    corner_coords_tgt_prj_np = np.array(corner_coords_tgt_prj)
    x_coords = corner_coords_tgt_prj_np[:, 0]
    y_coords = corner_coords_tgt_prj_np[:, 1]
    tgt_extent = [np.min(x_coords), np.min(y_coords), np.max(x_coords), np.max(y_coords)]

    return tgt_extent


def _move_extent_to_coordgrid(extent: Tuple[float, float, float, float],
                              tgt_xgrid: Tuple[float, float],
                              tgt_ygrid: Tuple[float, float]):
    tgt_xgrid, tgt_ygrid = np.array(tgt_xgrid), np.array(tgt_ygrid)
    xmin, ymin, xmax, ymax = extent
    tgt_xmin = find_nearest(tgt_xgrid, xmin, roundAlg='off', extrapolate=True)
    tgt_xmax = find_nearest(tgt_xgrid, xmax, roundAlg='on', extrapolate=True)
    tgt_ymin = find_nearest(tgt_ygrid, ymin, roundAlg='off', extrapolate=True)
    tgt_ymax = find_nearest(tgt_ygrid, ymax, roundAlg='on', extrapolate=True)

    return tgt_xmin, tgt_ymin, tgt_xmax, tgt_ymax


def _get_validated_tgt_res(tgt_coordgrid, tgt_res):
    exp_tgt_res = np.ptp(tgt_coordgrid[0]), np.ptp(tgt_coordgrid[1])
    if tgt_res and exp_tgt_res != tgt_res:
        raise ValueError('The target resolution must be compliant to the target coordinate grid if given.')

    return exp_tgt_res

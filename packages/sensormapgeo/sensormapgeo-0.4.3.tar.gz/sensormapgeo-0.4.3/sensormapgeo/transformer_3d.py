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

"""Module to transform 3D arrays between sensor and map geometry (using band-wise Lon/Lat arrays)."""

from typing import Union, Tuple
import multiprocessing

import numpy as np
from pyproj import CRS
from py_tools_ds.geo.coord_trafo import transform_any_prj

from .transformer_2d import \
    SensorMapGeometryTransformer, _corner_coords_lonlat_to_extent, \
    _move_extent_to_coordgrid, _get_validated_tgt_res
from pyresample import AreaDefinition


class SensorMapGeometryTransformer3D(object):
    def __init__(self,
                 lons: np.ndarray,
                 lats: np.ndarray,
                 resamp_alg: str = 'nearest',
                 radius_of_influence: int = 30,
                 mp_alg: str = 'auto',
                 **opts) -> None:
        """Get an instance of SensorMapGeometryTransformer.

        :param lons:    3D longitude array corresponding to the 3D sensor geometry array
        :param lats:    3D latitude array corresponding to the 3D sensor geometry array

        :Keyword Arguments:  (further documentation here: https://pyresample.readthedocs.io/en/latest/swath.html)
            - resamp_alg:           resampling algorithm ('nearest', 'bilinear', 'gauss', 'custom')
            - radius_of_influence:  <float> Cut off distance in meters (default: 30)
                                    NOTE: keyword is named 'radius' in case of bilinear resampling
            - mp_alg                multiprocessing algorithm
                                    'bands': parallelize over bands using multiprocessing lib
                                    'tiles': parallelize over tiles using OpenMP
                                    'auto': automatically choose the algorithm
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
        if lons.ndim != 3:
            raise ValueError('Expected a 3D longitude array. Received a %dD array.' % lons.ndim)
        if lats.ndim != 3:
            raise ValueError('Expected a 3D latitude array. Received a %dD array.' % lats.ndim)
        if lons.shape != lats.shape:
            raise ValueError((lons.shape, lats.shape), "'lons' and 'lats' are expected to have the same shape.")

        self.lats = lats
        self.lons = lons
        self.resamp_alg = resamp_alg
        self.radius_of_influence = radius_of_influence
        self.opts = opts

        # define number of CPUs to use (but avoid sub-multiprocessing)
        #   -> parallelize either over bands or over image tiles
        #      bands: multiprocessing uses multiprocessing.Pool, implemented in to_map_geometry / to_sensor_geometry
        #      tiles: multiprocessing uses OpenMP implemented in pykdtree which is used by pyresample
        self.opts['nprocs'] = opts.get('nprocs', multiprocessing.cpu_count())
        if self.opts['nprocs'] > multiprocessing.cpu_count():
            self.opts['nprocs'] = multiprocessing.cpu_count()
        self.mp_alg = ('bands' if self.lons.shape[2] >= opts['nprocs'] else 'tiles') if mp_alg == 'auto' else mp_alg

    @staticmethod
    def _to_map_geometry_2D(kwargs_dict: dict
                            ) -> Tuple[np.ndarray, tuple, str, int]:
        SMGT2D = SensorMapGeometryTransformer(lons=kwargs_dict['lons'],
                                              lats=kwargs_dict['lats'],
                                              resamp_alg=kwargs_dict['resamp_alg'],
                                              radius_of_influence=kwargs_dict['radius_of_influence'],
                                              **kwargs_dict['init_opts'])
        data_mapgeo, out_gt, out_prj = SMGT2D.to_map_geometry(data=kwargs_dict['data'],
                                                              area_definition=kwargs_dict['area_definition'])

        return data_mapgeo, out_gt, out_prj, kwargs_dict['band_idx']

    def _get_common_target_extent(self,
                                  tgt_epsg: int,
                                  tgt_coordgrid: Tuple[Tuple, Tuple] = None):
        if tgt_epsg == 4326:
            corner_coords_ll = [[self.lons[0, 0, :].min(), self.lats[0, 0, :].max()],  # common UL_xy
                                [self.lons[0, -1, :].max(), self.lats[0, -1, :].max()],  # common UR_xy
                                [self.lons[-1, 0, :].min(), self.lats[-1, 0, :].min()],  # common LL_xy
                                [self.lons[-1, -1, :].max(), self.lats[-1, -1, :].min()],  # common LR_xy
                                ]
            common_tgt_extent = _corner_coords_lonlat_to_extent(corner_coords_ll, tgt_epsg)
        else:
            # get Lon/Lat corner coordinates of geolayers
            UL_UR_LL_LR_ll = [(self.lons[y, x], self.lats[y, x]) for y, x in [(0, 0), (0, -1), (-1, 0), (-1, -1)]]

            # transform them to target projection
            UL_UR_LL_LR_prj = [transform_any_prj(4326, tgt_epsg, x, y) for x, y in UL_UR_LL_LR_ll]

            # separate X and Y
            X_prj, Y_prj = zip(*UL_UR_LL_LR_prj)

            # 3D geolayers, i.e., the corner coordinates have multiple values for multiple bands
            # -> use the outermost coordinates to be sure all data is included
            X_prj = (X_prj[0].min(), X_prj[1].max(), X_prj[2].min(), X_prj[3].max())
            Y_prj = (Y_prj[0].max(), Y_prj[1].max(), Y_prj[2].min(), Y_prj[3].min())

            # get the extent
            common_tgt_extent = (min(X_prj), min(Y_prj), max(X_prj), max(Y_prj))

        if tgt_coordgrid:
            common_tgt_extent = _move_extent_to_coordgrid(common_tgt_extent, *tgt_coordgrid)

        return common_tgt_extent

    def _get_common_area_definition(self,
                                    data: np.ndarray,
                                    tgt_prj: Union[str, int],
                                    tgt_extent: Tuple[float, float, float, float] = None,
                                    tgt_res: Tuple = None,
                                    tgt_coordgrid: Tuple[Tuple, Tuple] = None
                                    ) -> AreaDefinition:
        # get common target extent
        tgt_epsg = CRS(tgt_prj).to_epsg()
        tgt_extent = tgt_extent or self._get_common_target_extent(tgt_epsg, tgt_coordgrid=tgt_coordgrid)

        SMGT2D = SensorMapGeometryTransformer(lons=self.lons[:, :, 0],  # does NOT affect the computed area definition
                                              lats=self.lats[:, :, 0],  # -> only needed for __init__
                                              resamp_alg=self.resamp_alg,
                                              radius_of_influence=self.radius_of_influence,
                                              **self.opts)
        common_area_definition = SMGT2D.compute_areadefinition_sensor2map(data=data[:, :, 0],
                                                                          tgt_prj=tgt_prj,
                                                                          tgt_extent=tgt_extent,
                                                                          tgt_res=tgt_res)

        return common_area_definition

    def to_map_geometry(self,
                        data: np.ndarray,
                        tgt_prj: Union[str, int],
                        tgt_extent: Tuple[float, float, float, float] = None,
                        tgt_res: Tuple[float, float] = None,
                        tgt_coordgrid: Tuple[Tuple, Tuple] = None,
                        area_definition: AreaDefinition = None
                        ) -> Tuple[np.ndarray, tuple, str]:
        """Transform the input sensor geometry array into map geometry.

        :param data:            3D numpy array (representing sensor geometry) to be warped to map geometry
        :param tgt_prj:         target projection (WKT or 'epsg:1234' or <EPSG_int>)
        :param tgt_extent:      extent coordinates of output map geometry array (LL_x, LL_y, UR_x, UR_y) in the tgt_prj
        :param tgt_res:         target X/Y resolution (e.g., (30, 30))
        :param tgt_coordgrid:   target coordinate grid ((x, x), (y, y)):
                                if given, the output extent is moved to this coordinate grid
        :param area_definition: an instance of pyresample.geometry.AreaDefinition;
                                OVERRIDES tgt_prj, tgt_extent, tgt_res and tgt_coordgrid; saves computation time
        """
        if data.ndim != 3:
            raise ValueError(data.ndim, "'data' must have 3 dimensions.")

        if data.shape != self.lons.shape:
            raise ValueError(data.shape, 'Expected a sensor geometry data array with %d rows, %d columns and %d bands.'
                             % self.lons.shape)

        if not tgt_prj and not area_definition:
            raise ValueError(tgt_prj, 'Target projection must be given if area_definition is not given.')

        if tgt_coordgrid:
            tgt_res = _get_validated_tgt_res(tgt_coordgrid, tgt_res)

        init_opts = self.opts.copy()
        if self.mp_alg == 'bands':
            del init_opts['nprocs']  # avoid sub-multiprocessing

        # get common area_definition
        if not area_definition:
            area_definition = self._get_common_area_definition(data, tgt_prj, tgt_extent, tgt_res, tgt_coordgrid)

        args = [dict(
            resamp_alg=self.resamp_alg,
            radius_of_influence=self.radius_of_influence,
            init_opts=init_opts,
            area_definition=area_definition,
            band_idx=band,
            lons=self.lons[:, :, band],
            lats=self.lats[:, :, band],
            data=data[:, :, band],
        ) for band in range(data.shape[2])]

        if self.opts['nprocs'] > 1 and self.mp_alg == 'bands':
            # NOTE: We use imap here as it directly returns the results when available (works like a generator).
            #       This saves a lot of memory compared with map. We also don't use an initializer to share the input
            #       arrays because this would allocate the memory for the input arrays of all bands at once.
            with multiprocessing.Pool(self.opts['nprocs']) as pool:
                result = [res for res in pool.imap_unordered(self._to_map_geometry_2D, args)]

        else:
            result = [self._to_map_geometry_2D(argsdict) for argsdict in args]

        band_inds = [res[-1] for res in result]
        data_mapgeo = np.dstack([result[band_inds.index(i)][0] for i in range(data.shape[2])])
        out_gt = result[0][1]
        out_prj = result[0][2]

        return data_mapgeo, out_gt, out_prj

    @staticmethod
    def _to_sensor_geometry_2D(kwargs_dict: dict
                               ) -> (np.ndarray, int):
        SMGT2D = SensorMapGeometryTransformer(lons=kwargs_dict['lons'],
                                              lats=kwargs_dict['lats'],
                                              resamp_alg=kwargs_dict['resamp_alg'],
                                              radius_of_influence=kwargs_dict['radius_of_influence'],
                                              **kwargs_dict['init_opts'])
        data_sensorgeo = SMGT2D.to_sensor_geometry(data=kwargs_dict['data'],
                                                   src_prj=kwargs_dict['src_prj'],
                                                   src_extent=kwargs_dict['src_extent'])

        return data_sensorgeo, kwargs_dict['band_idx']

    def to_sensor_geometry(self,
                           data: np.ndarray,
                           src_prj: Union[str, int],
                           src_extent: Tuple[float, float, float, float]
                           ) -> np.ndarray:
        """Transform the input map geometry array into sensor geometry

        :param data:        3D numpy array (representing map geometry) to be warped to sensor geometry
        :param src_prj:     projection of the input map geometry array (WKT or 'epsg:1234' or <EPSG_int>)
        :param src_extent:  extent coordinates of input map geometry array (LL_x, LL_y, UR_x, UR_y) in the src_prj
        """
        if data.ndim != 3:
            raise ValueError(data.ndim, "'data' must have 3 dimensions.")

        init_opts = self.opts.copy()
        if self.mp_alg == 'bands':
            del init_opts['nprocs']  # avoid sub-multiprocessing

        args = [dict(
            resamp_alg=self.resamp_alg,
            radius_of_influence=self.radius_of_influence,
            init_opts=init_opts,
            src_prj=src_prj,
            src_extent=src_extent,
            band_idx=band,
            lons=self.lons[:, :, band],
            lats=self.lats[:, :, band],
            data=data[:, :, band],

        ) for band in range(data.shape[2])]

        if self.opts['nprocs'] > 1 and self.mp_alg == 'bands':
            # NOTE: See the comments in the to_map_geometry() method.
            with multiprocessing.Pool(self.opts['nprocs']) as pool:
                result = [res for res in pool.imap_unordered(self._to_sensor_geometry_2D, args)]
        else:
            result = [self._to_sensor_geometry_2D(argsdict) for argsdict in args]

        band_inds = [res[-1] for res in result]
        data_sensorgeo = np.dstack([result[band_inds.index(i)][0] for i in range(data.shape[2])])

        return data_sensorgeo

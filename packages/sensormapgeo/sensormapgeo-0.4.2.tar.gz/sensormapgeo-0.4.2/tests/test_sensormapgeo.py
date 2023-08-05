#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sensormapgeo, A package for transforming remote sensing images between sensor and map geometry.
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

"""Tests for `sensormapgeo` package."""


import os
from unittest import TestCase

import numpy as np
from gdalnumeric import LoadFile
from py_tools_ds.geo.coord_calc import corner_coord_to_minmax, get_corner_coordinates

from sensormapgeo import __path__
from sensormapgeo import SensorMapGeometryTransformer, SensorMapGeometryTransformer3D


tests_path = os.path.abspath(os.path.join(__path__[0], "..", "tests"))
rsp_algs = ['nearest', 'bilinear', 'gauss']


class Test_SensorMapGeometryTransformer(TestCase):
    def setUp(self):
        self.dem_map_geo = LoadFile(os.path.join(tests_path, 'data', 'dem_map_geo.bsq'))
        self.dem_sensor_geo = LoadFile(os.path.join(tests_path, 'data', 'dem_sensor_geo.bsq'))
        self.lons = LoadFile(os.path.join(tests_path, 'data', 'lons_full_vnir.bsq'))
        self.lats = LoadFile(os.path.join(tests_path, 'data', 'lats_full_vnir.bsq'))
        self.dem_area_extent_coarse_subset_utm = (622613.864409047,  # LL_x
                                                  5254111.40255343,  # LL_x
                                                  660473.864409047,  # LL_x
                                                  5269351.40255343)  # UR_y

        self.expected_dem_area_extent_lonlat = (10.685733901515151,  # LL_x
                                                47.44113415492957,  # LL_y
                                                11.073066098484848,  # UR_x
                                                47.54576584507042)  # UR_y

        self.expected_dem_area_extent_utm = (626938.928052,  # LL_x
                                             5256253.56579,  # LL_y
                                             656188.928052,  # UR_x
                                             5267203.56579)  # UR_y

        self.expected_dem_area_extent_utm_ongrid = (626910,  # LL_x
                                                    5256240,  # LL_y
                                                    656190,  # UR_x
                                                    5267220)  # UR_y

    def test_to_sensor_geometry(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer(lons=self.lons,
                                                lats=self.lats,
                                                resamp_alg=rsp_alg,
                                                radius_of_influence=30 if rsp_alg != 'bilinear' else 45)
            dem_sensor_geo = SMGT.to_sensor_geometry(self.dem_map_geo,
                                                     src_prj=32632, src_extent=self.dem_area_extent_coarse_subset_utm)
            self.assertIsInstance(dem_sensor_geo, np.ndarray)
            self.assertFalse(np.array_equal(np.unique(dem_sensor_geo), np.array([0])))
            self.assertEqual(dem_sensor_geo.shape, (150, 1000))
            self.assertEqual(self.dem_map_geo.dtype, dem_sensor_geo.dtype)

    def test_to_sensor_geometry_3DInput(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer(lons=self.lons,
                                                lats=self.lats,
                                                resamp_alg=rsp_alg)
            dem_sensor_geo = SMGT.to_sensor_geometry(np.dstack([self.dem_map_geo] * 2),
                                                     src_prj=32632, src_extent=self.dem_area_extent_coarse_subset_utm)
            self.assertIsInstance(dem_sensor_geo, np.ndarray)
            self.assertFalse(np.array_equal(np.unique(dem_sensor_geo), np.array([0])))
            self.assertEqual(dem_sensor_geo.shape, (150, 1000, 2))
            self.assertTrue(np.array_equal(dem_sensor_geo[:, :, 0], dem_sensor_geo[:, :, 1]))
            self.assertEqual(self.dem_map_geo.dtype, dem_sensor_geo.dtype)

    def test_to_map_geometry_lonlat(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer(lons=self.lons,
                                                lats=self.lats,
                                                resamp_alg=rsp_alg)

            # to Lon/Lat
            dem_map_geo, dem_gt, dem_prj = SMGT.to_map_geometry(self.dem_sensor_geo, tgt_prj=4326)

            # from geoarray import GeoArray
            # GeoArray(dem_map_geo, dem_gt, dem_prj)\
            #     .save(os.path.join(tests_path, 'test_output', 'resampled_pyresample_ll.bsq'))

            self.assertIsInstance(dem_map_geo, np.ndarray)
            self.assertEqual(dem_map_geo.shape, (SMGT.area_definition.height,
                                                 SMGT.area_definition.width))
            xmin, xmax, ymin, ymax = corner_coord_to_minmax(get_corner_coordinates(gt=dem_gt,
                                                                                   cols=dem_map_geo.shape[1],
                                                                                   rows=dem_map_geo.shape[0]))
            self.assertTrue(False not in np.isclose(np.array([xmin, ymin, xmax, ymax]),
                                                    np.array(self.expected_dem_area_extent_lonlat)))
            self.assertFalse(np.array_equal(np.unique(dem_map_geo), np.array([0])))
            self.assertTrue(np.isclose(np.mean(dem_map_geo[dem_map_geo != 0]),
                                       np.mean(self.dem_sensor_geo),
                                       rtol=0.01))
            self.assertEqual(self.dem_sensor_geo.dtype, dem_map_geo.dtype)

            with self.assertRaises(ValueError):
                SMGT.to_map_geometry(self.dem_sensor_geo[:10, :10], tgt_prj=4326)  # must have the shape of lons/lats

    def test_to_map_geometry_utm(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer(lons=self.lons,
                                                lats=self.lats,
                                                resamp_alg=rsp_alg,
                                                # neighbours=8,
                                                # radius_of_influence=45,
                                                # epsilon=0
                                                )

            # to UTM32
            # dem_map_geo, dem_gt, dem_prj = SMGT.to_map_geometry(self.dem_sensor_geo, tgt_prj=32632, tgt_res=(30, 30))
            dem_map_geo, dem_gt, dem_prj = SMGT.to_map_geometry(self.dem_sensor_geo, tgt_prj=32632,
                                                                tgt_res=(30, 30),
                                                                # tgt_extent=self.expected_dem_area_extent_utm,
                                                                tgt_coordgrid=((0, 30), (0, 30))
                                                                )
            # from geoarray import GeoArray
            # GeoArray(dem_map_geo, dem_gt, dem_prj).save(os.path.join(tests_path, 'test_output',
            #                                                          'resampled_pyresample_bilinear_16n.bsq'))

            self.assertIsInstance(dem_map_geo, np.ndarray)
            self.assertEqual(dem_map_geo.shape, (366, 976))
            xmin, xmax, ymin, ymax = corner_coord_to_minmax(get_corner_coordinates(gt=dem_gt,
                                                                                   cols=dem_map_geo.shape[1],
                                                                                   rows=dem_map_geo.shape[0]))
            self.assertTrue(False not in np.isclose(np.array([xmin, ymin, xmax, ymax]),
                                                    np.array(self.expected_dem_area_extent_utm_ongrid)))
            self.assertFalse(np.array_equal(np.unique(dem_map_geo), np.array([0])))
            self.assertTrue(np.isclose(np.mean(dem_map_geo[dem_map_geo != 0]),
                                       np.mean(self.dem_sensor_geo),
                                       rtol=0.01))
            self.assertEqual(self.dem_sensor_geo.dtype, dem_map_geo.dtype)


class Test_SensorMapGeometryTransformer3D(TestCase):
    def setUp(self):
        dem_map_geo = LoadFile(os.path.join(tests_path, 'data', 'dem_map_geo.bsq'))
        dem_sensor_geo = LoadFile(os.path.join(tests_path, 'data', 'dem_sensor_geo.bsq'))
        lons = LoadFile(os.path.join(tests_path, 'data', 'lons_full_vnir.bsq'))
        lats = LoadFile(os.path.join(tests_path, 'data', 'lats_full_vnir.bsq'))

        self.data_map_geo_3D = np.dstack([dem_map_geo, dem_map_geo])
        self.data_sensor_geo_3D = np.dstack([dem_sensor_geo, dem_sensor_geo])
        self.lons_3D = np.dstack([lons, lons + .002])  # assume slightly different coordinates in both bands
        self.lats_3D = np.dstack([lats, lats + .002])

        self.dem_area_extent_coarse_subset_utm = (622613.864409047,  # LL_x
                                                  5254111.40255343,  # LL_x
                                                  660473.864409047,  # LL_x
                                                  5269351.40255343)  # UR_y

        # this differs from the 2D version because the geolayer in the second band has slightly different coordinates
        self.expected_dem_area_extent_lonlat = (10.685733901515151,  # LL_x
                                                47.44113415492957,  # LL_y
                                                11.075064739115845,  # UR_x
                                                47.54772559829233)  # UR_y

        self.expected_dem_area_extent_utm = (626938.928052,  # LL_x
                                             5256253.56579,  # LL_y
                                             656188.928052,  # UR_x
                                             5267203.56579)  # UR_y

        # this differs from the 2D version because the geolayer in the second band has slightly different coordinates
        self.expected_dem_area_extent_utm_ongrid = (626910,  # LL_x
                                                    5256240,  # LL_y
                                                    656340,  # UR_x
                                                    5267430)  # UR_y

    def test_to_map_geometry_lonlat_3D_geolayer(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer3D(lons=self.lons_3D,
                                                  lats=self.lats_3D,
                                                  # resamp_alg='nearest',
                                                  resamp_alg=rsp_alg,
                                                  )

            # to Lon/Lat
            data_mapgeo_3D, dem_gt, dem_prj = SMGT.to_map_geometry(self.data_sensor_geo_3D, tgt_prj=4326)

            # from geoarray import GeoArray
            # GeoArray(data_mapgeo_3D, dem_gt, dem_prj)\
            #     .save(os.path.join(tests_path, 'test_output', 'resampled_3D_02_ll.bsq'))

            self.assertIsInstance(data_mapgeo_3D, np.ndarray)
            # only validate number of bands (height and width are validated in 2D version
            #   fixed numbers may fail here due to float uncertainty errors
            self.assertGreater(np.dot(*data_mapgeo_3D.shape[:2]), np.dot(*self.data_sensor_geo_3D.shape[:2]))
            self.assertEqual(data_mapgeo_3D.shape[2], 2)
            xmin, xmax, ymin, ymax = corner_coord_to_minmax(get_corner_coordinates(gt=dem_gt,
                                                                                   cols=data_mapgeo_3D.shape[1],
                                                                                   rows=data_mapgeo_3D.shape[0]))
            self.assertTrue(False not in np.isclose(np.array([xmin, ymin, xmax, ymax]),
                                                    np.array(self.expected_dem_area_extent_lonlat)))

            self.assertTrue(np.isclose(np.mean(data_mapgeo_3D[data_mapgeo_3D != 0]),
                                       np.mean(self.data_sensor_geo_3D),
                                       rtol=0.01))
            self.assertEqual(self.data_sensor_geo_3D.dtype, data_mapgeo_3D.dtype)

    def test_to_map_geometry_utm_3D_geolayer(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer3D(lons=self.lons_3D,
                                                  lats=self.lats_3D,
                                                  # resamp_alg='nearest',
                                                  resamp_alg=rsp_alg,
                                                  )

            # to Lon/Lat
            data_mapgeo_3D, dem_gt, dem_prj = SMGT.to_map_geometry(self.data_sensor_geo_3D,
                                                                   tgt_prj=32632,
                                                                   tgt_res=(30, 30),
                                                                   # tgt_extent=self.expected_dem_area_extent_utm,
                                                                   tgt_coordgrid=((0, 30), (0, 30))
                                                                   )
            # from geoarray import GeoArray
            # GeoArray(data_mapgeo_3D, dem_gt, dem_prj)\
            #     .save(os.path.join(tests_path, 'test_output', 'resampled_3D_02_pyresample.bsq'))

            self.assertIsInstance(data_mapgeo_3D, np.ndarray)
            # only validate number of bands (height and width are validated in 2D version
            #   fixed numbers may fail here due to float uncertainty errors
            self.assertGreater(np.dot(*data_mapgeo_3D.shape[:2]), np.dot(*self.data_sensor_geo_3D.shape[:2]))
            self.assertEqual(data_mapgeo_3D.shape[2], 2)
            xmin, xmax, ymin, ymax = corner_coord_to_minmax(get_corner_coordinates(gt=dem_gt,
                                                                                   cols=data_mapgeo_3D.shape[1],
                                                                                   rows=data_mapgeo_3D.shape[0]))
            self.assertTrue(False not in np.isclose(np.array([xmin, ymin, xmax, ymax]),
                                                    np.array(self.expected_dem_area_extent_utm_ongrid)))

            self.assertTrue(np.isclose(np.mean(data_mapgeo_3D[data_mapgeo_3D != 0]),
                                       np.mean(self.data_sensor_geo_3D),
                                       rtol=0.01))
            self.assertEqual(self.data_sensor_geo_3D.dtype, data_mapgeo_3D.dtype)

    def test_to_sensor_geometry(self):
        for rsp_alg in rsp_algs:
            SMGT = SensorMapGeometryTransformer3D(lons=self.lons_3D,
                                                  lats=self.lats_3D,
                                                  resamp_alg=rsp_alg,
                                                  )
            dem_sensors_geo = SMGT.to_sensor_geometry(self.data_map_geo_3D,
                                                      src_prj=32632, src_extent=self.dem_area_extent_coarse_subset_utm)
            self.assertIsInstance(dem_sensors_geo, np.ndarray)
            self.assertEqual(dem_sensors_geo.shape, (150, 1000,  2))
            self.assertEqual(self.data_map_geo_3D.dtype, dem_sensors_geo.dtype)

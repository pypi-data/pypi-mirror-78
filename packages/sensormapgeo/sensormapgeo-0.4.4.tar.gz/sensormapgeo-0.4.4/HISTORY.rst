=======
History
=======

0.4.4 (2020-09-04)
------------------

* Fixed issue #6 (Deadlock within SensorMapGeometryTransformer3D when running in multiprocessing for resampling
  algorithms 'near' and 'gauss'.)
* Added pebble to pip requirements.


0.4.3 (2020-09-02)
------------------

* create_area_def() now gets an EPSG string from sensormapgeo instead of a PROJ4 dictionary to get rid of the
  deprecated PROJ4 format.


0.4.2 (2020-09-01)
------------------

* Some adjustments to recent changes in py_tools_ds and pyproj.
* Added pyproj as direct dependency to requirements.


0.4.1 (2020-08-17)
------------------

* Fixed wrong import statement.
* Fixed numpy deprecation warning.


0.4.0 (2020-08-07)
------------------

* Revised the way how multiprocessing is called in the 3D transformer (replaced with pool.imap_unordered without
  initializer). This is as fast as before but has a much smaller memory consumption enabling the algorithm to also run
  on smaller machines while still highly benefiting from more CPUs. Fixes issue #5.


0.3.5 (2020-08-07)
------------------

* Fixed VisibleDeprecationWarning.


0.3.4 (2020-08-07)
------------------

* Fixed a NotADirectoryError on Windows, possibly due to race conditions.


0.3.3 (2020-05-08)
------------------

* Replaced workaround for warning with warnings.catch_warning.


0.3.2 (2020-05-08)
------------------

* Suppressed another warning coming from pyresample.


0.3.1 (2020-05-08)
------------------

* Fixed a warning coming from pyresample.


0.3.0 (2020-05-08)
------------------

* Converted all type hints to Python 3.6 style. Dropped Python 3.5 support. Fixed code duplicate.
* Split sensormapgeo module into transformer_2d and transformer_3d.
* SensorMapGeometryTransformer.compute_areadefinition_sensor2map() now directly uses pyresample instead of GDAL if the
  target resolution is given.
* SensorMapGeometryTransformer3D.to_map_geometry() now computes a common area definition only ONCE which saves
  computation time and increases stability.
* The computation of the common extent in 3D geolayers now works properly if target projection is not set to LonLat.
* Added paramter tgt_coordgrid to to_map_geometry methods to automatically move the output extent to a given coordinate
  grid.
* compute_areadefinition_sensor2map() now also adds 1 pixel around the output extent in the pyresample version just
  like in the GDAL version.
* Added some input validation.


0.2.2 (2020-03-10)
------------------

* Fix for always returning 0.1.0 when calling sensormapgeo.__version__.


0.2.1 (2020-03-10)
------------------

* Fix for always returning returning float64 output data type in case of bilinear resampling.
* Added output data type verification to tests.
* Fix for an exception if the output of get_proj4info() contains trailing white spaces
  (fixed by an update of py_tools_ds).
* Improved tests.
* Set channel priority to strict.
* Force libgdal to be installed from conda-forge.
* Fixed broken documentation link


0.2.0 (2020-01-06)
------------------

* Added continous integration.
* Updated readme file.
* Added PyPI release.


0.1.0 (2020-01-06)
------------------

* First release on GitLab.

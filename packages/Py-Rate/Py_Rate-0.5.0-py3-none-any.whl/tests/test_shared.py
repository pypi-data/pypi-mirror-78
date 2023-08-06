#   This Python module is part of the PyRate software package.
#
#   Copyright 2020 Geoscience Australia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
This Python module contains tests for the shared.py PyRate module.
"""
import os
import shutil
import sys
import tempfile
import pytest
from pathlib import Path
from itertools import product
from numpy import isnan, where, nan
from os.path import join, basename, exists
from stat import S_IRGRP, S_IWGRP, S_IWOTH, S_IROTH, S_IRUSR, S_IWUSR

import numpy as np
from numpy.testing import assert_array_equal
from osgeo import gdal
from osgeo.gdal import Open, Dataset, UseExceptions

from tests.common import SML_TEST_TIF, SML_TEST_DEM_TIF, TEMPDIR
from pyrate.core import shared, ifgconstants as ifc, config as cf, prepifg_helper, gamma
from pyrate.core.shared import dem_or_ifg
from pyrate import prepifg, conv2tif
from pyrate.configuration import Configuration, MultiplePaths
from pyrate.core.shared import Ifg, DEM, RasterException
from pyrate.core.shared import cell_size, _utm_zone

from tests import common

UseExceptions()

if not exists(SML_TEST_TIF):
    sys.exit("ERROR: Missing small_test data for unit tests\n")


class TestIfgTests:
    """Unit tests for the Ifg/interferogram class."""

    def setup_class(cls):
        cls.ifg = Ifg(join(SML_TEST_TIF, 'geo_060619-061002_unw.tif'))
        cls.ifg.open()
        cls.ifg.nodata_value = 0

    def test_headers_as_attr(self):
        for a in ['ncols', 'nrows', 'x_first', 'x_step',
                  'y_first', 'y_step', 'wavelength', 'first', 'second']:
            assert getattr(self.ifg, a) is not None

    def test_convert_to_nans(self):
        self.ifg.convert_to_nans()
        assert self.ifg.nan_converted

    def test_xylast(self):
        # ensure the X|Y_LAST header element has been created
        assert self.ifg.x_last == pytest.approx(150.9491667)
        assert self.ifg.y_last == pytest.approx(-34.23)

    def test_num_cells(self):
        # test cell size from header elements
        data = self.ifg.phase_band.ReadAsArray()
        ys, xs = data.shape
        exp_ncells = ys * xs
        assert exp_ncells == self.ifg.num_cells

    def test_shape(self):
        assert self.ifg.shape == self.ifg.phase_data.shape

    def test_nan_count(self):
        num_nan = 0
        for row in self.ifg.phase_data:
            for v in row:
                if isnan(v):
                    num_nan += 1
        if self.ifg.nan_converted:
            assert num_nan == self.ifg.nan_count
        else:
            assert num_nan == 0

    def test_phase_band(self):
        data = self.ifg.phase_band.ReadAsArray()
        assert data.shape == (72, 47)

    def test_nan_fraction(self):
        # NB: source data lacks 0 -> NaN conversion
        data = self.ifg.phase_data
        data = where(data == 0, nan, data) # fake 0 -> nan for the count below

        # manually count # nan cells
        nans = 0
        ys, xs = data.shape
        for y, x in product(range(ys), range(xs)):
            if isnan(data[y, x]):
                nans += 1
        del data

        num_cells = float(ys * xs)
        assert nans > 0
        assert nans <= num_cells
        assert nans / num_cells == self.ifg.nan_fraction

    def test_xy_size(self):
        assert ~ (self.ifg.ncols is None)
        assert ~ (self.ifg.nrows is None)

        # test with tolerance from base 90m cell
        # within 2% of cells over small?
        assert self.ifg.y_size > 88.0
        assert self.ifg.y_size < 92.0, 'Got %s' % self.ifg.y_size

        width = 76.9 # from nearby PyRate coords
        assert self.ifg.x_size > 0.97 * width  # ~3% tolerance
        assert  self.ifg.x_size < 1.03 * width

    def test_centre_latlong(self):
        lat_exp = self.ifg.y_first + \
                  (int(self.ifg.nrows / 2) * self.ifg.y_step)
        long_exp = self.ifg.x_first + \
                   (int(self.ifg.ncols / 2) * self.ifg.x_step)
        assert lat_exp == self.ifg.lat_centre
        assert long_exp == self.ifg.long_centre

    def test_centre_cell(self):
        assert self.ifg.x_centre == 23
        assert self.ifg.y_centre == 36

    def test_time_span(self):
        assert self.ifg.time_span == pytest.approx(0.287474332649)

    def test_wavelength(self):
        assert self.ifg.wavelength == pytest.approx(0.0562356424)


class TestIfgIOTests:

    def setup_method(self):
        self.ifg = Ifg(join(SML_TEST_TIF, 'geo_070709-070813_unw.tif'))
        self.header = join(common.SML_TEST_OBS, 'geo_070709-070813_unw.rsc')

    def test_open(self):
        assert self.ifg.dataset is None
        assert self.ifg.is_open is False
        self.ifg.open(readonly=True)
        assert self.ifg.dataset is not None
        assert self.ifg.is_open is True
        assert isinstance(self.ifg.dataset, Dataset)

        # ensure open cannot be called twice
        with pytest.raises(RasterException):
            self.ifg.open(True)

    def test_open_ifg_from_dataset(self):
        """
        Test showing open() can not be used for Ifg created with
        gdal.Dataset object as Dataset has already been read in
        """
        self.ifg.open()
        dataset = self.ifg.dataset
        new_ifg = Ifg(dataset)
        with pytest.raises(RasterException):
            new_ifg.open()

    def test_write(self):
        base = TEMPDIR
        src = self.ifg.data_path
        dest = join(base, basename(self.ifg.data_path))

        # shutil.copy needs to copy writeable permission from src
        os.chmod(src, S_IRGRP | S_IWGRP | S_IWOTH | S_IROTH |
                 S_IRUSR | S_IWUSR)
        shutil.copy(src, dest)
        os.chmod(src, S_IRGRP | S_IROTH | S_IRUSR)  # revert

        i = Ifg(dest)
        i.open()
        i.phase_data[0, 1:] = nan
        i.write_modified_phase()
        del i

        # reopen to ensure data/nans can be read back out
        i = Ifg(dest)
        i.open(readonly=True)
        assert_array_equal(True, isnan(i.phase_data[0, 1:]))
        i.close()
        os.remove(dest)

    def test_write_fails_on_readonly(self):
        # check readonly status is same before
        # and after open() for readonly file
        assert self.ifg.is_read_only
        self.ifg.open(readonly=True)
        assert self.ifg.is_read_only
        with pytest.raises(IOError):
            self.ifg.write_modified_phase()

    def test_phase_band_unopened_ifg(self):
        try:
            _ = self.ifg.phase_band
            self.fail("Should not be able to access band without open dataset")
        except RasterException:
            pass

    def test_nan_fraction_unopened(self):
        try:
            # NB: self.assertRaises doesn't work here (as it is a property?)
            _ = self.ifg.nan_fraction
            self.fail("Shouldn't be able to "
                      "call nan_fraction() with unopened Ifg")
        except RasterException:
            pass

    def test_phase_data_properties(self):
        # Use raw GDAL to isolate raster reading from Ifg functionality
        ds = Open(self.ifg.data_path)
        data = ds.GetRasterBand(1).ReadAsArray()
        del ds

        self.ifg.open()

        # test full array and row by row access
        assert_array_equal(data, self.ifg.phase_data)
        for y, row in enumerate(self.ifg.phase_rows):
            assert_array_equal(data[y], row)

        # test the data is cached if changed
        crd = (5, 4)
        orig = self.ifg.phase_data[crd]
        self.ifg.phase_data[crd] *= 2
        nv = self.ifg.phase_data[crd]  # pull new value out again
        assert nv == 2 * orig


# FIXME:
# class IncidenceFileTests():
#     'Unit tests to verify operations on GeoTIFF format Incidence rasters'
#
#     def setUp(self):
#         raise NotImplementedError
#         self.inc = Incidence(join(INCID_TEST_DIR, '128x2.tif'))
#         self.inc.open()
#
#
#     def test_incidence_data(self):
#         # check incidences rises while traversing the scene
#         data = self.inc.incidence_data
#         diff = data.ptp()
#         self.assertTrue(diff > 0.5, "Got ptp() diff of %s" % diff)
#
#         # ascending pass, values should increase from W->E across scene
#         for i in range(2):
#             d = data[i]
#             self.assertFalse((d == 0).any()) # ensure no NODATA
#             self.assertFalse((isnan(d)).any())
#
#             diff = array([d[i+1] - d[i] for i in range(len(d)-1)])
#             res = abs(diff[diff < 0])
# TODO: check if this is normal
#             self.assertTrue((res < 1e-4).all())
#
#
#     def test_azimuth_data(self):
#         # ensure azimuth is fairly constant
#
#         az = self.inc.azimuth_data
#         self.assertFalse((az == 0).all())
#         az = az[az != 0] # filter NODATA cells
#
#         # azimuth should be relatively constant
#         ptp = az.ptp()
#         self.assertTrue(ptp < 0.1, msg="min -> max diff is %s" % ptp)


class TestDEMTests:
    'Unit tests to verify operations on GeoTIFF format DEMs'

    def setup_method(self):
        self.ras = DEM(SML_TEST_DEM_TIF)

    def test_create_raster(self):
        # validate header path
        assert os.path.exists(self.ras.data_path)

    def test_headers_as_attr(self):
        self.ras.open()
        attrs = ['ncols', 'nrows', 'x_first', 'x_step', 'y_first', 'y_step' ]

        # TODO: are 'projection' and 'datum' attrs needed?
        for a in attrs:
            assert getattr(self.ras, a) is not None

    def test_is_dem(self):
        self.ras = DEM(join(SML_TEST_TIF, 'geo_060619-061002_unw.tif'))
        assert  ~hasattr(self.ras, 'datum')

    def test_open(self):
        assert self.ras.dataset is None
        self.ras.open()
        assert self.ras.dataset is not None
        assert isinstance(self.ras.dataset, Dataset)

        # ensure open cannot be called twice
        with pytest.raises(RasterException):
            self.ras.open()

    def test_band_fails_with_unopened_raster(self):
        # test accessing bands with open and unopened datasets
        with pytest.raises(RasterException):
            self.ras.height_band

    def test_band_read_with_open_raster(self):
        self.ras.open()
        data = self.ras.height_band.ReadAsArray()
        assert data.shape == (72, 47)


class TestWriteUnw:

    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls, gamma_params):
        # change the required params
        shutil.rmtree(gamma_params[cf.OUT_DIR])  # start with a clean directory
        shared.mkdir_p(gamma_params[cf.OUT_DIR])
        cls.params = gamma_params
        cls.params[cf.OBS_DIR] = common.SML_TEST_GAMMA
        cls.params[cf.PROCESSOR] = 1  # gamma
        cls.params[cf.PARALLEL] = 0
        cls.params[cf.REF_EST_METHOD] = 1
        cls.params[cf.DEM_FILE] = common.SML_TEST_DEM_GAMMA
        # base_unw_paths need to be geotiffed and multilooked by run_prepifg
        cls.base_unw_paths = cf.original_ifg_paths(cls.params[cf.IFG_FILE_LIST], cls.params[cf.OBS_DIR])
        cls.base_unw_paths.append(common.SML_TEST_DEM_GAMMA)

        # dest_paths are tifs that have been geotif converted and multilooked
        conv2tif.main(cls.params)
        prepifg.main(cls.params)

        cls.dest_paths = [Path(cls.params[cf.OUT_DIR]).joinpath(Path(c.sampled_path).name).as_posix()
                          for c in cls.params[cf.INTERFEROGRAM_FILES][:-2]]
        cls.ifgs = [dem_or_ifg(i) for i in cls.dest_paths]
        for i in cls.ifgs:
            i.open()
            i.nodata_value = 0

    @classmethod
    def teardown_class(cls):
        """auto cleaning on"""

    def test_unw_contains_same_data_as_numpy_array(self):
        from datetime import time
        temp_unw = tempfile.mktemp(suffix='.unw')
        temp_tif = tempfile.mktemp(suffix='.tif')

        # setup some header files for use in write_geotif
        dem_header_file = common.SML_TEST_DEM_HDR_GAMMA
        dem_header = gamma.parse_dem_header(dem_header_file)

        header = gamma.parse_epoch_header(
            os.path.join(common.SML_TEST_GAMMA, '20060828_slc.par'))
        header.update(dem_header)

        # insert some dummy data so we are the dem in write_fullres_geotiff is not
        # not activated and ifg write_fullres_geotiff operation works
        header[ifc.PYRATE_TIME_SPAN] = 0
        header[ifc.SECOND_DATE] = 0
        header[ifc.DATA_UNITS] = 'degrees'
        header[ifc.DATA_TYPE] = ifc.ORIG
        header[ifc.SECOND_TIME] = time(10)

        # now create aritrary data
        data = np.random.rand(dem_header[ifc.PYRATE_NROWS], dem_header[ifc.PYRATE_NCOLS])

        # convert numpy array to .unw
        shared.write_unw_from_data_or_geotiff(geotif_or_data=data, dest_unw=temp_unw, ifg_proc=1)
        # convert the .unw to geotif
        shared.write_fullres_geotiff(header=header, data_path=temp_unw, dest=temp_tif, nodata=np.nan)

        # now compare geotiff with original numpy array
        ds = gdal.Open(temp_tif, gdal.GA_ReadOnly)
        data_lv_theta = ds.ReadAsArray()
        ds = None
        np.testing.assert_array_almost_equal(data, data_lv_theta)
        try:
            os.remove(temp_tif)
        except PermissionError:
            print("File opened by another process.")

        try:
            os.remove(temp_unw)
        except PermissionError:
            print("File opened by another process.")

    def test_multilooked_tiffs_converted_to_unw_are_same(self):
        # Get multilooked geotiffs
        geotiffs = list(set(self.dest_paths))
        geotiffs = [g for g in geotiffs if 'dem' not in g]

        # Convert back to .unw
        dest_unws = []
        for g in set(geotiffs):
            dest_unw = os.path.join(self.params[cf.OUT_DIR], Path(g).stem + '.unw')
            shared.write_unw_from_data_or_geotiff(geotif_or_data=g, dest_unw=dest_unw, ifg_proc=1)
            dest_unws.append(dest_unw)

        dest_unws_ = []

        for d in dest_unws:
            dest_unws_.append(MultiplePaths(d, self.params))

        # Convert back to tiff
        new_geotiffs_ = conv2tif.do_geotiff(dest_unws_, self.params)
        new_geotiffs = [gt for gt, b in new_geotiffs_]

        # Ensure original multilooked geotiffs and 
        #  unw back to geotiff are the same
        geotiffs.sort()
        new_geotiffs.sort()
        for g, u in zip(geotiffs, new_geotiffs):
            g_ds = gdal.Open(g)
            u_gs = gdal.Open(u)
            np.testing.assert_array_almost_equal(u_gs.ReadAsArray(), g_ds.ReadAsArray())
            u_gs = None
            g_ds = None

    def test_roipac_raises(self):
        geotiffs = [os.path.join(
            self.params[cf.OUT_DIR], os.path.basename(b).split('.')[0] + '_' 
            + os.path.basename(b).split('.')[1] + '.tif')
            for b in self.base_unw_paths]

        for g in geotiffs[:1]:
            dest_unw = os.path.join(self.params[cf.OUT_DIR], os.path.splitext(g)[0] + '.unw')
            with pytest.raises(NotImplementedError):
                shared.write_unw_from_data_or_geotiff(geotif_or_data=g, dest_unw=dest_unw, ifg_proc=0)


class TestGeodesy:

    def test_utm_zone(self):
        # test some different zones (collected manually)
        for lon in [174.0, 176.5, 179.999, 180.0]:
            assert 60 == _utm_zone(lon)

        for lon in [144.0, 144.1, 146.3456, 149.9999]:
            assert 55 == _utm_zone(lon)

        for lon in [-180.0, -179.275, -176.925]:
            assert 1 == _utm_zone(lon)

        for lon in [-72.0, -66.1]:
            assert 19 == _utm_zone(lon)

        for lon in [0.0, 0.275, 3.925, 5.999]:
            assert 31 == _utm_zone(lon)

    def test_cell_size_polar_region(self):
        # Can't have polar area zones: see http://www.dmap.co.uk/utmworld.htm
        for lat in [-80.1, -85.0, -90.0, 84.1, 85.0, 89.9999, 90.0]:
            with pytest.raises(ValueError):
                cell_size(lat, 0, 0.1, 0.1)

    def test_cell_size_calc(self):
        # test conversion of X|Y_STEP to X|Y_SIZE
        x_deg = 0.000833333
        y_deg = -x_deg

        approx = 90.0 # x_deg is approx 90m
        exp_low = approx - (.15 * approx) # assumed tolerance
        exp_high = approx + (.15 * approx)

        latlons = [(10.0, 15.0), (-10.0, 15.0), (10.0, -15.0), (-10.0, -15.0),
            (178.0, 33.0), (-178.0, 33.0), (178.0, -33.0), (-178.0, -33.0) ]

        for lon, lat in latlons:
            xs, ys = cell_size(lat, lon, x_deg, y_deg)
            for s in (xs, ys):
                assert s > 0, "size=%s" % s
                assert s > exp_low, "size=%s" % s
                assert s < exp_high, "size=%s" % s

# coding: utf-8
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
This Python module contains tests for mpi operations in PyRate.
Tun this module as 'mpirun -n 4 pytest tests/test_mpi.py'
"""
import shutil
import numpy as np
import os
from pathlib import Path

import pyrate.configuration
import pyrate.core.covariance
import pyrate.core.orbital
import pyrate.core.ref_phs_est
import pyrate.core.refpixel
from pyrate import correct, prepifg, conv2tif, configuration
from pyrate.core import mpiops, config as cf
from tests import common
from tests.common import SML_TEST_DIR
from tests.test_covariance import legacy_maxvar


def test_vcm_legacy_vs_mpi(mpisync, tempdir, roipac_or_gamma_conf):

    params = configuration.Configuration(roipac_or_gamma_conf).__dict__
    LEGACY_VCM_DIR = os.path.join(SML_TEST_DIR, 'vcm')
    legacy_vcm = np.genfromtxt(os.path.join(LEGACY_VCM_DIR, 'vcmt.csv'), delimiter=',')
    tmpdir = Path(mpiops.run_once(tempdir))
    mpiops.run_once(common.copytree, params[cf.OBS_DIR], tmpdir)
    params[cf.OUT_DIR] = tmpdir.joinpath('out')
    params[cf.PARALLEL] = 0
    output_conf = Path(tmpdir).joinpath('conf.cfg')
    pyrate.configuration.write_config_file(params=params, output_conf_file=output_conf)
    params = configuration.Configuration(output_conf).__dict__

    # dest_paths = [p.sampled_path for p in params[cf.INTERFEROGRAM_FILES]]
    # run conv2tif and prepifg, create the dest_paths files
    conv2tif.main(params)
    params = configuration.Configuration(output_conf).__dict__
    prepifg.main(params)
    params = configuration.Configuration(output_conf).__dict__
    params[cf.ORBFIT_OFFSET] = True
    correct._copy_mlooked(params=params)
    correct._update_params_with_tiles(params)
    correct._create_ifg_dict(params=params)
    pyrate.core.refpixel.ref_pixel_calc_wrapper(params)
    pyrate.core.orbital.orb_fit_calc_wrapper(params)
    pyrate.core.ref_phs_est.ref_phase_est_wrapper(params)

    maxvar, vcmt = pyrate.core.covariance.maxvar_vcm_calc_wrapper(params)

    # phase data after ref pixel has changed due to commit bf2f7ebd
    # Legacy tests won't match anymore
    np.testing.assert_array_almost_equal(maxvar, legacy_maxvar, decimal=4)
    np.testing.assert_array_almost_equal(legacy_vcm, vcmt, decimal=3)
    mpiops.run_once(shutil.rmtree, tmpdir)

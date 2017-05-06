from __future__ import division, print_function, absolute_import

import numpy as np
import numpy.testing as npt

from distutils.version import LooseVersion
from dipy.reconst.peaks import PeaksAndMetrics
from nibabel.tmpdirs import InTemporaryDirectory

# Conditional import machinery for pytables
from dipy.utils.optpkg import optional_package

# Allow import, but disable doctests, if we don't have pytables
tables, have_tables, _ = optional_package('tables')

from dipy.data import get_sphere
from dipy.core.sphere import Sphere

from dipy.io.peaks import load_peaks, save_peaks

# Decorator to protect tests from being run without pytables present
iftables = npt.dec.skipif(not have_tables,
                          'Pytables does not appear to be installed')


@iftables
def test_io_peaks():

    with InTemporaryDirectory():

        fname = 'test.pam5'

        sphere = get_sphere('repulsion724')

        pam = PeaksAndMetrics()
        pam.affine = np.eye(4)
        pam.peak_dirs = np.random.rand(10, 10, 10, 5, 3)
        pam.peak_values = np.zeros((10, 10, 10, 5))
        pam.peak_indices = np.zeros((10, 10, 10, 5))
        pam.shm_coeff = np.zeros((10, 10, 10, 45))
        pam.sphere = sphere
        pam.B = np.zeros((45, sphere.vertices.shape[0]))
        pam.total_weight = 0.5
        pam.ang_thr = 60
        pam.gfa = np.zeros((10, 10, 10))
        pam.qa = np.zeros((10, 10, 10, 5))
        pam.odf = np.zeros((10, 10, 10, sphere.vertices.shape[0]))

        save_peaks(fname, pam)
        pam2 = load_peaks(fname, verbose=True)
        npt.assert_array_equal(pam.peak_dirs, pam2.peak_dirs)

        pam2.affine = None

        fname2 = 'test2.pam5'
        save_peaks(fname2, pam2)

        pam3 = load_peaks(fname2, verbose=False)
        npt.assert_equal(pam3.total_weight, pam.total_weight)
        npt.assert_equal(pam3.ang_thr, pam.ang_thr)
        npt.assert_equal(pam3.gfa, pam.gfa)
        npt.assert_equal(pam3.qa, pam.qa)
        npt.assert_equal(pam3.odf, pam.odf)

        fname3 = 'test3.pam5'
        pam4 = PeaksAndMetrics()
        npt.assert_raises(ValueError, save_peaks, fname3, pam4)

        fname4 = 'test4.pam5'
        del pam.affine
        save_peaks(fname4, pam, affine=None)

        fname5 = 'test5.pkm'
        npt.assert_raises(IOError, save_peaks, fname5, pam)

        pam.affine = np.eye(4)
        fname6 = 'test6.pam5'
        save_peaks(fname6, pam, verbose=True)

        del pam.shm_coeff
        save_peaks(fname6, pam, verbose=False)

        pam.shm_coeff = np.zeros((10, 10, 10, 45))
        del pam.odf
        save_peaks(fname6, pam)
        pam_tmp = load_peaks(fname6, True)
        npt.assert_equal(pam_tmp.odf, None)


if __name__ == '__main__':

    npt.run_module_suite()

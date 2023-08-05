import os
import unittest
from os.path import abspath, isfile, join

from netCDF4 import Dataset

import spatialnc as spnc
from spatialnc.utilities import *


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUp(self):
        topo_f = abspath(join(spnc.__file__, '..', '..',
                              'tests', 'data', 'topo.nc'))
        self.topo = Dataset(topo_f)

    @classmethod
    def tearDown(self):
        self.topo.close()

    def check_copy_nc(self, keep=None):
        '''
        A small func to test copy nc with and with out the excludes
        '''

        # Exclude all variables except dimensions
        if keep is not None:
            ex_var = [v for v in self.topo.variables if v.lower() not in keep]
        else:
            ex_var = None

        # Copy over x,y, and projection
        d = copy_nc(self.topo, 'test.nc', exclude=ex_var)

        if keep is not None:
            self.assertTrue(len(keep) == len(d.variables.keys()))
            for v in keep:
                self.assertTrue(v in d.variables.keys())

        out_f = d.filepath()
        d.close()

        # Clean up
        if isfile(out_f):
            os.remove(out_f)

    def test_copy_nc_w_exclude(self):
        '''
        Test whether we can copy a netcdf
        '''
        keep = ['x', 'y', 'projection']
        self.check_copy_nc(keep=keep)

    def test_copy_nc_wo_exclude(self):
        '''
        Test whether we can copy a whole netcdf over with no exclude
        '''
        self.check_copy_nc()

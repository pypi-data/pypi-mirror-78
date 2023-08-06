#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains tests for 'sicor_enmap' module.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from unittest import TestCase
import logging
import sys
import os
import tempfile
import zipfile
import pkgutil
import numpy as np
import dill

from enpt.io.reader import L1B_Reader
from enpt.options.config import EnPTConfig, config_for_testing

from sicor.options.options import get_options
from sicor.sicor_enmap import sicor_ac_enmap
from sicor.Tools.EnMAP.LUT import interpol_lut_c
from sicor.AC.RtFo_3_phases import Fo


class TestSicor_EnMAP_FO(TestCase):
    def setUp(self):
        self.logger = logging.Logger("EnMAP")
        fmt_suffix = None
        formatter_ConsoleH = logging.Formatter('%(asctime)s' + (' [%s]' % fmt_suffix if fmt_suffix else '') +
                                               ':   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        consoleHandler_out = logging.StreamHandler(stream=sys.stdout)
        consoleHandler_out.setFormatter(formatter_ConsoleH)
        self.logger.addHandler(consoleHandler_out)

        path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
        path_options_default = os.path.join(path_sicorlib, 'options', 'enmap_options.json')

        self.options = get_options(path_options_default, validation=False)

        print("")
        print("################################################")
        print("#                                              #")
        print("# Test reading EnMAP Level-1B product          #")
        print("#                                              #")
        print("################################################")
        print("")
        print("")

        config = EnPTConfig(**config_for_testing)
        pathList_testimages = [config.path_l1b_enmap_image, config.path_l1b_enmap_image_gapfill]
        tmpdir = tempfile.mkdtemp(dir=config.working_dir)

        for l1b_file in pathList_testimages:
            with zipfile.ZipFile(l1b_file, "r") as zf:
                zf.extractall(tmpdir)
        prods = [os.path.join(tmpdir, os.path.basename(pathList_testimages[0]).split(".zip")[0]),
                 os.path.join(tmpdir, os.path.basename(pathList_testimages[1]).split(".zip")[0])]

        rd = L1B_Reader(config=config)

        L1_obj = rd.read_inputdata(prods[0], compute_snr=False)

        print("Done!")
        print("")
        print("")

        self.enmap_l1b = L1_obj

    def test_fo_enmap(self):
        print("")
        print("################################################")
        print("#                                              #")
        print("# Test instantiating forward operator          #")
        print("#                                              #")
        print("################################################")
        print("")
        print("")
        Fo(self.enmap_l1b, self.options, logger=self.logger)
        print("Done!")
        print("")
        print("")


class TestSicor_EnMAP_AC(TestCase):
    def setUp(self):
        self.logger = logging.Logger("EnMAP")
        fmt_suffix = None
        formatter_ConsoleH = logging.Formatter('%(asctime)s' + (' [%s]' % fmt_suffix if fmt_suffix else '') +
                                               ':   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        consoleHandler_out = logging.StreamHandler(stream=sys.stdout)
        consoleHandler_out.setFormatter(formatter_ConsoleH)
        self.logger.addHandler(consoleHandler_out)

        path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
        path_options_default = os.path.join(path_sicorlib, 'options', 'enmap_options.json')

        self.options = get_options(path_options_default, validation=False)

        print("")
        print("################################################")
        print("#                                              #")
        print("# Test reading EnMAP Level-1B product          #")
        print("#                                              #")
        print("################################################")
        print("")
        print("")

        config = EnPTConfig(**config_for_testing)
        pathList_testimages = [config.path_l1b_enmap_image, config.path_l1b_enmap_image_gapfill]
        tmpdir = tempfile.mkdtemp(dir=config.working_dir)

        for l1b_file in pathList_testimages:
            with zipfile.ZipFile(l1b_file, "r") as zf:
                zf.extractall(tmpdir)
        prods = [os.path.join(tmpdir, os.path.basename(pathList_testimages[0]).split(".zip")[0]),
                 os.path.join(tmpdir, os.path.basename(pathList_testimages[1]).split(".zip")[0])]

        rd = L1B_Reader(config=config)

        L1_obj = rd.read_inputdata(prods[0], compute_snr=False)

        L1_obj.get_preprocessed_dem()

        print("Done!")
        print("")
        print("")

        self.enmap_l1b = L1_obj

    def test_ac_enmap(self):
        print("")
        print("################################################")
        print("#                                              #")
        print("# Test EnMAP atmospheric correction            #")
        print("#                                              #")
        print("################################################")
        print("")
        print("")
        sicor_ac_enmap(self.enmap_l1b, self.options, logger=self.logger)
        print("Done!")
        print("")
        print("")


class TestSicor_EnMAP_interpol_LUT(TestCase):
    def setUp(self):
        path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
        testcase = os.path.abspath(os.path.join(path_sicorlib, "..", "tests", "data", "EnMAP",
                                                "interpol_testcase.dill"))

        with open(testcase, "rb") as fl:
            lut1_fit, lut2_fit, xnodes, nm_nodes, ndim, x_cell, pt, cwv_model, wvl_sel = dill.load(fl)

        self.lut1_fit = lut1_fit
        self.lut2_fit = lut2_fit
        self.xnodes = xnodes
        self.nm_nodes = nm_nodes
        self.ndim = np.int(ndim)
        self.x_cell = x_cell
        self.pt = pt[0, 0, :]
        self.xx = cwv_model[0, 0]
        self.wvl_sel = wvl_sel

        self.vtest = np.append(self.pt, self.xx)

    def test_interpol_LUT_numba(self):
        print("")
        print("################################################")
        print("#                                              #")
        print("# Test LUT interpolation using numba           #")
        print("#                                              #")
        print("################################################")
        print("")
        print("")
        interpol_lut_c(lut1=self.lut1_fit, lut2=self.lut2_fit, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                       ndim=self.ndim, x_cell=self.x_cell, vtest=self.vtest, intp_wvl=self.wvl_sel)
        print("Done!")
        print("")
        print("")

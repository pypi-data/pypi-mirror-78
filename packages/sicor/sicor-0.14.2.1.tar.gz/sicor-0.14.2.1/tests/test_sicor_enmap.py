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

from enpt.io.reader import L1B_Reader
from enpt.options.config import EnPTConfig, config_for_testing_dlr

from sicor.options.options import get_options
from sicor.sicor_enmap import sicor_ac_enmap


class LessThanFilter(logging.Filter):
    """Filter class to filter log messages by a maximum log level. Adapted from EnPT.enpt.utils.logging.py.

    Based on http://stackoverflow.com/questions/2302315/
        how-can-info-and-debug-logging-message-be-sent-to-stdout-and-higher-level-message
    """

    def __init__(self, exclusive_maximum, name=""):
        """Get an instance of LessThanFilter.

        :param exclusive_maximum:  maximum log level, e.g., logger.WARNING
        :param name:
        """
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        """Filter funtion.

        NOTE: Returns True if logging level of the given record is below the maximum log level.

        :param record:
        :return: bool
        """
        # non-zero return means we log this message
        return True if record.levelno < self.max_level else False


class TestSicor_EnMAP_AC_DLR(TestCase):
    def setUp(self):
        self.logger = logging.Logger("EnMAP")
        fmt_suffix = None
        formatter_ConsoleH = logging.Formatter('%(asctime)s' + (' [%s]' % fmt_suffix if fmt_suffix else '') +
                                               ':   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

        # create ConsoleHandler for logging levels DEGUG and INFO -> logging to sys.stdout
        consoleHandler_out = logging.StreamHandler(stream=sys.stdout)  # by default it would go to sys.stderr
        consoleHandler_out.setFormatter(formatter_ConsoleH)
        consoleHandler_out.set_name('console handler stdout')
        consoleHandler_out.setLevel("INFO")
        consoleHandler_out.addFilter(LessThanFilter(logging.WARNING))

        # create ConsoleHandler for logging levels WARNING, ERROR, CRITICAL -> logging to sys.stderr
        consoleHandler_err = logging.StreamHandler(stream=sys.stderr)
        consoleHandler_err.setFormatter(formatter_ConsoleH)
        consoleHandler_err.setLevel(logging.WARNING)
        consoleHandler_err.set_name('console handler stderr')

        self.logger.addHandler(consoleHandler_out)
        self.logger.addHandler(consoleHandler_err)

        path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
        path_options_default = os.path.join(path_sicorlib, 'options', 'enmap_options.json')

        self.options = get_options(path_options_default, validation=True)

        print("")
        print("################################################")
        print("#                                              #")
        print("# Test reading EnMAP Level-1B product          #")
        print("#                                              #")
        print("################################################")
        print("")
        print("")

        config = EnPTConfig(**config_for_testing_dlr)
        pathList_testimages = [config.path_l1b_enmap_image, config.path_l1b_enmap_image_gapfill]
        tmpdir = tempfile.mkdtemp(dir=config.working_dir)

        print(pathList_testimages[0])

        with zipfile.ZipFile(pathList_testimages[0], "r") as zf:
            zf.extractall(tmpdir)

        RD = L1B_Reader(config=config)

        L1_obj = RD.read_inputdata(tmpdir, compute_snr=False)

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
        enmap_l2a_vnir, enmap_l2a_swir, cwv_model, cwc_model, ice_model, toa_model, se, scem, sre = sicor_ac_enmap(
            self.enmap_l1b, self.options, logger=self.logger)

        try:
            assert enmap_l2a_vnir[np.isfinite(enmap_l2a_vnir)].shape[0] > 0
            assert enmap_l2a_swir[np.isfinite(enmap_l2a_swir)].shape[0] > 0
        except AssertionError:
            raise AssertionError("Atmospheric correction failed. L2A data of at least one detector contain only NaN. "
                                 "Please check for errors in the input data, the options file, or the processing code.")

        print("Done!")
        print("")
        print("")

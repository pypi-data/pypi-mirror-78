#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sicor
----------------------------------

Tests for `sicor` module.
"""

import unittest
import json
import dill
import sys
from os import path, sep
import tempfile
import zipfile
import os
from glob import glob
import logging
import numpy as np
import importlib
from time import time
from scipy.interpolate import RegularGridInterpolator
from itertools import product
from mock import patch
import matplotlib.pyplot as plt
import h5py
from datetime import datetime
import subprocess
import gdal


from sicor import tables
from sicor import options
from sicor import get_options
from sicor import ac_gms
from sicor import ac
from sicor.sensors import S2MSI
from sicor.sensors.S2MSI import S2Image
from sicor.sicor import IO

from sicor.sensors import SensorSRF
from sicor.options import python_to_json
from sicor.ECMWF import ECMWF_variable
from sicor.sicor import get_ecmwf_data
from sicor.tables import get_tables
from sicor.Tools import SolarIrradiance
from sicor.Tools.NM import interpolate_n

range_interp_spectral_n = (1, 3)


def comp(aa, bb, key_chain, max_delta=0.01, logger=None):
    """Compare values in two dicts aa and bb
    :param aa: dictionary
    :param bb: dictionary
    :param key_chain: iterable of dict keys to compare, e.g ('key1','key2')
    :param max_delta: if differences are larger than max_delta raise an Assertation error
    :param logger: None or logging instance
    """
    logger = logger or logging.getLogger(__name__)

    try:
        for key in key_chain:
            aa = aa[key]
            bb = bb[key]
    except KeyError:
        logger.info("Error in %s" % str(key_chain))
        raise
    try:
        assert np.all(np.abs(np.array(aa, dtype=np.float) - np.array(bb, dtype=np.float)) < max_delta)
    except AssertionError:
        logger.info("Deviations detected in: %s" % str(key_chain))
        raise
    else:
        logger.info("All good in: %s" % str(key_chain))


class TestSicor(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        print("Klaus")

    def test_ecmwf_get_ecmwf_data(self):
        base_path = path.join(path.dirname(__file__), "data", "ecmwf")
        ecmwf_data_file = path.join(base_path, "ecmwf.zip")
        l1c_file = path.join(
            path.dirname(__file__),
            "data", "s2a_l1c", "S2A_MSIL1C_20170430T103021_N0205_R108_T32UPV_20170430T103024.SAFE.zip")

        with tempfile.TemporaryDirectory() as tmpdir:
            print("Tmp dir: %s" % tmpdir)
            with zipfile.ZipFile(ecmwf_data_file, "r") as zf:
                zf.extractall(tmpdir)

            with zipfile.ZipFile(l1c_file, "r") as zf:
                zf.extractall(tmpdir)

            image = S2Image(granule_path=path.join(
                tmpdir, "S2A_MSIL1C_20170430T103021_N0205_R108_T32UPV_20170430T103024.SAFE", "GRANULE",
                "L1C_T32UPV_A009686_20170430T103024"))

            # allow 1000 days to g back in time
            options = {"ECMWF": {
                "path_db": path.join(tmpdir, "ecmwf"),
                "max_delta_day": 10000, "target_resolution": 20}}
            get_ecmwf_data(variable="fc_O3", image=image, options=options)
            # allow only 10 days to go back in time, for the test case nothing can be found and an OSError is raised
            options = {"ECMWF": {"path_db": path.join(tmpdir, "ecmwf"), "max_delta_day": 10, "target_resolution": 20}}
            self.assertRaises(OSError, get_ecmwf_data, variable="fc_O3", image=image, options=options)

    def test_ecmwf_read_data_from_database(self):
        default_products = [
            "fc_T2M",
            "fc_O3",
            "fc_SLP",
            "fc_TCWV",
            "fc_GMES_ozone",
            "fc_total_AOT_550nm",
            "fc_sulphate_AOT_550nm",
            "fc_black_carbon_AOT_550nm",
            "fc_dust_AOT_550nm",
            "fc_organic_matter_AOT_550nm",
            "fc_sea_salt_AOT_550nm"]

        base_path = path.join(path.dirname(__file__), "data", "ecmwf")

        ecmwf_data_file = path.join(base_path, "ecmwf.zip")
        ecmef_integration_test_data = path.join(base_path, "ecmwf_integration_test_data.h5")
        create_reference_file = False

        with tempfile.TemporaryDirectory() as tmpdir:
            print("Tmp dir: %s" % tmpdir)
            with zipfile.ZipFile(ecmwf_data_file, "r") as zf:
                zf.extractall(tmpdir)

            reference_results = {}
            for product_name in default_products:
                print("Get ecmef data: %s" % product_name)
                var = ECMWF_variable(variable=product_name, path_db=path.join(tmpdir, "ecmwf"),
                                     var_date=datetime(2015, 12, 7, 12, 0))
                lons, lats = np.linspace(0, 359, 360), np.linspace(80, -80, 180)
                lons2D, lats2D = np.meshgrid(lons, lats)
                step = 20
                shape = None
                reference_results[product_name] = var(step=step, lons=lons2D, lats=lats2D, shape=shape)

        if create_reference_file is True:
            with h5py.File(ecmef_integration_test_data, "w") as h5f:
                for name, value in reference_results.items():
                    print(name)
                    h5f.create_dataset(name=name, data=value)

            nx, ny = int(np.ceil(len(reference_results.keys()) / 3)), 3
            fig = plt.figure(figsize=(15, 15))

            for ii, (product_name, value) in enumerate(reference_results.items(), 1):
                ax = plt.subplot(nx, ny, ii)
                im = ax.imshow(value, cmap=plt.cm.Oranges)
                ax.set_title(product_name)
                fig.colorbar(im, ax=ax)
            fig.tight_layout()
            plt.savefig(ecmef_integration_test_data + ".jpg")

        else:
            with h5py.File(ecmef_integration_test_data, "r") as h5f:
                for name, value in reference_results.items():
                    delta = np.sum(np.abs(value - h5f[name]))
                    print(name, delta)
                    assert delta < 10 ** -6

    def test_sicor_Tools_NM_interp_spectral_n_X(self):
        n_spectral = 3
        for n_interp in range(*range_interp_spectral_n):
            t0 = time()
            intp = importlib.import_module("sicor.Tools.NM.interp_spectral_n_%i" % n_interp)

            def test_pt(pt, log=False):
                pt = np.array(pt)
                t0 = time()
                ff_erg = np.array([ff(np.hstack((pt, np.array([ss]))))[0] for ss in range(n_spectral)])
                t1 = time()

                ii_erg = ii(pt)[0] if jacobean is True else ii(pt)
                t2 = time()

                if log is True:
                    print("### timings: RG:%.4f,This:%.4f,RG/THIS:%.2f" % (t1 - t0, t2 - t1, (t1 - t0) / (t2 - t1)))
                    print("Test:", len(pt) * "%.2f," % tuple(pt))
                    print(ii_erg)
                    print(ff_erg)
                    print("Difference:", len(ii_erg) * "%.5f," % tuple(np.array(ii_erg) - np.array(ff_erg)))

                if np.sum(ii_erg - ff_erg) > 1e-5 or np.isnan(np.sum(ii_erg - ff_erg)):
                    print("Test Failed!")
                    print(ii_erg)
                    print(ff_erg)
                    print("Difference:", len(ii_erg) * "%.5f," % tuple(np.array(ii_erg) - np.array(ff_erg)))
                    raise ValueError()

            print("Test dim: %i" % n_interp)
            shape = n_interp * [2] + [n_spectral]
            print("Test shape:", shape)
            data = np.random.random_sample(np.prod(shape)).reshape(shape)
            axes = [(lambda x: np.array([x[0], x[0] + x[1]]))(np.random.random(2)) for ii in range(n_interp)]
            axes_low = np.array([ax[0] for ax in axes])
            axes_high = np.array([ax[1] for ax in axes])
            print("Random axes:", axes)

            for jacobean in [True, False]:
                print("Jacobean:%s" % str(jacobean))
                ii = intp.intp(data, axes=axes, jacobean=jacobean)
                ff = RegularGridInterpolator(axes + [np.arange(n_spectral)], data)

                print("Test random points.")
                for _ in range(n_spectral):
                    pt = (axes_high - axes_low) * np.random.random_sample(n_interp) + axes_low
                    test_pt(pt)

                print("Test all axes corners.")
                t_c = time()
                for pt in product(*axes):
                    pt = np.array(pt)
                    test_pt(pt)
                    if time() - t_c > 20:
                        break

            print("sicor.Tools.NM.interp_spectral_n_%i:%.1fs" % (n_interp, time() - t0))
        print("Completed Test without errors, go ahead and happy spectral interpolating.")

    def test_srfs(self):
        for sensor in ["S2A", "Landsat-8"]:
            print("Read srf for: %s" % sensor)
            bf = SensorSRF(sensor=sensor)
            print(bf.srfs.keys())

        for sensor in ["Landsat-9", "Landsat-1", "klaus"]:
            with self.assertRaises(ValueError):
                SensorSRF(sensor=sensor)

        SensorSRF(sensor="S2A")["B01"]
        SensorSRF(sensor="Landsat-8")("1")

    def test_Tools_SolarIrradiance(self):
        for dataset in ["Thuillier2002", "Fontenla"]:
            solar = SolarIrradiance(dataset=dataset)
            assert len(solar.irr) == len(solar.wvl)

    def test_tables_get_tables(self):
        get_tables(optional_downloads=(
            # "ch4",
            # "hyperspectral_sample",
            # "s2_manual_classification",
        )
        )

    def test_read_l1c_sentinel_2_products(self):
        print("Test reading L1C data")
        for l1c_file in glob(path.join(path.dirname(__file__), "data", "s2a_l1c", "*.zip")):
            print(l1c_file)
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger("test_sicor")
            with tempfile.TemporaryDirectory() as tmpdir:
                print("Tmp dir: %s" % tmpdir)
                with zipfile.ZipFile(l1c_file, "r") as zf:
                    zf.extractall(tmpdir)

                for l1c_product in glob(os.path.join(tmpdir, "*.SAFE", "GRANULE", "*")):
                    print("Product: %s" % l1c_product)
                    img = S2Image(granule_path=l1c_product, logger=logger)
                    del img

    def test_ac_l1c_sentinel_2_products(self, save_new_expected_results=False):
        """Test in-python atmospheric correction for some test data: tests/data/s2a_l1c/*.zip
        :param save_new_expected_results: For each zipped L1c product write a corresponding json file with
        expected results. Actual results are compared to saved ones and in case of deviations an error is thrown.
        """
        print("Test ac on L1C data")
        sicor_table_path = os.path.dirname(tables.__file__)
        settings = os.path.join(os.path.dirname(options.__file__), "s2_options.json")
        opts = get_options(settings)
        opts['cld_mask']["persistence_file"] = os.path.join(
            sicor_table_path, os.path.basename(opts['cld_mask']["persistence_file"]))
        opts['cld_mask']["novelty_detector"] = os.path.join(
            sicor_table_path, os.path.basename(opts['cld_mask']["novelty_detector"]))
        opts["uncertainties"]["snr_model"] = os.path.join(
            os.path.dirname(S2MSI.__file__), "data", os.path.basename(opts["uncertainties"]["snr_model"]))
        for scat_type, op in opts["RTFO"].items():
            op['atm_tables_fn'] = os.path.join(sicor_table_path, os.path.basename(op['atm_tables_fn']))

        ecmwf_zip = path.join(path.dirname(__file__), "data", "ecmwf", "ecmwf.zip")

        for l1c_file in glob(path.join(path.dirname(__file__), "data", "s2a_l1c", "*.zip")):
            print(l1c_file)
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger("test_sicor")
            with tempfile.TemporaryDirectory() as tmpdir:
                print("Tmp dir: %s" % tmpdir)

                # extract test data to tmp dir
                with zipfile.ZipFile(l1c_file, "r") as zf:
                    zf.extractall(tmpdir)

                with zipfile.ZipFile(ecmwf_zip, "r") as zf:
                    zf.extractall(tmpdir)
                opts['ECMWF']["path_db"] = path.join(tmpdir, "ecmwf")

                # loop over l1c product and perform ac
                for l1c_product in glob(os.path.join(tmpdir, "*.SAFE", "GRANULE", "*")):
                    print("Product: %s" % l1c_product)
                    img = S2Image(granule_path=l1c_product, logger=logger)
                    img_ac = ac_gms(img, options=opts, logger=logger)
                    #
                    # write default processing output, only change / use this is you want to produce new ones -> you
                    # probably need to commit these json files to the repo
                    if save_new_expected_results is True:
                        with open(l1c_file.replace(".zip", ".json"), "w") as fl:
                            json.dump(opts['processing'], fl, indent=4)

                    # load to-be expected data from file and compare results
                    with open(l1c_file.replace(".zip", ".json"), "r") as fl:
                        expected_result = json.load(fl)

                    comp(expected_result, opts['processing'], ('clear_fraction',))
                    for metric in ('median_values', "std_values"):
                        for band in expected_result[metric].keys():
                            comp(expected_result, opts['processing'], (metric, band))

                    for band in expected_result['median_values'].keys():
                        comp(expected_result, opts['processing'], ('uncertainties', band, "coef"))

                    for band in expected_result["uncertainties"]['rfl_to_rad'].keys():
                        comp(expected_result, opts['processing'], ('uncertainties', 'rfl_to_rad', band))

                    for output_formats in opts["output"]:
                        print(output_formats['type'])
                        output_formats['out_dir'] = os.path.join(tmpdir, "L2A")
                        if output_formats['type'] == "metadata":
                            output_formats['fn'] = os.path.join(tmpdir, "L2A", "meta.%s" % output_formats["format"])
                        if output_formats['type'] == "rgb_jpeg":
                            output_formats['fn'] = os.path.join(tmpdir, "L2A", "RGB.jpg")
                        if output_formats['type'] == "L2A":
                            output_formats['fn'] = output_formats['out_dir']
                    print("Write L2A product")
                    IO.write_results(s2img=img_ac, options=opts, logger=logger)

                    del img
                    del img_ac

    def test_ac_file_system_l1c_sentinel_2_products(self):
        """
        Tests
        :return:
        """

        def create_reference_image_4_coreg(granule_path):
            """
            Creates RGB reference image (.tif) from L1C data with matching band setting for ac
            :param granule_path:
            :return:filename of the produced tif-file
            """
            out_fn = path.join(granule_path, "ref_image.tif")
            ref_img = None
            for ii, bi in enumerate((4, 3, 2)):
                fnt = glob(path.join(granule_path, "IMG_DATA", "*B%02i.jp2" % bi))
                if len(fnt) > 0:
                    ds = gdal.Open(fnt[0])
                    xsize = ds.RasterXSize
                    ysize = ds.RasterYSize
                    rb = ds.GetRasterBand(1)
                    arr = rb.ReadAsArray()
                    if ii == 0:
                        driver = gdal.GetDriverByName("GTiff")
                        ref_img = driver.Create(out_fn, xsize, ysize, 3, gdal.GDT_Int32)
                        ref_img.SetGeoTransform(ds.GetGeoTransform())
                        ref_img.SetProjection(ds.GetProjection())
                        ref_img.GetRasterBand(1).WriteArray(arr)
                    else:
                        ref_img.GetRasterBand(ii + 1).WriteArray(arr)
                    del ds
                else:
                    raise FileNotFoundError("Could not find: %s" % path.join(granule_path, "IMG_DATA", "*B%02i.jp2" %
                                                                             bi))
            if path.isfile(out_fn):
                ref_img.FlushCache()
                del ref_img
                return out_fn
            else:
                raise FileNotFoundError("No Output was writen")

        print("Test ac on L1C data")
        sicor_table_path = os.path.dirname(tables.__file__)
        settings = os.path.join(os.path.dirname(options.__file__), "s2_options.json")
        opts = get_options(settings)
        opts['cld_mask']["persistence_file"] = os.path.join(
            sicor_table_path, os.path.basename(opts['cld_mask']["persistence_file"]))
        opts['cld_mask']["novelty_detector"] = os.path.join(
            sicor_table_path, os.path.basename(opts['cld_mask']["novelty_detector"]))
        opts["uncertainties"]["snr_model"] = os.path.join(
            os.path.dirname(S2MSI.__file__), "data", os.path.basename(opts["uncertainties"]["snr_model"]))
        opts["S2Image"]["driver"] = "OpenJpeg2000"

        for scat_type, op in opts["RTFO"].items():
            op['atm_tables_fn'] = os.path.join(sicor_table_path, os.path.basename(op['atm_tables_fn']))

        ecmwf_zip = path.join(path.dirname(__file__), "data", "ecmwf", "ecmwf.zip")

        for l1c_file in glob(path.join(path.dirname(__file__), "data", "s2a_l1c", "*.zip")):
            print(l1c_file)
            logging.basicConfig(level=logging.INFO)

            with tempfile.TemporaryDirectory() as tmpdir:
                print("Tmp dir: %s" % tmpdir)
                # extract test data to tmp dir
                with zipfile.ZipFile(l1c_file, "r") as zf:
                    zf.extractall(tmpdir)
                # extract ECMWF test data
                with zipfile.ZipFile(ecmwf_zip, "r") as zf:
                    zf.extractall(tmpdir)
                opts['ECMWF']["path_db"] = path.join(tmpdir, "ecmwf")
                # save custom options
                fn_options = path.join(tmpdir, "options.json")
                with open(fn_options, "w") as fl:
                    json.dump(python_to_json(opts), fl, indent=4)

                # loop over l1c product and perform ac
                for l1c_product in glob(os.path.join(tmpdir, "*.SAFE", "GRANULE", "*")):
                    print("Product: %s" % l1c_product)
                    ref_image_fn = create_reference_image_4_coreg(l1c_product)
                    ac(granule_path=l1c_product, settings=fn_options, logdir=tmpdir, out_dir=tmpdir,
                       catch_all_exceptions=False, coregistration={"ref_image_fn": ref_image_fn,
                                                                   "fmt_out": "JP2OpenJPEG",
                                                                   "n_local_points": 120})
                    print("### Testing geocorrected files for empty results")
                    gp = [pp for pp in l1c_product.split(sep) if pp != '']
                    l2a_product_name = gp[-1].replace("L1C", "L2A")
                    l2a_path = path.join(tmpdir, gp[-3].replace("MSIL1C", "MSIL2A").replace("PDMC", "GFZ"), "GRANULE",
                                         l2a_product_name)
                    cjp2_files = glob(path.join(l2a_path, "IMG_DATA", "**", "*_coreg.jp2"), recursive=True)
                    if cjp2_files == []:
                        raise FileNotFoundError("Did not find any corrected jp2 files.")
                    for cjp2 in cjp2_files:
                        print("# Reading files: {file} ".format(file=cjp2))
                        cds = gdal.Open(cjp2)
                        cdarray = np.array(cds.GetRasterBand(1).ReadAsArray())
                        cndv = cds.GetRasterBand(1).GetNoDataValue()
                        gidx = np.where(cdarray != cndv)
                        if len(gidx[0]) > 0:
                            cmedian = np.median(cdarray[gidx])
                        else:
                            print("No valid pixel found for {file}".format(file=cjp2))
                        jp2 = cjp2.replace("_coreg", "")
                        ds = gdal.Open(jp2)
                        darray = np.array(ds.GetRasterBand(1).ReadAsArray())
                        ndv = ds.GetRasterBand(1).GetNoDataValue()
                        gidx = np.where(darray != ndv)
                        if len(gidx[0]) > 0:
                            median = np.median(darray[gidx])
                        else:
                            print("No valid pixel found for {file}".format(file=jp2))

                        if 1-(cmedian / median) > 0.1:
                            raise AssertionError(
                                "Deviation of {dev} between coreg non-coreg detected between {file} and {cfile}".format(
                                    file=jp2, cfile=cjp2, dev=1-(cmedian / median)))
                        else:
                            print("### Test successfull.")

    def test_bin_ecmwf(self):
        def print_run(run):
            print("#############")
            print("## Running ##")
            print("#############")
            print(run.args)
            print("############")
            print("## Stdout ##")
            print("############")
            print(run.stdout.decode("utf-8"))
            print("############")
            print("## Stderr ##")
            print("############")
            print(run.stderr.decode("utf-8"))
            print("#############")
            print("### EEooFF ##")
            print("#############")

            assert run.returncode == 0

        # set up env such that coverage will measure command line script
        env = {env_name: os.environ.get(env_name) for env_name in ["PATH", "PYTHONPATH"]}
        env["COVERAGE_PROCESS_START"] = path.abspath(path.join(path.dirname(__file__), "env", "coveragerc"))
        env["PYTHONPATH"] = "%s:%s" % (path.join(path.dirname(__file__), "env"), env["PYTHONPATH"])
        fn_bin = path.join(path.dirname(__file__), path.pardir, "bin", "sicor_ecmwf.py")
        print_run(subprocess.run(["{python} {script} --help".format(python=sys.executable, script=fn_bin)],
                                 shell=True, check=False, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=env))

        ecmwf_zip = path.join(path.dirname(__file__), "data", "ecmwf", "ecmwf.zip")
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(ecmwf_zip, "r") as zf:
                zf.extractall(tmpdir)

                print_run(subprocess.run(
                    ["{python} {script} --db_path {db_path} -f 2015/12/07 -t 2015/12/07".format(
                        python=sys.executable, script=fn_bin,
                        db_path=path.join(tmpdir, "ecmwf"),
                    )],
                    shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env))

                print_run(subprocess.run(
                    ["{python} {script} --db_path {db_path} -f 2015/12/07 -t 2015/12/07 -r 5/0.0001/0.1".format(
                        python=sys.executable, script=fn_bin,
                        db_path=path.join(tmpdir, "ecmwf"),
                    )],
                    shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env))

    def test_bin_sicor_ac(self):
        def print_run(run, returncode=0):
            print("#############")
            print("## Running ##")
            print("#############")
            print(run.args)
            print("############")
            print("## Stdout ##")
            print("############")
            print(run.stdout.decode("utf-8"))
            print("############")
            print("## Stderr ##")
            print("############")
            print(run.stderr.decode("utf-8"))
            print("#############")
            print("### EEooFF ##")
            print("#############")
            print(run.returncode, returncode)
            assert run.returncode == returncode

        # set up env such that coverage will measure command line script
        env = {env_name: os.environ.get(env_name) for env_name in ["PATH", "PYTHONPATH"]}
        env["COVERAGE_PROCESS_START"] = path.abspath(path.join(path.dirname(__file__), "env", "coveragerc"))
        env["PYTHONPATH"] = "%s:%s" % (path.join(path.dirname(__file__), "env"), env["PYTHONPATH"])
        fn_bin = path.join(path.dirname(__file__), path.pardir, "bin", "sicor_ac.py")
        print_run(subprocess.run(["{python} {script} --help".format(python=sys.executable, script=fn_bin)],
                                 shell=True, check=False, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=env))

        print_run(subprocess.run(["{python} {script} --version".format(python=sys.executable, script=fn_bin)],
                                 shell=True, check=False, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=env))

        # give only -l options should not work
        print_run(subprocess.run(["{python} {script} -l ./".format(python=sys.executable, script=fn_bin)],
                                 shell=True, check=False, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=env),
                  returncode=2)

        with tempfile.TemporaryDirectory() as tmpdir:
            ecmwf_zip = path.join(path.dirname(__file__), "data", "ecmwf", "ecmwf.zip")
            with zipfile.ZipFile(ecmwf_zip, "r") as zf:
                zf.extractall(tmpdir)

            print_run(subprocess.run(["{python} {script} --export_options_to {fn} ".format(
                python=sys.executable, script=fn_bin, fn=path.join(tmpdir, "options_s2.json"))],
                                     shell=True, check=False, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, env=env))

            print(tmpdir)
            print(tmpdir)

    def test_sicor_Tools_NM_interpolate_n(self):

        intpn = interpolate_n

        # Two dimensions initialisation
        lut = np.arange(12, dtype=np.float).reshape(3, 4)
        xx = np.array([3., 4., 6.])
        yy = np.array([1., 5., 10, 15])
        axes = (xx, yy)
        pn = intpn.interpolate_n(lut, axes)
        # recall
        pos = np.array([[4.5, 1.5], [3.5, 1.5], [5.5, 2.5], [4.5, 1.5]])  # (xx,yy),(xx,yy),(xx,yy),(xx,yy)
        print(pos.shape)
        print(pn.recall(pos))
        pos = np.array([[4.5, 1.5]])
        print(pn.recall(pos))

        # Four dimensions initialisation
        lut = np.arange(2 * 3 * 4 * 5, dtype=np.float).reshape(2, 3, 4, 5)
        x1 = np.array([3., 7.])
        x2 = np.array([1., 5., 10.])
        x3 = np.array([1., 2., 4., 12.])
        x4 = np.array([0., 1., 3., 8., 10.])
        axes = (x1, x2, x3, x4)
        pn = intpn.interpolate_n(lut, axes)
        # recall
        pos = np.array([[3.5, 5.5, 4.2, 8.8], [4.5, 4.5, 5.2, 7.8]])  # (x1,x2,x3,x4),(x1,x2,x3,x4)
        print(pos.shape)
        print(pn.recall(pos))
        pos = np.array([[4.5, 1.5, 3.8, 8.]])
        print(pn.recall(pos))
        pos = np.array([[3.5, 5.5, 4.2, 8.8]])
        print(pn.recall(pos))
        print('==')
        print(pn.recall(np.array([[0.125, 1.1, 2.025, 3.4]]), is_index=True))


class TestSicor_disable_numba_jit(unittest.TestCase):
    """Use some tests from TestSicior, but use mock to disable numba.jit."""

    def setUp(self):
        # Do cleanup first so it is ready if an exception is sraised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            patch.stopall()  # Stops all patches started with start()

            for n_interp in range(*range_interp_spectral_n):
                intp = importlib.import_module("sicor.Tools.NM.interp_spectral_n_%i" % n_interp)
                importlib.reload(intp)  # Reload our UUT module which restores the original decorator

        # We want to make sure this is run so we do this in addCleanup instead of tearDown
        self.addCleanup(kill_patches)
        self.__test_sicor_Tools_NM_interp_spectral_n_X = TestSicor.test_sicor_Tools_NM_interp_spectral_n_X

        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        patch('numba.jit', lambda *x, **y: lambda f: f).start()
        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        for n_interp in range(*range_interp_spectral_n):
            intp = importlib.import_module("sicor.Tools.NM.interp_spectral_n_%i" % n_interp)
            importlib.reload(intp)  # Reload our UUT module which restores the original decorator

    def test_sicor_Tools_NM_interp_spectral_n_X(self):
        self.__test_sicor_Tools_NM_interp_spectral_n_X(self)


class TestSicor_GeoMultiSens_using_dill_files(unittest.TestCase):
    """Test for sicor based on inputs from GeoMultiSens"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_sicor_ac_landsat8(self, save_new_expected_results=False):
        print("Test ac on Landsat8 L1C data")

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("w")

        sicor_table_path = os.path.dirname(tables.__file__)
        settings = os.path.join(os.path.dirname(options.__file__), "l8_options.json")
        opts = get_options(settings)
        for scat_type, op in opts["RTFO"].items():
            op['atm_tables_fn'] = path.join(sicor_table_path, path.basename(op['atm_tables_fn']))

        for l1c_file in glob(path.join(path.dirname(__file__), "data", "L8_l1c", "*.dill")):
            with tempfile.TemporaryDirectory() as tmpdir:
                opts["ECMWF"]['path_db'] = path.join(tmpdir, "ecmwf")

                ecmwf_zip = path.join(path.dirname(__file__), "data", "ecmwf", "ecmwf.zip")
                with zipfile.ZipFile(ecmwf_zip, "r") as zf:
                    zf.extractall(tmpdir)
                opts['ECMWF']["path_db"] = path.join(tmpdir, "ecmwf")

                soft_dir = path.join(tmpdir, "py")
                os.makedirs(soft_dir, exist_ok=True)
                gms_zip = path.join(path.dirname(__file__), "data", "soft", "gms_preprocessing_reduced.zip")
                with zipfile.ZipFile(gms_zip, "r") as zf:
                    zf.extractall(soft_dir)

                sys.path.insert(0, path.join(soft_dir, "gms_preprocessing"))
                logger.info("Load: %s" % l1c_file)
                with open(l1c_file, "rb") as fl:
                    gms_interface = dill.load(fl)

                s2img = gms_interface["rs_image"]
                s2img.logger = logger
                s2img.metadata['SENSING_TIME'] = datetime(2015, 12, 7, 14)  # make ecmwf test archive simpler

                ac_gms(s2img=s2img, options=opts)

                if save_new_expected_results is True:
                    with open(l1c_file.replace(".dill", ".json"), "w") as fl:
                        json.dump(opts['processing'], fl, indent=4)

                # load to-be expected data from file and compare results
                with open(l1c_file.replace(".dill", ".json"), "r") as fl:
                    expected_result = json.load(fl)

                comp(expected_result, opts['processing'], ('clear_fraction',))
                for metric in ('median_values', "std_values"):
                    for band in expected_result[metric].keys():
                        comp(expected_result, opts['processing'], (metric, band))

                for band in expected_result['median_values'].keys():
                    comp(expected_result, opts['processing'], ('uncertainties', band, "coef"))

                for band in expected_result["uncertainties"]['rfl_to_rad'].keys():
                    comp(expected_result, opts['processing'], ('uncertainties', 'rfl_to_rad', band))


if __name__ == "__main__":
    unittest.main()

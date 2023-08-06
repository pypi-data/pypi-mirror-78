"""Convert example ipynb files to res in docs.

When exporting jupyter notebooks as rsf files, image links don't work when moved to
deeper file structure, which is fixed by running this script:

sicor_ch4/sicor_ch4.rst  ->  sicor_ch4/sicor_ch4_adj.rst
    .. image:: output_14_0.png  ->  .. image:: examples/sicor_ch4/output_14_0.png
    .. image:: output_19_1.png  ->  .. image:: examples/sicor_ch4/output_19_1.png
    .. image:: output_22_2.png  ->  .. image:: examples/sicor_ch4/output_22_2.png
    .. image:: output_23_0.png  ->  .. image:: examples/sicor_ch4/output_23_0.png

Files are renamed with '_adj' and files with this token are not touched.
"""

import subprocess
import sys
from glob import glob
from os import path, remove, chdir


__author__ = "Niklas Bohn, Andre Hollstein"

examples = (
    "sicor_ch4",
    "sicor_CloudMask",
    "sicor_scene_detection",
    "sicor_ac_EnMAP",
)
docs_dir = path.join(
    path.abspath(path.join(path.dirname(__file__), path.pardir)),
    "docs", "examples")
exclude_token = "_adj"
image_token = ".. image:: "

if __name__ == "__main__":

    for example in examples:  # run nbconvert to rst
        cmd = "{jupyter} nbconvert --to RST {infile} --output {outfile}".format(
            jupyter=sys.executable.replace("python", "jupyter"),
            infile=path.join(path.dirname(__file__), example + ".ipynb"),
            outfile=path.join(docs_dir, example, example + ".rst"))
        print(example, "-->", cmd)

        run = subprocess.run([cmd], shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # change image lings to right depth
    chdir(docs_dir)
    for fn in glob("**/*%s.rst" % exclude_token,):
        remove(fn)
    for rst_file in glob("**/*.rst",):
        if "_adj" not in rst_file:
            rst_file_adj = rst_file.replace(".rst", "%s.rst" % exclude_token)
            print(rst_file, " -> ", rst_file_adj)
            with open(rst_file, "r+", encoding='utf-8') as rs, open(rst_file_adj, "w", encoding='utf-8') as fl:
                for line in rs:
                    if image_token in line:
                        line2 = "%s%s" % (
                            image_token, path.join(
                                "examples",
                                path.dirname(rst_file),
                                path.basename(line.replace("\n", "").split(image_token)[-1])
                            ))
                        print("   ", line.replace("\n", ""), " -> ", line2)
                        line = line2
                    fl.write(line)

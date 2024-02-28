#!/usr/bin/python

import os
import subprocess
import glob
import shutil

openbabel_dir = "/home/essex/Downloads/openbabel/build/bin/"
pdb_file = glob.glob("*.pdb")
for pdb in pdb_file:
    pdb_prefix = pdb.split(".")[0]
    pdb2mol2_cmd = openbabel_dir + "obabel -ipdb " + pdb + " -omol2 -O " + pdb_prefix + ".mol2"
    subprocess.run(pdb2mol2_cmd, shell=True)

if not os.path.exists("mol2"):
    os.mkdir("mol2")
mol2_file = glob.glob("*.mol2")
for mol2 in mol2_file:
    shutil.move(mol2, "mol2")

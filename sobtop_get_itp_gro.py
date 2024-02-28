#!/usr/bin/python
# use sobtop program to get itp and gro fromat file.

import os
import subprocess
import glob
import shutil

current_dir = os.getcwd()
sobtop_dir = "/home/essex/Downloads/sobtop/sobtop_1.0_dev3.1/"
mol2_file = glob.glob("*.mol2")
for mol2 in mol2_file:
    # print(mol2)
    os.chdir(current_dir)
    shutil.copy(mol2, sobtop_dir)
    os.chdir(sobtop_dir)
    p1 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # get itp and top file
    p1.communicate(mol2.encode() + "\n1\n3\n0\n4\n\n\n0\n".encode())

    # get gro file
    p2 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p2.communicate(mol2.encode() + "\n2\n\n0\n".encode())

if not os.path.exists(current_dir + "/itp"):
    os.mkdir(current_dir + "/itp")
itp_file = glob.glob("*.itp")
for itp in itp_file:
    print(itp)
    shutil.move(itp, current_dir + "/itp")

if not os.path.exists(current_dir + "/top"):
    os.mkdir(current_dir + "/top")
top_file = glob.glob("*.top")
for top in top_file:
    shutil.move(top, current_dir + "/top")
#
if not os.path.exists(current_dir + "/gro"):
    os.mkdir(current_dir + "/gro")
gro_file = glob.glob("*.gro")
for gro in gro_file:
    shutil.move(gro, current_dir + "/gro")

m2_file = glob.glob("*.mol2")
for m2 in m2_file:
    os.remove(m2)
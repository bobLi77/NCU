#!/usr/bin/python
# 用于将cif格式文件转换成pdb格式
import os
import subprocess
import glob
import shutil


cif_file = glob.glob("*.cif")
Multiwfn_dir = "/home/essex/Downloads/Multiwfn/Multiwfn_3.8_dev_bin_Linux/"
for cif in cif_file:
    p = subprocess.Popen(Multiwfn_dir + "Multiwfn\n",shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    p.communicate(cif.encode() + '\n100\n2\n1\n\n0\nq\n'.encode())
if not os.path.exists("pdb"):
    os.mkdir("pdb")
pdb_file = glob.glob("*.pdb")
for p in pdb_file:
    shutil.move(p,"pdb")
    # print(cif)


#!/usr/bin/python

# author:bob
# created time: 2023-08-31
# function: use to trjconv the box size to triclinic, gromacs default is cubic

import subprocess


# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量

trjconv_file = input("please input your gro file: ")
tpr_file_name = trjconv_file.split(".")[0] + ".tpr"
output_file_name = trjconv_file.split(".")[0] + "_trj.gro"
trjconv_tric_cmd = gmxdir + "gmx trjconv -s " + tpr_file_name + " -f " + trjconv_file + " -o " + output_file_name + " -ur tric -pbc mol"
subprocess.run(trjconv_tric_cmd, shell=True)

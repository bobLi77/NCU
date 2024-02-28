#!/usr/bin/python

# author:bob
# created time: 2023-08-31
# function: use to translate the gro file

import subprocess
import time

# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量

input_file = input("please enter the file name: ")
translate_xyz = input("please enter translate xyz(such as 0 0 6): ")
output_name = input_file.split("box")[0] + "trans.gro"
translate_cmd = gmxdir + "gmx editconf -f " + input_file + " -o " + output_name + " -translate " + translate_xyz
subprocess.run(translate_cmd, shell=True)

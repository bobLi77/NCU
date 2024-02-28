#!/usr/bin/python

# author:bob
# created time: 2023-08-30
# function: use to generate the posre itp file

import subprocess

# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量

input_name = input("please enter the gro file name: ")
output_name = input_name.split(".")[0] + "_posre.itp"
genrestr_cmd = "gmx genrestr -f " + input_name + " -o " + output_name
p = subprocess.Popen(gmxdir + genrestr_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p.communicate("2\n".encode())

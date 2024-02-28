#!/usr/bin/python

# author:bob
# created time: 2023-08-25
# function: use to reset small molecular box size

import subprocess


# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量


input_name = input("please enter the reset box file name: ")
output_name = input_name.split(".")[0] + "_box.gro"
reset_box_x = input("please input reset_box x axis size: ")
reset_box_y = input("please input reset_box y axis size: ")
reset_box_z = input("please input reset_box z axis size: ")

reset_box_size_cmd = gmxdir + "gmx editconf -f " + input_name +" -o " + output_name +" -c -box " + reset_box_x + " " + reset_box_y + " " + reset_box_z
box_size = subprocess.run(reset_box_size_cmd, shell=True)
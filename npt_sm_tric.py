#!/usr/bin/python

# author:bob
# created time: 2023-08-25
# function: use to mm and npt the packmol small molecular

import subprocess
import time

# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量

input_packmol_sm_name = input("please enter the sm pdb name: ")
print("\n请输入xyz坐标,如沿y轴扩散,xz坐标在原基础上减去0.2nm(2A)\n")
box_x = input("please input box x axis size: ")
box_y = input("please input box y axis size: ")
box_z = input("please input box z axis size: ")
box_angles = input("please input triclinic angles(such as 90 109 90): ")

output_gro_name = input_packmol_sm_name.split('.')[0] + ".gro"
# 1. set box size
set_box_size_cmd = gmxdir + "gmx editconf -f " + input_packmol_sm_name + " -o " + output_gro_name \
                   + " -c -box " + box_x + " " + box_y + " " + box_z + " -bt triclinic -angles " + box_angles
box_size = subprocess.run(set_box_size_cmd, shell=True)
time.sleep(2)


# 2. MM
mm_grompp_cmd = gmxdir + "gmx grompp -f minim.mdp -c " + output_gro_name + " -p sm.top -o min_cmp100.tpr"
mm_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm min_cmp100"
mm_grompp = subprocess.run(mm_grompp_cmd, shell=True)
mm_mdrun = subprocess.run(mm_mdrun_cmd, shell=True)
time.sleep(2)

# npt
npt_grompp_cmd = gmxdir + "gmx grompp -f npt.mdp -c min_cmp100.gro -p sm.top -o npt_cmp100.tpr"
npt_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm npt_cmp100 -update gpu"
npt_grompp = subprocess.run(npt_grompp_cmd, shell=True)
npt_mdrun = subprocess.run(npt_mdrun_cmd, shell=True)

#!/usr/bin/python

# author:bob
# created time: 2023-08-25
# function: use to MM and nvt

import os
import subprocess
import time

# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量

current_dir = os.getcwd()
filefoldlist = os.listdir(current_dir)
# print(filefoldlist)
# print(len(filefoldlist))
for fold in filefoldlist:
    # print(fold)
    os.chdir(fold)
    # 1. MM
    mm_grompp_cmd = gmxdir + "gmx grompp -f minim.mdp -c complex_trans.gro -p topol.top -o min_cmp_mix.tpr"
    mm_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm min_cmp_mix"
    mm_grompp = subprocess.run(mm_grompp_cmd, shell=True)
    mm_mdrun = subprocess.run(mm_mdrun_cmd, shell=True)
    time.sleep(2)
    #
    # 2.nvt
    npt_grompp_cmd = gmxdir + "gmx grompp -f nvt_md_pbc.mdp -c min_cmp_mix.gro -r min_cmp_mix.gro -p topol.top -o nvt_cmp_mix_200ns.tpr"
    npt_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm nvt_cmp_mix_200ns -update gpu"
    npt_grompp = subprocess.run(npt_grompp_cmd, shell=True)
    npt_mdrun = subprocess.run(npt_mdrun_cmd, shell=True)
    time.sleep(2)
    os.chdir(current_dir)

#!/usr/bin/python
# author:bob
# created time: 2024-1-2
# function:
# 1. 用于验证力场的正确性


import os
import subprocess
import shutil
import glob

# gmx运行路径,根据安装路径进行修改
import time

gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量
sobtop_dir = "/home/essex/Downloads/sobtop/sobtop_1.0_dev3.1/"
current_dir = os.getcwd()


def md_pbc_mdp():
    with open("md_PBC.mdp", 'w', encoding="utf-8") as fw:
        fw.write("integrator = md\n"
                 "dt =0.001\n"
                 "nsteps = 1000000\n"
                 "comm-grps = system\n"
                 "nstxout = 0\n"
                 "nstvout = 0\n"
                 "nstfout = 0\n"
                 "nstlog = 500000\n"
                 "nstenergy = 500000\n"
                 "nstxout-compressed = 500000\n"
                 "compressed-x-grps = system\n"
                 "periodic-molecules = yes\n"
                 "pbc = xyz\n"
                 "cutoff-scheme = verlet\n"
                 "rlist = 1.2\n"
                 "coulombtype = PME\n"
                 "rcoulomb = 1.2\n"
                 "vdwtype = cut-off\n"
                 "rvdw = 1.2\n"
                 "DispCorr = no\n"
                 "Tcoupl = v-rescale\n"
                 "tau_t = 0.2\n"
                 "tc_grps = system\n"
                 "ref_t = 300\n"
                 "Pcoupl = C-rescale\n"
                 "pcoupltype = isotropic\n"
                 "tau_p = 1.5\n"
                 "ref_p = 1.0\n"
                 "compressibility = 4.5e-5\n"
                 "gen_vel = yes\n"
                 "gen_temp = 100\n"
                 "gen_seed = -1\n"
                 "constraints = hbonds")


def process_molsie():
    # 1. 四周增加1A距离,防止边缘周期性问题
    # input_molecular_sieve_name = input("please enter the molecular_sieve pdb name: ")
    all_pdb_file_name = glob.glob("*.pdb")
    for pdb_file_name in all_pdb_file_name:
        # print(pdb_file_name)
        # 文件夹名
        fold_name = pdb_file_name.split('.')[0]
        # print(fold_name)
        os.mkdir(fold_name)
        shutil.move(pdb_file_name, current_dir + "/" + fold_name)
        os.chdir(current_dir + "/" + fold_name)
        # print(os.getcwd())
        output_name = pdb_file_name.split(".")[0] + "_1A.pdb"
        # 打开pdb文件,读取第二行信息
        with open(pdb_file_name, "r", encoding="utf-8") as f:
            # 提取第二行信息,并且将多个空格置换成一个逗号(或一个空格)
            second_context = ",".join(f.readlines()[1].split())
            # 提取第2,3,4列数据作为xyz坐标,同时进行单位换算,转换成nm
            x = float(second_context.split(",")[1]) / 10 + 1
            y = float(second_context.split(",")[2]) / 10 + 1
            z = float(second_context.split(",")[3]) / 10 + 1
        f.close()
        editconf_cmd = gmxdir + "gmx editconf -f " + pdb_file_name + " -o " + output_name \
                       + " -c -box " + str(x) + " " + str(y) + " " + str(z)
        subprocess.run(editconf_cmd, shell=True)

        # 2. editconf生成的pdb文件,SI类型变成S,需要手动替换
        # 只打开一次文件,使用w+ 读写功能,结果为空, 原因不清,理论上应该可以覆盖写入
        with open(output_name, 'r', encoding="utf-8") as fi:
            context = fi.read()
            mod_cont = context.replace("    S", "   SI")
        with open(output_name, 'w', encoding="utf-8") as fw:
            fw.write(mod_cont)
        fw.close()
        fi.close()

        # 3. 通过sobtop获取itp,gro,top文件
        # 3.1 将文件复制到sobtop文件夹
        shutil.copy(output_name, sobtop_dir)
        # 3.2 将路径切换到sobtop
        os.chdir(sobtop_dir)
        # 3.3 运行命令
        p1 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        # 3.4 get itp and top file
        p1.communicate(output_name.encode() + "\n1\n5\n1\n0\n4\n\n\n0\n".encode())
        # 3.5 get gro file
        p2 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        p2.communicate(output_name.encode() + "\n2\n\n0\n".encode())
        # 3.6 将itp,gro,top剪切过来
        itp_name = output_name.split(".")[0] + ".itp"
        gro_name = output_name.split(".")[0] + ".gro"
        top_name = output_name.split(".")[0] + ".top"
        # shutil.move(output_name, current_dir + "/" + fold_name)
        os.remove(output_name)
        shutil.move(itp_name, current_dir + "/" + fold_name)
        shutil.move(gro_name, current_dir + "/" + fold_name)
        shutil.move(top_name, current_dir + "/" + fold_name)

        # 返回文件夹
        os.chdir(current_dir + "/" + fold_name)
        # 4. 处理分子筛的itp文件,
        molsie_output_file_name = output_name.split('.')[0] + "_mod.itp"
        process_molsie_itp_cmd = "cat " + itp_name \
                                 + " | sed 's/UF_Si      1      MOL/Si_bulk    1      MOL/g' " \
                                   "| sed 's/0.00000000   28.085499/1.10000000   28.085499/g' " \
                                   "| sed 's/UF_O       1      MOL      O/O_bulk     1      MOL      O/g' " \
                                   "| sed 's/ 0.00000000   15.999405/-0.55000000   15.999405/g' " \
                                   "| sed 's/         1        .*     2.500000E+05     /         1        0.165000     2.384880E+05     /g' " \
                                   "| sed 's/         1       .*      5.000000E+02     /         1       109.500      8.368000E+02     /g' " \
                                   "| sed 's/         1       .*      5.000000E+02     /         1       149.000      8.368000E+02     /g' " \
                                   "| sed '/^UF_Si       14    /d' | sed '/^UF_O         8    /d' > " + molsie_output_file_name
        subprocess.run(process_molsie_itp_cmd, shell=True)
        # 将文件覆盖原来文件
        subprocess.run("mv " + molsie_output_file_name + " " + itp_name, shell=True)

        # 5. 运行npt模拟
        top_file_name = output_name.split(".")[0] + ".top"
        tpr_file_name = output_name.split(".")[0] + ".tpr"
        grompp_cmd = "gmx grompp -f md_PBC.mdp -c " + output_name + " -p " + top_file_name + " -o " + tpr_file_name + " -maxwarn 2"
        mdrun_cmd = "gmx mdrun -v -deffnm " + tpr_file_name.split('.')[0]

        # 获取md_PBC.mdp
        md_pbc_mdp()
        # 运行模拟
        subprocess.run(gmxdir + grompp_cmd, shell=True)
        subprocess.run(gmxdir + mdrun_cmd, shell=True)

        time.sleep(2)
        # 完成一个文件的创建后,返回上一级目录
        os.chdir(current_dir)


if __name__ == '__main__':
    process_molsie()

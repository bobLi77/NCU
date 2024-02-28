#!/usr/bin/python
# author:bob
# created time: 2023-12-30
# function:
# 1. 小分子pdb文件,通过packmol构建单一分子体系,自定义构建数量
# 2. he 墙,通过packmol构建,数量为2000;
# 3. 分子筛通过重设盒子尺寸,与小分子体系,he构成初始模型
# 4. 针对非直角类型盒子.

import glob
import os
import time
import subprocess
import shutil


def packmol_sm_and_sobtop_pdb2gro(small_mol_pdb_file_name):
    sm_packmol_file_name = str(small_mol_pdb_file_name).split('.')[0] + "_" + str(construct_small_mol_count) + "_" + \
                           str(mol_sie_pdb_file_name).split('.')[0] + ".inp"
    with open(sm_packmol_file_name, 'w', encoding='utf-8') as fw:
        fw.write("tolerance 2.0\n"
                 "filetype pdb\n"
                 "output " + sm_packmol_file_name.split('.')[0] + '.pdb\n\n'
                                                                  'structure ' + small_mol_pdb_file_name + "\n"
                                                                                                           "        number " + construct_small_mol_count + '\n'
                                                                                                                                                           '        inside box 0. 0. 0. ' + str(
            int(float(x) - 2)) + '. ' + str(int(float(y) - 2)) + '. ' + str(int(float(z) - 2)) + '.\n'
                                                                            'end structure')
    # 运行packmol 构建
    subprocess.run("packmol < " + sm_packmol_file_name, shell=True)
    time.sleep(2)
    # gmx editconf 将pdb转gro
    # sobtop将pdb转gro存在异常

    sm_packmol_pdb_file_name = sm_packmol_file_name.split('.')[0] + ".pdb"
    # output_sm_gro_file_name = sm_packmol_file_name.split('.')[0] + ".gro"
    # gmx_editconf_cmd = gmxdir + "gmx editconf -f " + sm_packmol_pdb_file_name + " -o " + output_sm_gro_file_name
    # subprocess.run(gmx_editconf_cmd, shell=True)

    shutil.move(sm_packmol_pdb_file_name, sobtop_dir)
    os.chdir(sobtop_dir)
    p1 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p1.communicate(sm_packmol_pdb_file_name.encode() + "\n2\n\n0\n".encode())
    gro_file_name = sm_packmol_file_name.split('.')[0] + ".gro"
    shutil.move(gro_file_name, current_dir + fold_name)
    shutil.move(sm_packmol_pdb_file_name, current_dir + fold_name)
    os.chdir(current_dir + fold_name)


def sobtop_pdb_to_mol2_and_get_itptop(small_mol_pdb_file_name):
    # pdb to mol2
    mol2_file_name = small_mol_pdb_file_name.split('.')[0] + ".mol2"
    subprocess.run(obabel_dir + "obabel -ipdb " + small_mol_pdb_file_name + " -omol2 -O " + mol2_file_name, shell=True)
    # sobtop 获取itp和top
    shutil.move(mol2_file_name, sobtop_dir)
    os.chdir(sobtop_dir)
    p2 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # get itp and top file
    p2.communicate(mol2_file_name.encode() + "\n1\n3\n0\n4\n\n\n0\n".encode())
    itp_file_name = small_mol_pdb_file_name.split('.')[0] + ".itp"
    top_file_name = small_mol_pdb_file_name.split('.')[0] + ".top"
    shutil.move(itp_file_name, current_dir + fold_name)
    shutil.move(top_file_name, current_dir + fold_name)
    shutil.move(mol2_file_name, current_dir + fold_name)
    os.chdir(current_dir + fold_name)


def cal_resp_and_replace(small_mol_pdb_file_name):
    # 从pdb计算resp,得到chg文件,然后将itp中的电荷替换成resp
    subprocess.run(resp_orca_dir + "RESP_ORCA.sh " + small_mol_pdb_file_name, shell=True)
    # 替换resp电荷
    chg_file_name = small_mol_pdb_file_name.split('.')[0] + ".chg"
    itp_file_name = small_mol_pdb_file_name.split('.')[0] + ".itp"

    subprocess.run(
        "cat " + itp_file_name + " | sed -n '/\[ atoms \]/,/\[ bonds \]/p' | sed '1,2d' | sed '$d' | sed '$d' >atoms_tmp1.txt",
        shell=True)
    subprocess.run(
        "cat " + chg_file_name + " | awk '{printf \"%13s\\n\", $NF}' | paste atoms_tmp1.txt - | awk '{$7=$NF;print $0}' | awk '{$NF=null;print $0}' | awk '{printf \"%6s%7s%10s%9s%8s%12s%14s%12s\\n\",$1,$2,$3,$4,$5,$6,$7,$8}' >chg_tmp2.txt",
        shell=True)
    subprocess.run(
        "cat " + itp_file_name + " | sed -n '1,/\[ bonds \]/p' | sed -n '1,/Index/p' | cat - chg_tmp2.txt >itp_tmp3.txt",
        shell=True)
    subprocess.run("cat " + itp_file_name + "  | sed -n '/\[ bonds \]/,/$p/p' | sed '1i\ ' | cat itp_tmp3.txt - >" +
                   small_mol_pdb_file_name.split('.')[0] + "_resp.itp", shell=True)
    subprocess.run("rm *.txt", shell=True)
    subprocess.run(
        "mv " + small_mol_pdb_file_name.split('.')[0] + "_resp.itp " + " " + small_mol_pdb_file_name.split('.')[
            0] + ".itp", shell=True)
    subprocess.run("echo \"RESP电荷已成功替换,请查看当前itp文件\"", shell=True)


def modify_top_small_mol_count(small_mol_pdb_file_name):
    top_file_name = small_mol_pdb_file_name.split('.')[0] + ".top"
    with open(top_file_name, 'r', encoding='utf-8') as ftop:
        ftop_context = ftop.readlines()
        # 提取最后一行的名字, 加数字组合成新的top
        small_mol_name = ftop_context[-1].split()[0]
        other_context = ftop_context[:-1]
        str_other_context = ""
        for line in other_context:
            str_other_context += line
        new_top_file = str_other_context + small_mol_name + '\t' + construct_small_mol_count
    ftop.close()
    with open(top_file_name, 'w', encoding='utf-8') as fwtop:
        fwtop.write(new_top_file)
    fwtop.close()


def get_minim_npt_mdp_file():
    with open("sm_minim.mdp", 'w', encoding='utf-8') as fwmin:
        fwmin.write("integrator = steep\n"
                    "emtol = 1000.0\n"
                    "emstep = 0.01\n"
                    "nsteps = 50000\n"
                    "nstlist = 40\n"
                    "cutoff-scheme = Verlet\n"
                    "ns_type = grid\n"
                    "coulombtype = cutoff\n"
                    "rcoulomb = 1.2\n"
                    "rvdw = 1.2\n"
                    "pbc = xyz")
    fwmin.close()

    with open("sm_npt.mdp", 'w', encoding='utf-8') as fwnpt:
        fwnpt.write("integrator = md\n"
                    "nsteps = 100000\n"
                    "dt = 0.002\n"
                    "nstxout = 5000\n"
                    "nstvout = 5000\n"
                    "nstenergy = 5000\n"
                    "nstlog = 5000\n"
                    "nstlist = 40\n"
                    "nstcomm = 100\n"
                    "pbc = xyz\n"
                    "rlist = 1.2\n"
                    "coulombtype = PME\n"
                    "pme_order = 4\n"
                    "fourierspacing = 0.16\n"
                    "rcoulomb = 1.2\n"
                    "vdw-type = Cut-off\n"
                    "rvdw = 1.2\n"
                    "Tcoupl = v-rescale\n"
                    "tc-grps = system\n"
                    "tau_t = 0.1\n"
                    "ref_t = 300\n"
                    "DispCorr = EnerPres\n"
                    "Pcoupl = C-rescale\n"
                    "Pcoupltype = Isotropic\n"
                    "tau_p = 2.0\n"
                    "compressibility = 4.5e-5\n"
                    "ref_p = 1.0\n"
                    "refcoord_scaling = com\n"
                    "gen_vel = no\n"
                    "constraints = h-bonds\n"
                    "continuation = yes\n"
                    "constraint_algorithm = lincs\n"
                    "lincs_iter = 1\n"
                    "lincs_order = 4")
    fwnpt.close()



def minim_npt_small_mol(small_mol_pdb_file_name):
    input_pdb_name = str(small_mol_pdb_file_name).split('.')[0] + "_" + str(construct_small_mol_count) + "_" + \
                     str(mol_sie_pdb_file_name).split('.')[0] + ".pdb"
    output_gro_name = str(small_mol_pdb_file_name).split('.')[0] + "_" + str(construct_small_mol_count) + "_" + \
                      str(mol_sie_pdb_file_name).split('.')[0] + ".gro"
    top_file_name = small_mol_pdb_file_name.split('.')[0] + ".top"
    # 1. set box size
    set_box_size_cmd = gmxdir + "gmx editconf -f " + input_pdb_name + " -o " + output_gro_name \
                       + " -c -box " + str(float(x) / 10) + " " + str(float(y) / 10) + " " + str(
        float(z) / 10)
    subprocess.run(set_box_size_cmd, shell=True)
    time.sleep(2)

    # 2. MM
    mm_grompp_cmd = gmxdir + "gmx grompp -f sm_minim.mdp -c " + output_gro_name + " -p " + top_file_name + " -o min_small_mol.tpr"
    mm_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm min_small_mol"
    subprocess.run(mm_grompp_cmd, shell=True)
    subprocess.run(mm_mdrun_cmd, shell=True)
    time.sleep(2)

    # # NVT
    # nvt_grompp_cmd = gmxdir + "gmx grompp -f sm_nvt.mdp -c min_small_mol.gro -p " + top_file_name + " -o nvt_small_mol.tpr"
    # nvt_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm nvt_small_mol -update gpu"
    # subprocess.run(nvt_grompp_cmd, shell=True)
    # subprocess.run(nvt_mdrun_cmd, shell=True)
    # npt
    npt_grompp_cmd = gmxdir + "gmx grompp -f sm_npt.mdp -c min_small_mol.gro -p " + top_file_name + " -o npt_small_mol.tpr"
    npt_mdrun_cmd = gmxdir + "gmx mdrun -v -deffnm npt_small_mol -update gpu"
    subprocess.run(npt_grompp_cmd, shell=True)
    subprocess.run(npt_mdrun_cmd, shell=True)

    # # 修正npt后的小分子,从正方体变成斜体
    # trjconv_tric_cmd = gmxdir + "gmx trjconv -s min_small_mol.tpr -f min_small_mol.gro -o tric_min_small_mol.gro -ur tric -pbc mol"
    # p = subprocess.Popen(trjconv_tric_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # p.communicate("1\n".encode())


def get_mol_sieve_gro_itp_top():
    # 1. 获取分子筛的坐标,然后xyz分别增加1A, 得到的pdb文件后,再通过sobtop获取gro,itp,top文件
    with open(mol_sie_pdb_file_name, 'r', encoding='utf-8') as frms:
        frms_context = frms.readlines()
        mol_sie_x = frms_context[1].split()[1]
        mol_sie_y = frms_context[1].split()[2]
        mol_sie_z = frms_context[1].split()[3]
        mol_sie_anglex = frms_context[1].split()[4]
        mol_sie_angley = frms_context[1].split()[5]
        mol_sie_anglez = frms_context[1].split()[6]
    frms.close()

    # 2. gmx editconf 增加1A
    mol_sie_output_name = mol_sie_pdb_file_name.split('.')[0] + "_1A.pdb"
    add_1_a_cmd = gmxdir + "gmx editconf -f " + mol_sie_pdb_file_name + " -o " + mol_sie_output_name \
                  + " -c -box " + str(float(mol_sie_x) / 10 + 1) + " " + str(float(mol_sie_y) / 10 + 1) + " " + str(
        float(
            mol_sie_z) / 10 + 1)
    subprocess.run(add_1_a_cmd, shell=True)

    # 3. editconf生成的pdb文件,SI类型变成S,需要手动替换
    # 只打开一次文件,使用w+ 读写功能,结果为空, 原因不清,理论上应该可以覆盖写入
    with open(mol_sie_output_name, 'r', encoding="utf-8") as fi:
        context = fi.read()
        mod_cont = context.replace("    S", "   SI")
    with open(mol_sie_output_name, 'w', encoding="utf-8") as fw:
        fw.write(mod_cont)
    fw.close()
    fi.close()

    # 3. 通过sobtop获取itp,gro,top文件
    # 3.1 将文件复制到sobtop文件夹
    shutil.move(mol_sie_output_name, sobtop_dir)
    # 3.2 将路径切换到sobtop
    os.chdir(sobtop_dir)
    # 3.3 运行命令
    p1 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # 3.4 get itp and top file
    p1.communicate(mol_sie_output_name.encode() + "\n1\n5\n1\n0\n4\n\n\n0\n".encode())
    # 3.5 get gro file
    p2 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p2.communicate(mol_sie_output_name.encode() + "\n2\n\n0\n".encode())
    # 3.6 将itp,gro,top剪切过来
    itp_name = mol_sie_output_name.split(".")[0] + ".itp"
    gro_name = mol_sie_output_name.split(".")[0] + ".gro"
    top_name = mol_sie_output_name.split(".")[0] + ".top"
    shutil.move(mol_sie_output_name, current_dir + fold_name)
    shutil.move(itp_name, current_dir + fold_name)
    shutil.move(gro_name, current_dir + fold_name)
    shutil.move(top_name, current_dir + fold_name)
    os.chdir(current_dir + fold_name)


def packmol_he2000():
    he_packmol_file_name = str(he_pdb_file_name).split('.')[0] + "2000.inp"
    with open(he_packmol_file_name, 'w', encoding='utf-8') as fw:
        fw.write("tolerance 2.0\n"
                 "filetype pdb\n"
                 "output " + he_packmol_file_name.split('.')[0] + '.pdb\n\n'
                                                                  'structure ' + he_pdb_file_name + "\n"
                                                                                                    "        number 2000\n"
                                                                                                    '        inside box 0. 0. 0. ' + str(
            int(float(x))) + '. ' + str(int(float(10))) + '. ' + str(int(float(z))) + '.\n'
                                                            'end structure')
    # 运行packmol 构建
    subprocess.run("packmol < " + he_packmol_file_name, shell=True)
    time.sleep(2)

    # sobtop将He2000.pdb转gro
    # sobtop 将He.pdb获取itp和top
    he_packmol_pdb_file_name = he_packmol_file_name.split('.')[0] + ".pdb"
    shutil.copy(he_packmol_pdb_file_name, sobtop_dir)
    shutil.copy(he_pdb_file_name, sobtop_dir)

    os.chdir(sobtop_dir)
    # 获取He2000.gro
    p1 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p1.communicate(he_packmol_pdb_file_name.encode() + "\n2\n\n0\n".encode())
    # 获取He.itp, He.top
    p2 = subprocess.Popen(sobtop_dir + "./sobtop\n", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p2.communicate(he_pdb_file_name.encode() + "\n1\n1\n0\n4\n\n\n0\n".encode())

    he2000_gro_file_name = he_packmol_pdb_file_name.split('.')[0] + ".gro"
    he_itp_file_name = he_pdb_file_name.split('.')[0] + ".itp"
    he_top_file_name = he_pdb_file_name.split('.')[0] + ".top"

    shutil.copy(he2000_gro_file_name, current_dir + fold_name)
    shutil.copy(he_packmol_pdb_file_name, current_dir + fold_name)

    shutil.copy(he_itp_file_name, current_dir + fold_name)
    shutil.copy(he_top_file_name, current_dir + fold_name)
    shutil.copy(he_pdb_file_name, current_dir + fold_name)

    os.remove(sobtop_dir + he2000_gro_file_name)
    os.remove(sobtop_dir + he_packmol_pdb_file_name)
    os.remove(sobtop_dir + he_itp_file_name)
    os.remove(sobtop_dir + he_top_file_name)
    os.remove(sobtop_dir + he_pdb_file_name)

    os.chdir(current_dir + fold_name)


def reset_size():
    # 获取npt后的小分子坐标
    with open("npt_small_mol.gro", 'r', encoding='utf-8') as frnptsm:
        frnptsm_context = frnptsm.readlines()
        # npt_sm_x = frnptsm_context[-1].split()[0]
        npt_sm_y = ' '.join(frnptsm_context[-1].split()).split(' ')[1]
    frnptsm.close()

    # 重设盒子大小, 分子筛变更回初始大小
    input_mol_sie_file_name = mol_sie_pdb_file_name.split('.')[0] + "_1A.gro"
    output_mol_sie_file_name = mol_sie_pdb_file_name.split('.')[0] + "_1A_box.gro"
    reset_mol_sie_box_size_cmd = gmxdir + "gmx editconf -f " + input_mol_sie_file_name + " -o " + output_mol_sie_file_name + " -c -box " \
                                 + str(float(mol_sie_x) / 10) + " " + str(float(mol_sie_y) / 10) + " " + str(
        float(
            mol_sie_z) / 10)
    subprocess.run(reset_mol_sie_box_size_cmd, shell=True)

    # 小分子尺寸
    input_small_mol_file_name = 'npt_small_mol.gro'
    output_small_mol_file_name = 'npt_small_mol_box.gro'
    reset_small_mol_box_size_cmd = gmxdir + "gmx editconf -f " + input_small_mol_file_name + " -o " + output_small_mol_file_name + " -c -box " \
                                   + str(float(mol_sie_x) / 10) + " " + str((float(mol_sie_y) / 10 + float(gaps) + float(npt_sm_y) / 2) * 2) + " "  + str(float(
        mol_sie_z) / 10)
    subprocess.run(reset_small_mol_box_size_cmd, shell=True)

    # He wall尺寸
    input_he2000_file_name = "He2000.gro"
    output_he2000_file_name = "he2000_box.gro"
    reset_he2000_box_size_cmd = gmxdir + "gmx editconf -f " + input_he2000_file_name + " -o " + output_he2000_file_name + " -c -box " \
                                 + str(
        float(mol_sie_x) / 10) + " " + str((float(mol_sie_y) / 10 + float(gaps) + float(npt_sm_y) + float(gaps) + 1 / 2) * 2) + " "+ str(float(
        mol_sie_z) / 10)
    subprocess.run(reset_he2000_box_size_cmd, shell=True)


def process_grofile(molsie_gro, lig_gro, he_gro):
    # 分子筛
    with open(molsie_gro, 'r', encoding='utf-8') as ms:
        ms_content = ms.readlines()
        ms1 = ms_content[0]
        ms2 = ms_content[1]
        ms_mol = "".join(ms_content[2:-1])
        ms_last = ms_content[-1]
    ms.close()

    # 小分子
    with open(lig_gro, 'r', encoding='utf-8') as lig:
        lig_content = lig.readlines()
        lig2 = lig_content[1]
        lig_mol = "".join(lig_content[2:-1])
        lig_mol2lig = lig_mol.replace("MOL", "LIG")
    lig.close()

    # He walls
    with open(he_gro, 'r', encoding='utf-8') as he:
        he_content = he.readlines()
        he2 = he_content[1]
        he_mol = "".join(he_content[2:-1])
        he_mol2wal = he_mol.replace("MOL", "WAL")
    he.close()
    # 计算总原子数
    total_atom_num = int(ms2) + int(lig2) + int(he2)
    # 合并文件
    complex_gro = ms1 + str(total_atom_num) + "\n" + ms_mol + lig_mol2lig + he_mol2wal + ms_last

    with open("complex.gro", "w", encoding="utf-8") as cm:
        cm.write(complex_gro)
    cm.close()


def merge_complex_gro():
    mol_sie_box_gro_file_name = mol_sie_pdb_file_name.split('.')[0] + "_1A_box.gro"
    small_mol_box_gro_file_name = 'npt_small_mol_box.gro'
    he_box_gro_file_name = "he2000_box.gro"
    process_grofile(mol_sie_box_gro_file_name, small_mol_box_gro_file_name, he_box_gro_file_name)


def reset_complex_gro_box():
    # 获取分子筛原始坐标
    with open(mol_sie_pdb_file_name, 'r', encoding='utf-8') as frms:
        frms_context = frms.readlines()
        mol_sie_x = frms_context[1].split()[1]
        mol_sie_y = frms_context[1].split()[2]
        mol_sie_z = frms_context[1].split()[3]
        mol_sie_anglex = frms_context[1].split()[4]
        mol_sie_angley = frms_context[1].split()[5]
        mol_sie_anglez = frms_context[1].split()[6]
    frms.close()

    # 获取小分子坐标
    with open("npt_small_mol.gro", 'r', encoding='utf-8') as frnptsm:
        frnptsm_context = frnptsm.readlines()
        # npt_sm_x = frnptsm_context[-1].split()[0]
        npt_sm_y = ' '.join(frnptsm_context[-1].split()).split(' ')[1]
    frnptsm.close()

    # 重设complex.gro盒子大小, 真空区为2倍原子区
    input_complex_gro_file = "complex.gro"
    output_reset_complex_gro_file_name = "complex_box.gro"
    reset_y = float(mol_sie_y) / 10 + float(gaps) + float(npt_sm_y) + float(gaps) + 1 + float(npt_sm_y) * 2
    reset_complex_gro_box_cmd = gmxdir + "gmx editconf -f " + input_complex_gro_file + " -o " + output_reset_complex_gro_file_name + " -c -box " \
                                + str(float(mol_sie_x) / 10) + " " + str(reset_y) + " "  + str(
        float(
            mol_sie_z) / 10)
    subprocess.run(reset_complex_gro_box_cmd, shell=True)


def translate_complex_gro_box():
    # 平移复合物盒子到边缘
    input_file = "complex_box.gro"
    output_name = "complex_trans.gro"
    # 获取分子筛原始坐标
    with open(mol_sie_pdb_file_name, 'r', encoding='utf-8') as frms:
        frms_context = frms.readlines()
        mol_sie_x = frms_context[1].split()[1]

    frms.close()

    # 获取npt后的小分子坐标
    with open("npt_small_mol.gro", 'r', encoding='utf-8') as frnptsm:
        frnptsm_context = frnptsm.readlines()
        # npt_sm_x = frnptsm_context[-1].split()[0]
        npt_sm_y = ' '.join(frnptsm_context[-1].split()).split(' ')[1]
    frnptsm.close()

    reset_y = float(mol_sie_y) / 10 + float(gaps) + float(npt_sm_y) + float(gaps) + 1 + float(npt_sm_y) * 2
    translate_y = reset_y / 2 - (float(mol_sie_y) / 10 + float(gaps) + float(npt_sm_y) + float(gaps) + 1) / 2

    translate_xyz = "0 " + str(float(translate_y)) + " 0"
    translate_cmd = gmxdir + "gmx editconf -f " + input_file + " -o " + output_name + " -translate " + translate_xyz
    subprocess.run(translate_cmd, shell=True)


def generate_porse_itp():
    mol_sie_output_name = mol_sie_pdb_file_name.split(".")[0] + "_1A_posre.itp"
    he_posre_itp_output_name = "he2000_posre.itp"
    mol_sie_genrestr_cmd = "gmx genrestr -f " + mol_sie_pdb_file_name + " -o " + mol_sie_output_name
    he_genrestr_cmd = "gmx genrestr -f He.pdb" + " -o " + he_posre_itp_output_name
    p1 = subprocess.Popen(gmxdir + mol_sie_genrestr_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p1.communicate("2\n".encode())
    p2 = subprocess.Popen(gmxdir + he_genrestr_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p2.communicate("2\n".encode())


def create_minim_mdp_file():
    with open("minim.mdp", 'w', encoding='utf-8') as fwmin:
        fwmin.write("integrator = steep\n"
                    "emtol = 1000.0\n"
                    "emstep = 0.01\n"
                    "nsteps = 50000\n"
                    "nstlist = 40\n"
                    "cutoff-scheme = Verlet\n"
                    "ns_type = grid\n"
                    "coulombtype = PME\n"
                    "rcoulomb = 1.2\n"
                    "rvdw = 1.2\n"
                    "pbc = xyz")
    fwmin.close()


def create_topol_file(small_mol_pdb_file_name):
    # 将3个top文件整合成一个新的topol文件
    mol_sie_top_file = mol_sie_pdb_file_name.split('.')[0] + "_1A.top"
    small_mol_top_file = small_mol_pdb_file_name.split('.')[0] + ".top"
    he_top_file = "He.top"
    # 取前面相同的行
    with open(mol_sie_top_file, 'r', encoding='utf-8') as f1:
        f1_context = f1.readlines()
        common_line = ''
        mol_sie_include_rows = ""
        mol_sie_count = ''
        for f1_line in f1_context[:6]:
            common_line += f1_line
        for include_row1 in f1_context:
            if "include" in include_row1:
                mol_sie_include_rows = include_row1
            else:
                mol_sie_count = include_row1
    f1.close()
    # print(common_line)
    # print(mol_sie_include_rows)
    # print(mol_sie_count)
    # 取小分子的include和数量行
    with open(small_mol_top_file, 'r', encoding='utf-8') as f2:
        f2_context = f2.readlines()
        small_mol_include_rows = ""
        small_mol_count = ''
        for include_row2 in f2_context:
            if "include" in include_row2:
                small_mol_include_rows = include_row2
            else:
                small_mol_count = include_row2
    # 取he的include行和数量
    with open(he_top_file, 'r', encoding='utf-8') as f3:
        f3_context = f3.readlines()
        he_include_rows = ""
        he_count = ''
        for include_row3 in f3_context:
            if "include" in include_row3:
                he_include_rows = include_row3
            else:
                he_count = "He\t2000"

    # 整合上述取出来的数据
    mol_sie_posre = "#ifdef POSRES\n#include " + "\"" + mol_sie_pdb_file_name.split('.')[
        0] + "_1A_posre.itp\"\n#endif\n\n"
    he_posre = "#ifdef POSRES\n#include \"he2000_posre.itp\"\n#endif\n\n"
    with open("topol.top", 'w', encoding='utf-8') as fwtop:
        fwtop.write(
            common_line + mol_sie_include_rows + mol_sie_posre + small_mol_include_rows + '\n' + he_include_rows + he_posre
            + "[ system ]\ncomplex\n\n[ molecules ]\n; Molecule      nmols\n" + mol_sie_count + small_mol_count + '\n' + he_count)
    fwtop.close()


def modify_itp():
    # 处理分子筛的itp文件,
    molsie_output_file_name = mol_sie_pdb_file_name.split('.')[0] + "_mod.itp"
    process_molsie_itp_cmd = "cat " + mol_sie_itp_file_name \
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
    subprocess.run("mv " + molsie_output_file_name + " " + mol_sie_itp_file_name, shell=True)
    with open(mol_sie_itp_file_name, 'r', encoding='utf-8') as f1:
        f1_context = f1.readlines()
        molsie_moleculetype_row = ''
        molsie_atomtype = ""
        molsie_othercontext = ""
        for i, molsie in enumerate(f1_context):
            # print(molsie)
            if molsie == "[ moleculetype ]\n":
                molsie_moleculetype_row = i
        for atomtype in f1_context[:molsie_moleculetype_row]:
            molsie_atomtype += atomtype
        for othercontext in f1_context[molsie_moleculetype_row:]:
            molsie_othercontext += othercontext
    f1.close()
    # print(molsie_moleculetype_row)
    # print(molsie_atomtype)
    # print(molsie_othercontext)

    # 小分子
    with open(small_mol_itp_file_name, 'r', encoding='utf-8') as f2:
        f2_context = f2.readlines()
        sm_moleculetype_row = ''
        sm_atomtype = ""
        sm_othercontext = ""
        for j, sm in enumerate(f2_context):
            if sm == "[ moleculetype ]\n":
                sm_moleculetype_row = j
        for atomtype in f2_context[4:sm_moleculetype_row]:
            sm_atomtype += atomtype
        for othercontext in f2_context[sm_moleculetype_row:]:
            sm_othercontext += othercontext
    f2.close()
    # print(sm_atomtype)

    # He
    with open(he_itp_file_name, 'r', encoding='utf-8') as f3:
        f3_context = f3.readlines()
        he_moleculetype_row = ''
        he_atomtype = ""
        he_othercontext = ''
        for k, he in enumerate(f3_context):
            if he == "[ moleculetype ]\n":
                he_moleculetype_row = k
        for atomtype in f3_context[4:he_moleculetype_row]:
            he_atomtype += atomtype
        for othercontext in f3_context[he_moleculetype_row:]:
            he_othercontext += othercontext
    f3.close()
    # print(he_atomtype)
    merge_atomtype = molsie_atomtype + sm_atomtype + he_atomtype
    # print(merge_atomtype)
    # 重写itp文件
    with open(mol_sie_itp_file_name, 'w', encoding='utf-8') as fw1:
        fw1.write(merge_atomtype + molsie_othercontext)
    fw1.close()
    with open(small_mol_itp_file_name, 'w', encoding='utf-8') as fw2:
        fw2.write(sm_othercontext)
    fw2.close()
    with open(he_itp_file_name, 'w', encoding='utf-8') as fw3:
        fw3.write(he_othercontext)
    fw3.close()


def nvt_md_pbc_mdp():
    run_time = int(run_time_ns) * 1000000 / 2
    nvt_md_pbc_mdp_file_name = "nvt_md_pbc.mdp"
    with open(nvt_md_pbc_mdp_file_name, 'w', encoding='utf-8') as fwnvt:
        fwnvt.write("; Processing\n"
                    "define = -DPOSRES\n\n"
                    "; Run Control\n"
                    "integrator = md\n"
                    "dt = 0.002\n"
                    "nsteps = "
                    + str(int(run_time))
                    + '\n'
                      'comm-grps = system\n\n'
                      '; Output Control\n'
                      'nstxout = 250000\n'
                      'nstvout = 250000\n'
                      'nstfout = 250000\n'
                      'nstlog = 250000\n'
                      'nstenergy = 250000\n'
                      'nstxout-compressed = 250000\n'
                      'compressed-x-grps = system\n\n'
                      '; Neighbor searching\n'
                      'cutoff-scheme = verlet\n'
                      'nstlist = 40\n'
                      'pbc = xyz\n'
                      'periodic-molecules = yes\n'
                      'rlist = 2.0\n\n'
                      '; Electrostatics\n'
                      'coulombtype = PME\n'
                      'rcoulomb = 2.0\n\n'
                      '; Van der Waals\n'
                      'vdwtype = cut-off\n'
                      'rvdw = 2.0\n'
                      'DispCorr = no\n\n'
                      '; Temperature coupling\n'
                      'Tcoupl = V-rescale\n'
                      'tc_grps = system\n'
                      'tau_t = 0.2\n'
                      'ref_t = '
                    + temp
                    + '\n\n'
                      '; Velocity generation\n'
                      'gen_vel = yes\n'
                      'gen_temp = 100\n '
                      'gen_seed = -1\n\n'
                      '; Bonds\n'
                      'constraints = hbonds')


if __name__ == '__main__':
    sobtop_dir = "/home/essex/Downloads/sobtop/sobtop_1.0_dev3.1/"
    obabel_dir = "/home/essex/Downloads/openbabel/build/bin/"
    resp_orca_dir = "/home/essex/Downloads/Multiwfn/Multiwfn_3.8_dev_bin_Linux/examples/RESP/"
    gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量

    current_dir = os.getcwd() + "/"
    print(current_dir)
    mol_sie_pdb_file_name = "MTW_414.pdb"
    he_pdb_file_name = "He.pdb"
    construct_small_mol_count = "500"

    x = "102"
    y = "40"
    z = "48"
    gaps = "2"

    # 获取分子筛原始坐标
    with open(mol_sie_pdb_file_name, 'r', encoding='utf-8') as frms:
        frms_context = frms.readlines()
        mol_sie_x = frms_context[1].split()[1]
        mol_sie_y = frms_context[1].split()[2]
        mol_sie_z = frms_context[1].split()[3]
        mol_sie_anglex = frms_context[1].split()[4]
        mol_sie_angley = frms_context[1].split()[5]
        mol_sie_anglez = frms_context[1].split()[6]
    frms.close()

    mol_sie_itp_file_name = mol_sie_pdb_file_name.split('.')[0] + "_1A.itp"
    he_itp_file_name = "He.itp"

    # 运行时间,ns为单位
    run_time_ns = "100"
    temp = "773"

    all_pdb_file = glob.glob('*.pdb')
    # print(all_pdb_file)
    exclude_pdb_file_name = [mol_sie_pdb_file_name, he_pdb_file_name]
    for sm_pdb_file in all_pdb_file:
        if sm_pdb_file not in exclude_pdb_file_name:
            small_mol_itp_file_name = sm_pdb_file.split(".")[0] + ".itp"
            fold_name = sm_pdb_file.split('.')[0] + "_" + mol_sie_pdb_file_name.split("_")[0] + "_" + construct_small_mol_count
            if not os.path.exists(fold_name):
                os.mkdir(fold_name)
                # print("1")
                # subprocess.run("mv " + current_dir + sm_pdb_file + " " + current_dir + fold_name, shell=True)
                shutil.copy(sm_pdb_file, fold_name)
                shutil.copy(mol_sie_pdb_file_name, fold_name)
                shutil.copy(he_pdb_file_name, fold_name)
            else:
                # print("2")
                # subprocess.run("mv " + current_dir + sm_pdb_file + " " + current_dir + fold_name, shell=True)
                shutil.copy(sm_pdb_file, fold_name)
                shutil.copy(mol_sie_pdb_file_name, fold_name)
                shutil.copy(he_pdb_file_name, fold_name)
            # 进入目录
            os.chdir(fold_name)

            # 每一个小分子生成初始模型
            packmol_sm_and_sobtop_pdb2gro(sm_pdb_file)
            sobtop_pdb_to_mol2_and_get_itptop(sm_pdb_file)
            cal_resp_and_replace(sm_pdb_file)
            modify_top_small_mol_count(sm_pdb_file)
            get_minim_npt_mdp_file()
            minim_npt_small_mol(sm_pdb_file)
            get_mol_sieve_gro_itp_top()
            packmol_he2000()
            reset_size()
            merge_complex_gro()
            reset_complex_gro_box()
            translate_complex_gro_box()
            generate_porse_itp()
            create_minim_mdp_file()
            create_topol_file(sm_pdb_file)
            modify_itp()
            nvt_md_pbc_mdp()
            # 退出当前目前
            os.chdir(current_dir)

    # small_mol_pdb_file_name = input("请输入小分子的pdb文件名: ")
    # mol_sie_pdb_file_name = input("请输入分子筛的pdb文件名: ")
    # construct_small_mol_count = input("请输入构建的数量: ")
    # small_mol_pdb_file_name = "1-2-methylnaphthalene.pdb"
    # 坐标根据分子筛的尺寸来设置
    # x = input("请输入构建的盒子的x坐标: ")
    # y = input("请输入构建的盒子的y坐标: ")
    # z = input("请输入构建的盒子的z坐标: ")

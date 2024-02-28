#!/usr/bin/python

# author:bob
# created time: 2023-08-25
# function: use to process molecular sieve
import os
import subprocess
import shutil

# gmx运行路径,根据安装路径进行修改
gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量
sobtop_dir = "/home/essex/Downloads/sobtop/sobtop_1.0_dev3.1/"
current_dir = os.getcwd()

# 1. 四周增加1A距离,防止边缘周期性问题
input_molecular_sieve_name = input("please enter the molecular_sieve pdb name: ")
output_name = input_molecular_sieve_name.split(".")[0] + "_1A.pdb"

# 打开pdb文件,读取第二行信息
with open(input_molecular_sieve_name, "r", encoding="utf-8") as f:
    # 提取第二行信息,并且将多个空格置换成一个逗号(或一个空格)
    second_context = ",".join(f.readlines()[1].split())
    # 提取第2,3,4列数据作为xyz坐标,同时进行单位换算,转换成nm
    x = float(second_context.split(",")[1]) / 10 + 1
    y = float(second_context.split(",")[2]) / 10 + 1
    z = float(second_context.split(",")[3]) / 10 + 1
f.close()
editconf_cmd = gmxdir + "gmx editconf -f " + input_molecular_sieve_name + " -o " + output_name \
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
shutil.move(output_name, sobtop_dir)
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
shutil.move(output_name, current_dir)
shutil.move(itp_name, current_dir)
shutil.move(gro_name, current_dir)
shutil.move(top_name, current_dir)

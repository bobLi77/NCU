#!/home/essex/datas/bob/NCU/env/bin/python

# author:bob
# created time: 2023-09-22
# function: 用于批量计算MSD,输出xvg数据作图
import pexpect
import os
# 获取当前路径
current_path = os.getcwd()
# 遍历,获取所有文件名
for file_name in os.listdir(current_path):
    # 判断当前名字是否为文件夹
    if os.path.isdir(file_name):
        # 进入到该文件夹下
        os.chdir(file_name)
        # 运行msd计算,分别计算12个小分子, 即A-L字母标识
        for i in range(12):
            output_name = "msd_" +file_name + "_" + str(i+3)
            msd_cmd = "gmx msd -f nvt_cmp_mix_200ns.xtc -s nvt_cmp_mix_200ns.gro -o " + output_name + " -beginfit -1 -endfit -1"
            child = pexpect.spawn(msd_cmd)
            child.sendline(str(i+3))
            child.sendcontrol("d")
            child.expect(pexpect.EOF)
        os.chdir(current_path)

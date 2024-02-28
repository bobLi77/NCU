#!/home/essex/datas/bob/NCU/env/bin/python

# author:bob
# created time: 2023-09-22
# function: 用于批量计算MSD,输出xvg数据作图
import pexpect
import os
import subprocess
# 获取当前路径
current_path = os.getcwd()
# 遍历,获取所有文件名
for file_name in os.listdir(current_path):
    # 判断当前名字是否为文件夹
    if os.path.isdir(file_name):
        # 进入到该文件夹下
        os.chdir(file_name)
        # 将小分子字母识别全部换成同一类
        # 替换标签
        # atom_index = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL"]
        with open("nvt_cmp_mix_200ns.gro",'r',encoding='utf-8') as fr:
            cnt = fr.read().replace("BBB","AAA").replace("CCC",'AAA').replace("DDD",'AAA').replace("EEE",'AAA')\
                .replace("FFF",'AAA').replace("GGG",'AAA').replace("HHH",'AAA').replace("III",'AAA')\
                .replace("JJJ",'AAA').replace("KKK",'AAA').replace("LLL",'AAA')
        fr.close()
        with open("nvt_cmp_mix_200ns.gro",'w',encoding='utf-8') as fw:
            fw.write(cnt)
        fw.close()
        # 运行msd计算,分别计算12个小分子, 即A-L字母标识
        output_name = "msd_" + file_name + "_single.xvg"
        msd_cmd = "gmx msd -f nvt_cmp_mix_200ns.xtc -s nvt_cmp_mix_200ns.gro -o " + output_name + " -beginfit -1 -endfit -1"
        child = pexpect.spawn(msd_cmd)
        child.sendline(str(3))
        child.sendcontrol("d")
        child.expect(pexpect.EOF)
        os.chdir(current_path)


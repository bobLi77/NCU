#!/home/essex/datas/bob/NCU/env/bin/python
# author:bob
# created time: 2023-09-22
# 功能:
# 1. 重命名gro文件中的小分子名称, 用于区分混合体系中不同的小分子类型
# 2. 计算每一类小分子的MSD, 输出xvg格式文件
# 3. 处理xvg文件,提取msd数据,导出excel

import os
import pexpect
import glob
import pandas as pd


def gro_rename_sm():
    current_path = os.getcwd() + "/"
    gro_file_name = "nvt_cmp_mix_200ns.gro"
    # 获取当前路径下所有文件夹名字
    for fold_name in os.listdir(current_path):
        # 判断是否为文件夹
        if os.path.isdir(current_path + fold_name):
            # print(fold_name)
            # 进入文件夹
            os.chdir(fold_name)
            # 读取文件
            with open(os.path.join(current_path, fold_name, gro_file_name), "r", encoding="utf-8") as f:
                sm_count = 0
                he_count = 0
                content = f.readlines()
                # 获取sm的起始行索引
                for first_rows_index in content:
                    if "2MOL" in first_rows_index:
                        # print(sm_count)
                        break
                    sm_count += 1
                # 指针回到初始位置,否则文件读完一次就到末尾了
                f.seek(0)
                # 获取sm的末索引
                for row_he_index in content:
                    if "HE" in row_he_index:
                        # print(he_count)
                        break
                    he_count += 1
                # 提取sm的区间
                f.seek(0)
                # 开头至分子筛区间
                molsie = content[:sm_count]
                # 小分子的区间
                row_sm = content[sm_count:he_count]
                # he至末尾 区间
                he = content[he_count:]
                # 存放替换后的sm
                final_merge_single_sm = ""
                # 替换标签
                atom_index = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL"]
                # tmp_sm_content = fo.readlines()

                # 一共有12个小分子, 循环12次
                # print(row_sm)

                for i in range(12):
                    first_rows_count = 0
                    last_rows_count = 0
                    first_rows_string = str((100 * i + 2)) + "MOL"
                    last_rows_string = str((100 * (i + 1) + 2)) + "MOL"
                    for row_first in row_sm:
                        if first_rows_string in row_first:
                            break
                        first_rows_count += 1
                    for row_last in row_sm:
                        if last_rows_string in row_last:
                            break
                        last_rows_count += 1

                    single_sm = row_sm[first_rows_count:last_rows_count]
                    for j in single_sm:
                        final_merge_single_sm += j.replace("MOL", atom_index[i])

                # 重新组装成gro文件
                str_molsie = ""
                str_he = ""
                for ms in molsie:
                    str_molsie += ms
                for h in he:
                    str_he += h
                final_res = str_molsie + final_merge_single_sm + str_he
                # print(final_res)
                with open("nvt_cmp_mix_200ns.gro", "w", encoding="utf-8") as fw:
                    fw.write(final_res)
                fw.close()
            f.close()
            # 返回当前目前
            os.chdir(current_path)


def cal_msd():
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
                output_name = "msd_" + file_name + "_" + str(i + 3)
                msd_cmd = "gmx msd -f nvt_cmp_mix_200ns.xtc -s nvt_cmp_mix_200ns.gro -o " + output_name
                child = pexpect.spawn(msd_cmd)
                child.sendline(str(i + 3))
                child.sendcontrol("d")
                child.expect(pexpect.EOF)
            os.chdir(current_path)


def get_msd_from_xvg():
    current_path = os.getcwd()
    file_name_lt = []
    all_msd_lt = []
    for file_name in os.listdir(current_path):
        if os.path.isdir(file_name):
            file_name_lt.append(file_name)
            os.chdir(file_name)
            # 获取所有xvg文件名,返回list
            xvg_file = glob.glob("*.xvg")
            msd_lt = []
            for xvg in xvg_file:
                with open(xvg, "r", encoding="utf-8") as fx:
                    content = fx.readlines()
                    for line in content:
                        if "legend \"D" in line:
                            msd_data = line.split("=")[1].split("(")[0].strip()
                            msd_lt.append(float(msd_data))
                            break
            all_msd_lt.append(msd_lt)
            os.chdir(current_path)
    # print(all_msd_lt)

    # 构造DataFrame
    data = pd.DataFrame(all_msd_lt)
    # 行列互换,表格好看点,也可以不互换
    datas = pd.DataFrame(data.values.T, columns=file_name_lt)
    datas.to_excel("msd.xlsx", sheet_name="sheet1", index=True)


if __name__ == "__main__":
    gro_rename_sm()
    cal_msd()
    get_msd_from_xvg()

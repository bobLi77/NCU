#!/usr/bin/python

# author:bob
# created time: 2023-09-15
# function: use to rename the atom name of the final gro file, MOL to others, distinguish different small molecular

# 批量处理, 最终的gro文件存放于文件夹中
import os

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
                last_rows_string  = str((100 * (i+1) + 2)) + "MOL"
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

#!/usr/bin/python
# author:bob
# created time: 2024-1-11
# function:
# 1. 计算轨迹的扩散量
import json
import os


def get_min_max_coordination():
    # 获取分子筛-He wall的坐标,排序得到最大最小值,不在该值范围内的就是扩散的坐标
    with open(trj_file, 'r', encoding='utf-8') as fr:
        cnt = fr.readlines()
        z_lt = []
        max_min_lt = []
        for line in cnt[2:-1]:
            strip_space = " ".join(line.split())
            mol_he = strip_space.split(' ')[0]
            # 分子筛和He标识都有MOL,小分子被修改了,没有该标识
            if "MOL" in mol_he:
                mol_he_two = strip_space.split(' ')[1]
                mol_he_five = float(strip_space.split(' ')[2])
                mol_he_six = float(strip_space.split(' ')[3])
                if mol_he_two.isalpha():
                    z_lt.append(mol_he_six)
                else:
                    z_lt.append(mol_he_five)

            # print(line)
        max_z = max(z_lt)
        min_z = min(z_lt)
        max_min_lt.append(max_z)
        max_min_lt.append(min_z)
    fr.close()
    # print(max_min_lt[0])
    # print(max_min_lt[-1])
    # print(max_min_lt)
    return max_min_lt


def get_diffused_capicity():
    max_min = get_min_max_coordination()
    maxs = max_min[0]
    mins = max_min[-1]
    # print(maxs)
    # print(mins)
    with open(trj_file, 'r', encoding='utf-8') as fr:
        cnt = fr.readlines()
        last_row = cnt[-1]
        # print(type(last_row))
        diffused_lt = []
        for line in cnt[2:-1]:
            # temp_lt = []
            # 将多个空格置换成一个
            z = ' '.join(line.split())
            z_two = z.split(' ')[1]
            z_five = z.split(' ')[2]
            z_six = z.split(' ')[3]
            # print(z_two)
            # print(z_six)
            if z_two.isalpha():
                if float(z_six) < mins or float(z_six) > maxs:
                    diffused_lt.append(line)
            else:
                if float(z_five) < mins or float(z_five) > maxs:
                    diffused_lt.append(line)

    fr.close()

    li_name_lt = []
    for lines in diffused_lt:
        li_name = ' '.join(lines.split()).split(' ')[0]
        # print(li_name)
        li_name_lt.append(li_name)
    set_li = list(set(li_name_lt))
    set_li.sort(key=li_name_lt.index)
    final_lt = []
    for name in set_li:
        for li in cnt[2:-1]:
            zi = ' '.join(li.split())
            if zi.split(' ')[0] == name:
                final_lt.append(li)

    with open("diffused_capacity.gro", 'w', encoding='utf-8') as fw:
        rewrite_cnt = ""
        counts = len(final_lt)
        for lines in final_lt:
            rewrite_cnt += lines
        fw.write("diffused mol\n" + str(counts) + "\n" + rewrite_cnt + last_row)
    fw.close()

    # 统计每一类分子有多少个
    sm_name_lt = []
    for single_sm in final_lt:
        strip_space = " ".join(single_sm.split())
        sm_name = strip_space.split(' ')[0]
        sm_name_lt.append(sm_name)
    # 去重
    set_sm_name_lt = list(set(sm_name_lt))
    # 按原来列表顺序重排
    set_sm_name_lt.sort(key=sm_name_lt.index)
    # 查找每一类小分子有多少个
    atom_index = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL"]
    sm_dict = {}
    for ai in atom_index:
        num = 0
        for sm in set_sm_name_lt:
            if ai in sm:
                num += 1
        sm_dict.update({
            ai: num,
        })
    with open(fold_name + "_sm_num.txt", 'w', encoding='utf-8') as fsmw:
        # indent = 1 换行显示,按照json格式输出
        fsmw.write(json.dumps(sm_dict, indent=1))
    fsmw.close()
    # print(sm_dict)
    # print(set_sm_name_lt)


if __name__ == '__main__':
    trj_file = "nvt_cmp_mix_200ns.gro"
    current_path = os.getcwd()
    all_fold = os.listdir(current_path)
    for fold_name in all_fold:
        # print(fold_name)
        os.chdir(fold_name)
        get_min_max_coordination()
        get_diffused_capicity()
        os.chdir(current_path)

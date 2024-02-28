#!/usr/bin/python

# author:bob
# created time: 2023-10-27
# function: 用于合并gro文件为复合物

# molecular_sieve_gro_file = input("请输入分子筛的gro文件: ")
# small_molecular_gro_file = input("请输入小分子的gro文件: ")
# he_gro_file = input("请输入he的gro文件: ")

molecular_sieve_gro_file = "AEL2a144_1A_box.gro"
small_molecular_gro_file = "npt_cmp500_box.gro"
he_gro_file = "he2000_box.gro"

str_ms_context = ''
str_sm_context = ''
str_he_context = ''
int_ms_atomnum = 0
int_sm_atomnum = 0
int_he_atomnum = 0
total_atomnum = 0

with open(molecular_sieve_gro_file, 'r', encoding="utf-8") as ms:
    ms_lines = ms.readlines()
    ms_atomnum = ms_lines[1:2]
    ms_context = ms_lines[2:-1]
    ms_coordinate = ms_lines[-1]

with open(small_molecular_gro_file, 'r', encoding='utf-8') as sm:
    sm_lines = sm.readlines()
    sm_atomnum = sm_lines[1:2]
    sm_context = sm_lines[2:-1]

with open(he_gro_file, 'r', encoding='utf-8') as he:
    he_lines = he.readlines()
    he_atomnum = he_lines[1:2]
    he_context = he_lines[2:-1]

for ms_line in ms_context:
    str_ms_context += ms_line

for sm_line in sm_context:
    replace_sm_line = sm_line.replace('MOL','LIG')
    str_sm_context += replace_sm_line

for he_line in he_context:
    str_he_context += he_line


for a in ms_atomnum:
    int_ms_atomnum = int(a)

for b in sm_atomnum:
    int_sm_atomnum = int(b)

for c in he_atomnum:
    int_he_atomnum = int(c)

total_atomnum = int_ms_atomnum + int_sm_atomnum + int_he_atomnum

with open("complex.gro", 'w', encoding='utf-8') as cmp:
    cmp.write("merge gro file" + '\n' + str(
        total_atomnum) + '\n'+  str_ms_context + str_sm_context + str_he_context + str(ms_coordinate))

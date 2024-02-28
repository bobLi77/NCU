#!/bin/bash

# author:bob
# created time: 2023-08-25
# function: assemble complex gro file from xxx_1A.gro, xxx_cmp100_box.gro, xxx_he2000_box.gro
# modify time: 2023-08-31, use various and customize input

# -r可以对反斜杠转义
read -r -p "请输入分子筛gro文件: " molsie
read -r -p "请输入小分子gro文件: " lig
read -r -p "请输入He的gro文件: " he

# 1. 将小分子文件的标识类型修改,MOL改成LIG, 防止与分子筛的文件MOL同名导致异常
cmp100_lig=$(cat "${lig}" | sed 's/MOL/LIG/g')
#echo "$cmp100_lig"
# 2. 删除前两行和最后一行,只取原子坐标部分
# 提取前两行
molsie_first=$(cat "${molsie}" | sed -n '1p')
a=$(cat "${molsie}" | sed -n '2p' | awk '{print int($0)}')
b=$(cat "${lig}" | sed -n '2p' | awk '{print int($0)}')
c=$(cat "${he}" | sed -n '2p'| awk '{print int($0)}')
# 通过let函数对变量求和

#atoms_num=`expr ("${a}" + "${b}") + "${c})`
atoms_num=$((a+b+c))
echo $atoms_num

## 提取最后一行
molsie_last=$(cat "${a}" | tail -1)
## 删除前两行和最后一行
molsie_del=$(cat "${a}" | sed 1,2d | sed '$d')
cmp100_del=$(echo "$cmp100_lig" | sed 1,2d | sed '$d')
#echo "$cmp100_del"
he2000_del=$(cat "${he}" | sed 1,2d | sed '$d')
#
## 3. 合并文件
"${molsie_first}\n${atoms_num}\n${molsie_del}\n${cmp100_del}\n${he2000_del}\n${molsie_last}" > cmp_mix.gro



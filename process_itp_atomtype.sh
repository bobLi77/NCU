#!/bin/bash

# created time: 2023-08-01
# author : 梁柏强 bob
# 功能: 用于处理分子筛itp文件,用于gromacs
# 说明: 分子筛是由MS构建所得,由于其存在周期性, 直接通过sobtop或者其他方法从pdb获取itp文件后, 其中的 bonds 和 angles存在问题
# (由于周期性原因,最左边的原子和最右边的原子有键角连接关系,在扩大盒子后,这部分连接会出现异常The largest distance between excluded atoms is xxx nm...)
# 因此在构建前先在分子筛周围一圈加真空(即扩大盒子),使这些键角正常,这是比较快的方法,如果在构建后再修改这些键角,由于体系非常大,一个个修改不太现实;
# 但在加一圈真空后, 通过sobtop生成itp,这部分原子不能被识别, 使用UFF原子类型先定义,使程序正常生成itp文件,再对该itp文件进行修改;
# 该脚本适用于Si-O 类型分子筛

read -p "请输入itp文件名: " name
cat $name | sed 's/UF_Si      1      MOL/Si_bulk    1      MOL/g' | sed 's/0.00000000   28.085499/1.10000000   28.085499/g' |
 sed 's/UF_O       1      MOL      O/O_bulk     1      MOL      O/g' | sed 's/ 0.00000000   15.999405/-0.55000000   15.999405/g' |
 sed 's/         1        .*     2.500000E+05     /         1        0.165000     2.384880E+05     /g' |
 sed 's/         1       .*      5.000000E+02     /         1       109.500      8.368000E+02     /g' |
 sed 's/         1       .*      5.000000E+02     /         1       149.000      8.368000E+02     /g' |
 sed '/^UF_Si       14    /d' |
 sed '/^UF_O         8    /d' > ${name%.*}_mod.itp
 mv ${name%.*}_mod.itp $name

# 脚本内容说明:
# read -p "请输入文件名: " name   获取用户输入,保存到变量name中;
# cat $name  读取文件;
# sed 's/UF_Si      1      MOL/Si_bulk    1      MOL/g'  文本替换, 将 "UF_Si      1      MOL" 替换成 "Si_bulk    1      MOL";
# sed 's/         1        .*     2.500000E+05     /         1        0.165000     2.384880E+05     /g'  文本替换, .*指代任意内容, 因为这里的数值是不同的,使用.*代替
# sed '/^UF_Si       14    /d'  删除UF_Si       14    开头的行

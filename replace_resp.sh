#!/bin/bash
# created time : 2023-08-03
# author : 梁柏强(bob)
# 功能:
# 1. 用于将计算好的resp电荷(xxx.chg)和itp文件中atoms字段内的电荷进行替换

for chg_name in *.chg;do
  cat ${chg_name%.*}.itp | sed -n '/\[ atoms \]/,/\[ bonds \]/p' | sed '1,2d' | sed '$d' | sed '$d' >atoms_tmp1.txt
  cat $chg_name | awk '{printf "%13s\n", $NF}' | paste atoms_tmp1.txt - | awk '{$7=$NF;print $0}' | awk '{$NF=null;print $0}' | awk '{printf "%6s%7s%10s%9s%8s%12s%14s%12s\n",$1,$2,$3,$4,$5,$6,$7,$8}' >chg_tmp2.txt
  cat ${chg_name%.*}.itp | sed -n '1,/\[ bonds \]/p' | sed -n '1,/Index/p' | cat - chg_tmp2.txt >itp_tmp3.txt
  cat ${chg_name%.*}.itp | sed -n '/\[ bonds \]/,/$p/p' | sed '1i\ ' | cat itp_tmp3.txt - >${chg_name%.*}_resp.itp
  rm *.txt
  mv ${chg_name%.*}_resp.itp ${chg_name%.*}.itp
  echo "RESP电荷已成功替换,请检查当前itp文件"
done


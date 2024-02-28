#!/usr/bin/python


import os
import subprocess
import glob

# 获取当前路径
current_path = os.getcwd()
# 获取所有msd开头,xvg结尾的文件
xvg_file = glob.glob("msd*.xvg")
# 设置初始名字1,然后递增,作为临时名字
num = 1
# 循环xvg文件, 删掉#行,@行,打印第二行msd数据
for xvg in xvg_file:
    xvg_cmd = "cat " + xvg + "| grep -v -E '#|@' | awk '{print $2}' > proxvg_" + str(num) + ".txt"
    subprocess.run(xvg_cmd, shell=True)
    num += 1
# 获取时间列,转换为ns
for xvg in xvg_file:
    time_cmd = "cat " + xvg + "| grep -v -E '#|@'  | awk '{print $1/1000}'  > time.txt"
    subprocess.run(time_cmd, shell=True)
    break

# 获取所有msd临时数据,然后将所有列合并成一个文件
txt_file = glob.glob("proxvg_*.txt")
all_txt_cmd = ""
for txt in txt_file:
    all_txt_cmd += txt + " "
merge_txt_cmd = "paste " + all_txt_cmd + " > merge.txt"
subprocess.run(merge_txt_cmd, shell=True)

# 将时间列与msd数据合并成一个新文件
add_time_cmd = "paste time.txt merge.txt   > merge_time.txt"
subprocess.run(add_time_cmd, shell=True)

# 将行与列互换
row2cols_cmd = "cat merge_time.txt | awk '{for(i=0;++i<=NF;)a[i]=a[i]?a[i] FS $i:$i}END{for(i=0;i++<NF;)print a[i]}' > merge_time_msd.txt"
subprocess.run(row2cols_cmd, shell=True)

# 构建名字文件
with open("smname.txt", 'w', encoding='utf-8') as fw:
    fw.write("Name\n"
             "1,2-dimethylnaphthalene\n"
             "1,3-dimethylnaphthalene\n"
             "1,4-dimethylnaphthalene\n"
             "1,5-dimethylnaphthalene\n"
             "1,6-dimethylnaphthalene\n"
             "1,7-dimethylnaphthalene\n"
             "1,8-dimethylnaphthalene\n"
             "1-methylnaphthalene\n"
             "2,3-dimethylnaphthalene\n"
             "2,6-dimethylnaphthalene\n"
             "2,7-dimethylnaphthalene\n"
             "2-methylnaphthalene")
    fw.close()

# 将名字文件与之前合并的文件合并,组成最终的文件
merge_smname_cmd = "paste smname.txt merge_time_msd.txt > final.xlsx"
subprocess.run(merge_smname_cmd, shell=True)

# # 删除所有临时文件
# all_txt_file = glob.glob("*.txt")
# for t in all_txt_file:
#     os.remove(current_path + "/" + t)

#!/home/essex/datas/bob/NCU/env/bin/python

# author:bob
# created time: 2023-09-22
# function: 用于批量提取XVG中的msd数据,构造dataframe,输出到excel
# 使用方法: 需要将相同类型的数据放在同一个文件夹下, 比如温度300K的数据, 创建一个300K文件夹,
# 该文件夹下再放置不同的文件夹(如不同的分子筛名字),再该分子筛文件夹下放置数据.

import os
import glob
import pandas as pd

# 处理数据
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
            with open(xvg,"r",encoding="utf-8") as fx:
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
datas = pd.DataFrame(data.values.T,columns=file_name_lt)
datas.to_excel("msd.xlsx", sheet_name="sheet1", index=True)




#!/home/essex/datas/bob/NCU/env/bin/python

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# 异常报错，添加TkAgg
matplotlib.use('TkAgg')

excel_file = "final.xlsx"
all_y_axis_data = pd.read_excel(excel_file)
# sm_name = pd.read_excel(excel_file,usecols=[0])
sm_name = all_y_axis_data.iloc[:,0]
y_axis_data = all_y_axis_data.iloc[:, 1:]
# print(sm_name)
# print(sm_name)
# y_axis_data = pd.read_excel(excel_file, usecols=[1, 2, 3, 4, 5, 6])


# print(y_axis_data)
# 坐标点的标记方式 【实心圆：o，加号：+，五角星：*，点：.，叉叉：x，上三角形：^，下三角形：v，左三角形：<，右三角形：>，正方形：s，菱形：d，五边形：p，六边形：h，下划线：(_或者数字的0和1)】
# marker = ['o', '+', '*', 'x', '^', 'v', '<', '>', 's', 'd', 'p', 'h']
# marker = ['o']

for i in range(len(y_axis_data)):
    tem = y_axis_data.iloc[i]
    x_axis_data = list(tem.index)
    y_axis_datas = list(tem.values)
    # alpha设置线条透明度0-1之间，越小越透明；
    # linewidth设置线条粗细；
    plt.plot(x_axis_data, y_axis_datas, alpha=1, linewidth=2, label=''.join(sm_name.values[i]))
# 显示样式在图中，如1,2-methyl..
plt.legend()
plt.title("MTW(1000) MSD (773K)\n", fontsize=20)
plt.xlabel('Time (ns)', fontsize=20)
# 设置nm2上标$\mathregular{nm^2}$
plt.ylabel('MSD ($\mathregular{nm^2}$)', fontsize=20)
plt.show()

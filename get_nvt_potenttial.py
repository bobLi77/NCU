#!/home/essex/datas/bob/NCU/env/bin/python
# author:bob
# created time: 2024-01-23
# 功能:
# 1.用于提取nvt模拟后的势能


import os
import subprocess

def get_nvt_potential():
    potential_cmd = "gmx energy -f " + file_name + " -o nvt_potential.xvg 2>&1 | tee nvt_potential.log"
    p = subprocess.Popen(potential_cmd,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    p.communicate("11 0\n".encode())

def extract_potential():
    with open("nvt_potential.log","r",encoding="utf-8") as fr:
        last_rows = ' '.join(fr.readlines()[-1].split()).split(' ')[1]
        return last_rows

def extract_max_potential():
    xvg_cmd = "cat nvt_potential.xvg| grep -v -E '#|@' | awk '{print $2}' > temp.txt"
    subprocess.run(xvg_cmd, shell=True)
    with open("temp.txt",'r',encoding='utf-8') as f2:
        max_potential = f2.readlines()[0].split('.')[0].replace('\n','')
        # print(max_potential)
        return max_potential



if __name__ == '__main__':
    file_name = 'nvt_cmp_mix_200ns.edr'
    gmxdir = "~/Downloads/gromacs/gmx-gpu/bin/"  # gmx环境变量
    current_path = os.getcwd()
    fold_name = os.listdir(current_path)
    all_potential = ""
    # extract_max_potential()
    for fold in fold_name:
        # 判断fold是一个文件夹
        if not os.path.isdir(fold):
            pass
        else:
            # 进入到文件夹中
            os.chdir(fold)
            # 获取nvt_potential.log文件
            get_nvt_potential()
            # 获取到势能
            potential = extract_potential()
            max_potential = extract_max_potential()
            all_potential += fold + '\t' + max_potential + '\t' + potential + '\n'
            os.chdir(current_path)

    with open("all_potential.txt",'w',encoding='utf-8') as fw:
        fw.write(all_potential)
    fw.close()


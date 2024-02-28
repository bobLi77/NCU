#!/usr/bin/python

# author:bob
# created time: 2023-08-31
# function: use to get merge complex gro file


def process_grofile(molsie_gro, lig_gro, he_gro):
    # 分子筛
    with open(molsie_gro, 'r', encoding='utf-8') as ms:
        ms_content = ms.readlines()
        ms1 = ms_content[0]
        ms2 = ms_content[1]
        ms_mol = "".join(ms_content[2:-1])
        ms_last = ms_content[-1]
    ms.close()

    # 小分子
    with open(lig_gro, 'r', encoding='utf-8') as lig:
        lig_content = lig.readlines()
        lig2 = lig_content[1]
        lig_mol = "".join(lig_content[2:-1])
        lig_mol2lig = lig_mol.replace("MOL", "LIG")
    lig.close()

    # He walls
    with open(he_gro, 'r', encoding='utf-8') as he:
        he_content = he.readlines()
        he2 = he_content[1]
        he_mol = "".join(he_content[2:-1])
        he_mol2wal = he_mol.replace("MOL", "WAL")
    he.close()
    # 计算总原子数
    total_atom_num = int(ms2) + int(lig2) + int(he2)
    # 合并文件
    complex_gro = ms1 + str(total_atom_num) + "\n" + ms_mol +  lig_mol2lig +  he_mol2wal + ms_last
    return complex_gro


def write_cmp_mix_gro(complex_gro):
    with open("cmp_mix.gro", "w", encoding="utf-8") as cm:
        cm.write(complex_gro)
    cm.close()


if __name__ == "__main__":
    molsie_gro_name = input("请输入分子筛gro文件: ")
    lig_gro_name = input("请输入小分子gro文件: ")
    he_gro_name = input("请输入He walls的gro文件: ")
    com_mix_gro = process_grofile(molsie_gro_name, lig_gro_name, he_gro_name)
    write_cmp_mix_gro(com_mix_gro)

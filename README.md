1.cal_msd.py  #用于批量计算均方位移MSD，输出xvg格式文件作图（混合模型使用）；

2.cal_resp.py  #使用ORCA程序批量计算RESP电荷；

3.cif2pdb.py  #用于批量将cif格式文件转换成pdb格式文件；

4.construct_complex_system.py  #用于构建初始体系；

5.diffused_capacity.py  #用于计算轨迹的扩散量；

6.genrestr.py  #用于生成限制性文件；

7.get_msd_from_xvg.py  #用于批量提取xvg文件中的msd数据输出到excel；

8.get_nvt_potential.py  #用于提取nvt模拟后的势能数据

9.line_graph.py  #折线图绘制；

10.merge_complex.py  #用于合并复合物的gro文件；

11.msd.py  #计算小分子的msd数据并处理输出到excel；

12.npt_sm.py  #用于packmol构建后的能量优化和npt平衡；

13.nvtmd_cmpmix.py  #用于初始结构的能量优化和nvt模拟；

14.pdb2mol2.py  #用于批量处理pdb格式文件转换成mol2格式文件；

15.process_itp_atomtype.sh  #用于批量修复itp文件中键角原子类型等异常；

16.process_molsie.py  #用于处理分子筛文件，输出Gromacs程序可用文件；

17.rename_gro_mol2oth.py  #用于重命名gro结果文件中小分子类型，将其区分开来；

18.replace_resp.sh  #用于将计算好的RESP电荷和itp文件中的电荷进行替换；

19.reset_box.py  #重置盒子尺寸；

20.sobtop_get_itp_gro.py  #使用sobtop程序获取小分子的itp和gro格式文件；

21.translate.py  #平移复合物结构

22.trjconv_tric.py  #用于修正轨迹文件中正方体盒子到平行四边形；

23.validation_force_field.py  #用于验证力场的正确性；

24.xvg2excel.py  #用于提取xvg中msd数据，合并输出到excel中；

### 其他脚本及具体功能请查看注释

import time
import re
import sys
import numpy as np
from modules import ImageReconize,dataprocess,pdfReconize,log
from file_operate import file_operate
import win32com.client as win32
import os
#日志配置
log.setlog()
#报销需要输入的必要信息
reason='检查样机'
exportfolder=r'C:\Users\123456\PycharmProjects\报销自动化'#txt文档输出文件夹
importfolder=r'C:\Users\123456\PycharmProjects\报销自动化\pdf识别'#pdf和png存放文件夹
#地铁截图输出的文档信息路径
# filename='1.txt'
# if not ImageReconize.export_txtfile(r'C:\Users\123456\PycharmProjects\报销自动化\图片识别\Photo_1014_2a.png'
#         ,filename):
#     print(False)
#     sys.exit(0)
data1=[]
if  ImageReconize.export_img_to_txt(importfolder,exportfolder):
    filelist=file_operate.get_files_by_extension(exportfolder,'txt')
    for filepath in filelist:
        i=file_operate.split_path(filepath)[1].find("ditie")
        if i<0:
            continue
        tmp=dataprocess.ditie_data_process(filepath,reason)
        if not len(tmp):
            print(f'文件路径：{filepath}   无法获取报销信息')
            continue
        if not len(data1):
            data1=tmp
            continue
        data1=np.vstack((data1,tmp))
#pdf信息提取---------------------------------------------------
data2=[]
if  pdfReconize.export_pdf_to_txt(importfolder,exportfolder):
    filelist=file_operate.get_files_by_extension(exportfolder,'txt')
    for filepath in filelist:
        i = file_operate.split_path(filepath)[1].find("ditie")
        if i > 0:
            continue
        tmp=dataprocess.didi_data_process(filepath,reason)
        if not len(tmp):
            print(f'文件路径：{filepath}   无法获取报销信息')
            continue
        if not len(data2):
            data2=tmp
            continue
        data2=np.vstack((data2,tmp))
    #PDF与图片信息整合-----------------
data3=np.vstack((data1,data2))
print(data3)

#---------------------------excel操作---------------------------
SRT_ROW=11
END_ROW=11
excel=win32.gencache.EnsureDispatch('Excel.Application')
wb=excel.Workbooks.Open(r'C:\Users\123456\PycharmProjects\报销自动化\表格处理\交通费报销表昆山3.xlsx')
excel.Visible=True
ws=wb.Worksheets(1)
for data in data3:
    cell_range=f'B{SRT_ROW}:K{END_ROW}'
    print(cell_range)
    print(data)
    ws.Range(cell_range).Value=tuple(data)
    SRT_ROW+=1
    END_ROW+=1
wb.SaveAs(r'.\6.xlsx')
excel.Application.Quit()
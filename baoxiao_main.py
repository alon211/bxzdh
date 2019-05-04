#删除临时文件
import  tempfile,os
t=tempfile.gettempdir()
dir=os.path.join(t,'gen_py')
if os.path.exists(dir):
    os.remove(dir)
import time
import re
import sys
import numpy as np
from modules import ImageReconize,dataprocess,pdfReconize,log
from file_operate import file_operate
import win32com.client as win32
from modules import mailprocess
import datetime

import os
#日志配置
log.setlog()
# 固定配置
exportfolder=r'C:\Users\123456\PycharmProjects\报销自动化\邮箱下载报销文件存放位置'#txt文档输出文件夹
importfolder=r'C:\Users\123456\PycharmProjects\报销自动化\邮箱下载报销文件存放位置'#pdf和png存放文件夹
maildownloadfolder=r'C:\Users\123456\PycharmProjects\报销自动化\邮箱下载报销文件存放位置'
#报销需要输入的必要信息
reason='SAK单机版功能验收'
maildownload_starttime='2019-02-11' #搜索邮件的起始日期
maildownload_endtime='2019-02-11' #搜索邮件的终止日期
ditie_starttime='02-10' #地铁票报销的时间段,格式一定要按照这个格式
ditie_endtime='02-11'#地铁票报销的时间段,格式一定要按照这个格式
didi_starttime='01-28'
didi_endtime='02-01'


#检查参数是否填写正确
try:
    ditie_startdate=datetime.datetime.strptime(ditie_starttime, '%m-%d')
    ditie_enddate =datetime.datetime.strptime(ditie_endtime, '%m-%d')
    maildownload_startdate=datetime.datetime.strptime(maildownload_starttime, '%Y-%m-%d')
    maildownload_enddate=datetime.datetime.strptime(maildownload_endtime, '%Y-%m-%d')
    if ditie_enddate < ditie_startdate or maildownload_enddate < maildownload_startdate:
        print('起始日期不能大于终止日期')
        sys.exit(0)
except:
    print("ditie_starttime或ditie_endtime或maildownload_endtime或maildownload_starttime格式错误")

#清空以前下载内容
for file in os.listdir(maildownloadfolder):
    os.remove(os.path.join(maildownloadfolder,file))
# for folder in exportfolder,importfolder,maildownloadfolder:
#     '' if os.path.exists(folder) else os.mkdir(folder)
# # 将滴滴附件和地铁附件件从邮箱下载到文件夹内
mailprocess.get_baoxiao_info(maildownload_starttime,maildownload_endtime,maildownloadfolder)

#地铁截图输出的文档信息路径
dite_data=[]
filelist=[]
if  ImageReconize.export_ditie_img_to_txt(importfolder, exportfolder):
    filelist=file_operate.get_files_by_extension(exportfolder,'txt')
    for filepath in filelist:
        i=file_operate.split_path(filepath)[1].find("ditie")
        if i<0:
            continue
        tmp=dataprocess.ditie_data_process(filepath,reason,ditie_starttime,ditie_endtime)
        if not len(tmp):
            print(f'文件路径：{filepath}   无法获取报销信息')
            continue
        if not len(dite_data):
            dite_data=tmp
            continue
        dite_data=np.vstack((dite_data,tmp))
#pdf信息提取---------------------------------------------------
didi_data=[]

if  pdfReconize.export_pdf_to_txt(importfolder,exportfolder):
    filelist=file_operate.get_files_by_extension(exportfolder,'txt')
    for filepath in filelist:
        i = file_operate.split_path(filepath)[1].find("滴滴")
        if i < 0:
            continue
        tmp=dataprocess.didi_data_process(filepath,reason,didi_starttime,didi_endtime)
        if not len(tmp):
            print(f'文件路径：{filepath}   无法获取报销信息')
            continue
        if not len(didi_data):
            didi_data=tmp
            continue
        didi_data=np.vstack((didi_data,tmp))
#高铁信息提取----------------------
railway_data = []
for filepath in filelist:
    i=file_operate.split_path(filepath)[1].find('railway')
    if i<0:
        continue
    tmp=dataprocess.railway_data_process(filepath,reason)
    if not len(tmp):
        print(f'文件路径：{filepath}无法获取高铁信息')
        continue
    if not len(railway_data):
        railway_data=tmp
        continue
    railway_data=np.vstack((railway_data,tmp))
 #PDF与图片信息整合-----------------
finall_data=[]
for item in didi_data:
    finall_data.append(item)
for item in dite_data:
    finall_data.append(item)
for item in railway_data:
    finall_data.append(item)

# if didi_data==[] and not dite_data==[]:
#     finall_data=dite_data
# elif dite_data==[] and not didi_data==[]:
#     finall_data=didi_data
# elif dite_data==[] and didi_data==[]:
#     finall_data=[]
# else:
#     finall_data=np.vstack((dite_data,didi_data))
print(finall_data)

#---------------------------excel操作---------------------------
SRT_ROW=11
END_ROW=11
excel=win32.gencache.EnsureDispatch('ket.Application')
wb=excel.Workbooks.Open(r'C:\Users\123456\PycharmProjects\报销自动化\表格处理\交通费报销表昆山3.xlsx')
excel.Visible=True
ws=wb.Worksheets(1)
for data in finall_data:
    cell_range=f'B{SRT_ROW}:K{END_ROW}'
    print(cell_range)
    print(data)
    ws.Range(cell_range).Value=tuple(data)
    SRT_ROW+=1
    END_ROW+=1
wb.SaveAs(r'.\6.xlsx')
excel.Application.Quit()
ws.Cells()
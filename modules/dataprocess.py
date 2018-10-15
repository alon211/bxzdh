import time
import re
import logging
import numpy as np
def ditie_data_process(filename,reason):
    """
    该方法仅针对metro APP中账单明细的截图有用
    :param filename: 图片识别后生成的txt文档路径
    :return: 返回按照报销表格需要的信息格式数据,如果没有返回空数组，如果有返回[[...]]
    """


    data = []
    #-------------------获取图片解析出的txt文档-------------------------
    with open(filename,
              'rt',encoding='utf-8') as f:
        txt=f.read()
        f.close()
    if txt is None:
        return data
    #--------------------信息预处理---------------------------------
    f=txt.replace(' ','')
    f=f.replace('\n','')
    #--------------------将数据整理后放入data中---------------------------------

    while True:
        #从文件末尾开始搜索
        i=f.rfind('出站')
        if i <0:
            break
        #花费的钱
        cost=f[i+3:i+7]
        #检查获取的钱格式是否正确
        k=re.match(r"\d\.\d{2}",cost)
        if not k:
            print(cost)
            print("数据错误，无法找到地铁花费的钱")
            logging.warning(f'钱格式错误，cost:{cost}')
            break

        #检查是否能获取到坐车时间
        if i-10<0:
            print("数据错误，无法找到坐车时间")
            logging.warning(f'坐车时间错误')

            break
        try:
            timedata=f[i-10:i-5]
            time.strptime(timedata,'%M-%d')
        except:
            print("地铁乘车时间不匹配，格式为'%M-%d'")
            logging.warning("地铁乘车时间不匹配，格式为'%M-%d'")

            break
        #字符串重新截取，删除已经获取的内容的字符串
        f=f[:i-10]
        #搜索起始地点和终点
        i=f.rfind('-')
        if i<0:
            print('无法找到坐车上下站地铁当中的横杠')
            logging.warning("无法找到坐车上下站地铁当中的横杠")

            break
        endplace=f[i+1:]

        #字符串重新截取，删除已经获取的内容的字符串
        f=f[:i]
        #获取起始地点的开头索引号
        i=f.rfind("交易成功")
        if i<0:
            i=f.rfind("明细")
            if i >0:
                i=i+2
        else:
            i=i+4
        if i<0:
            print("地铁信息搜索完毕")


        startpalce=f[i:]

        data.append([timedata,startpalce,endplace,'地铁',reason,'','','','',cost])
    # f=f[:i]
    # i=f.rfind('\n')
    return data
def didi_data_process(filename,reason):
    """
      获取每个pdf上的报销信息
      :param filespath: 文件路径
      :param reason: 出差原因
      :return: 返回按照报销表格需要的信息格式数据,如果没有返回空数组，如果有返回[[...]]
      """
    inf = []
    import os
    if not os.path.isfile(filename):
        logging.warning("不存在此文件")
        return inf
    with open(filename, 'rt', encoding='utf-8') as f:
        txt = f.read()
        f.close()
    if txt is None:
        return []

    srt = txt.find('快车')
    if srt < 0:
        return []
    while True:
        if srt < 0:
            break
        end = txt.find('\n', srt)
        if end < 0:
            print(txt[srt:])
            break
        data = txt[srt:end].split(" ")
        if len(data) != 9:
            break
        data = [data[1], data[5], data[6], "出租车", reason, "", "", "", "", data[8]]
        inf.append(data)
        srt = txt.find("快车", end)
    return inf

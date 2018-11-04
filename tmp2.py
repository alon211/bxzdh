from bs4 import BeautifulSoup
from bs4 import NavigableString
import os
from modules import mailprocess,dataprocess
import time

# l=mailprocess.get_msg('20181018','20181018')
# for e in l:
#    content=mailprocess.print_info(e)
# if os.path.exists('tmp.txt'):
#    txt = ''
#    with open("tmp.txt", 'rt',encoding='gb18030') as f:
#
#       tmp = f.read()
#       soup = BeautifulSoup(tmp,features="html.parser")
#       for tag in soup.find_all('div'):
#          if tag.string is None:
#             continue
#          txt += tag.string
#       f.close()
#    print(txt)
#    index = txt.find('张史龙')
#    txt = txt[index:]
#    index = txt.find("。")
#    txt = txt[:index]
#    data = txt.split('，')
#    print(data)
# print(content)



# txt=''
# if os.path.exists('tmp.txt'):
#    with open("tmp.txt", 'rt') as f:
#       tmp = f.read()
#       soup = BeautifulSoup(tmp)
#       for tag in soup.find_all('div'):
#          if tag.string is None:
#             continue
#          txt += tag.string
#       f.close()
#    index=txt.find('张史龙')
#    txt=txt[index:]
#    index=txt.find("。")
#    txt=txt[:index]
#    txtlist=txt.split('，')
#    print(txtlist)
txt=''
data = dataprocess.railway_data_process(r'C:\Users\123456\PycharmProjects\报销自动化\邮箱下载报销文件存放位置\railway_2018-11-04.txt','检查样机')
print(data)




# data=[]
# txt=['张史龙', '2018年10月18日12:39开', '无锡东-上海虹桥', 'G105次列车,01车08D号', '一等座', '票价84.5元', '检票口：A2']
# tmp=txt[2].split('-')
# startpalce=tmp[0]
# endplace=tmp[1]
# Date=txt[1][:11]
# traffic_type='火车'
# reason='1'
# money=txt[5][2:-1]
# data.append([Date, startpalce, endplace, traffic_type, reason, '', '', '', '', money])
# print(data)
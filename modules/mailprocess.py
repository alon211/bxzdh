
# -*- coding=utf-8 -*-
import poplib
import msvcrt
from bs4 import BeautifulSoup
import os
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText
import datetime
def input_password(msg=''):
    import msvcrt

    if msg!='':
        print(msg)

    li = []

    while 1:

        ch = msvcrt.getch()

        # 回车

        if ch == b'\r':

            msvcrt.putch(b'\n')

            # print('输入的密码是：%s' % b''.join(li).decode())

            return b''.join(li).decode()

        # 退格

        elif ch == b'\x08':

            if li:
                li.pop()

                msvcrt.putch(b'\b')

                msvcrt.putch(b' ')

                msvcrt.putch(b'\b')

        # Esc

        elif ch == b'\x1b':

            break

        else:

            li.append(ch)

            msvcrt.putch(b'*')

    # os.system('pause')
# indent用于缩进显示:

def print_info(msg, indent=0,export_path=r'./'):
    """
    获取邮件内容
    :param msg: 解析邮件返回的对象Parser().parsestr(msg_content)
    :param indent: 缩进
    :param export_path:如果是html格式的文档会在该路径下生成一个tmp.txt文件存储信息
    :return: info 如果邮件内容是纯文本格式，直接返回，如果是html格式的话，需要将info+tmp.txt(需要用beautisoup4提取有用的信息）
    合并才是所有内容
    """
    info=" "
    html_info=''
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))
            info=info+f"{('  ' * indent)}{header}:{value}'"+'\n'
    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            info=info+f"{('  ' * indent)}part {n}"+'\n'
            info=info+f"{('  ' * indent)}--------------------"+'\n'
            # print('%spart %s' % ('  ' * indent, n))
            # print('%s--------------------' % ('  ' * indent))
            # 递归打印每一个子对象:
            info+=print_info(part, indent + 1)
    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type=='text/plain':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)


            # 要检测文本编码:
            charset = __guess_charset(msg)

            try:
                content = content.decode(charset)
                # print('%sText: %s' % ('  ' * indent, content + '...'))
            except:
                content=content.decode("gb18030")
            info=info+f"{('  ' * indent)}Text: {(content + '...')}"+'\n'
            # print(info)
            #             # with open("tmp.txt",'wt') as f:
            #             #     f.write(content)
            #             #     f.close()
        elif content_type == 'text/html':
            content = msg.get_payload(decode=True)

            # 要检测文本编码:
            charset = __guess_charset(msg)

            try:
                content = content.decode(charset)
                # print('%sText: %s' % ('  ' * indent, content + '...'))
            except:
                content = content.decode("gb18030")
            html_info = f"{('  ' * indent)}Text: {(content + '...')}" + '\n'
            with open(os.path.join(export_path,r"tmp.txt"),'wt',encoding='gb18030') as f:
                f.write(html_info)
                f.close()
        else:
            # 不是文本,作为附件处理:
            # print('%sAttachment: %s' % ('  ' * indent, content_type))
            info=info+f"{('  ' * indent)}Attachment: {content_type}"+'\n'
    return info
# def print_info(msg, indent=0):
#     """
#     获取邮件内容
#     :param msg: 解析邮件返回的对象Parser().parsestr(msg_content)
#     :param indent: 缩进
#     :return: info 邮件内容string
#     """
#     info=" "
#     if indent == 0:
#         # 邮件的From, To, Subject存在于根对象上:
#         for header in ['From', 'To', 'Subject']:
#             value = msg.get(header, '')
#             if value:
#                 if header=='Subject':
#                     # 需要解码Subject字符串:
#                     value = decode_str(value)
#                 else:
#                     # 需要解码Email地址:
#                     hdr, addr = parseaddr(value)
#                     name = decode_str(hdr)
#                     value = u'%s <%s>' % (name, addr)
#             # print('%s%s: %s' % ('  ' * indent, header, value))
#             info=info+f"{('  ' * indent)}{header}:{value}'"+'\n'
#     if (msg.is_multipart()):
#         # 如果邮件对象是一个MIMEMultipart,
#         # get_payload()返回list，包含所有的子对象:
#         parts = msg.get_payload()
#         for n, part in enumerate(parts):
#             info=info+f"{('  ' * indent)}part {n}"+'\n'
#             info=info+f"{('  ' * indent)}--------------------"+'\n'
#             # print('%spart %s' % ('  ' * indent, n))
#             # print('%s--------------------' % ('  ' * indent))
#             # 递归打印每一个子对象:
#             info+=print_info(part, indent + 1)
#     else:
#         # 邮件对象不是一个MIMEMultipart,
#         # 就根据content_type判断:
#         content_type = msg.get_content_type()
#         print(content_type)
#         if content_type=='text/plain' or content_type=='text/html':
#             # 纯文本或HTML内容:
#             content = msg.get_payload(decode=True)
#
#
#             # 要检测文本编码:
#             charset = __guess_charset(msg)
#
#             try:
#                 content = content.decode(charset)
#                 # print('%sText: %s' % ('  ' * indent, content + '...'))
#             except:
#                 content=content.decode("gb18030")
#             info=info+f"{('  ' * indent)}Text: {(content + '...')}"+'\n'
#             # print(info)
#             #             # with open("tmp.txt",'wt') as f:
#             #             #     f.write(content)
#             #             #     f.close()
#         else:
#             # 不是文本,作为附件处理:
#             # print('%sAttachment: %s' % ('  ' * indent, content_type))
#             info=info+f"{('  ' * indent)}Attachment: {content_type}"+'\n'
#     return info
def __guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def __get_attr(msg,filepath,attfile_name=''):
    """

    :param msg: 析邮件返回的对象Parser().parsestr(msg_content)
    :param mailsubject: 搜索的邮件标题
    :param filepath: 保存路径
    :param attfile_name: 空代表所有附件都下载，如果非空代表下载指定文件
    :return: 返回附件名字
    """
    import email
    import os
    import time
    attachment_files=[]
    for part in msg.walk():
        file_name=part.get_filename()#获取附件名称类型
        contType = part.get_content_type()
        if file_name:
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)  # 对附件名称进行解码
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))  # 将附件名称可读化
                if attfile_name!='':
                    i=filename.find(attfile_name)
                    if i<0:
                        continue
                # filename = filename.encode("utf-8")
            data = part.get_payload(decode=True)  # 下载附件
            date=time.strftime('%Y%m%d%M%S',time.localtime(time.time()))
            att_file = open( os.path.join(filepath,date+filename), 'wb')  # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            attachment_files.append(filename)
            att_file.write(data)  # 保存附件
            att_file.close()
    return attachment_files

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def get_msg(start='19900101',end='20181013'):
    '''
    搜索起始日期到终止日期内的邮件，返回其msg对象数组
    :param start: 搜索的起始日期
    :param end: 搜索的终止日期
    :return: 返回Msg对象列表
    '''
    # 输入邮件地址, 口令和POP3服务器地址:
    # email = input('Email_username: ')
    # password = input('Password: ')
    # pop3_server = input('POP3 server: ')
    email, password, pop3_server, msg_inf = '', '', '', ''
    msg_list=[]
    # 邮箱账户读取位置
    with open(r'C:\Users\123456\Documents\MttQ\1.txt', 'rt', encoding='utf-8') as file:
        msg_inf = file.read().split('\n')
        file.close()
    if email == '':
        email = msg_inf[0]
    if pop3_server == '':
        pop3_server = 'pop.qq.com'
    print(email, password, pop3_server)

    # 连接到POP3服务器:
    server = poplib.POP3_SSL(pop3_server, 995)
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome())
    # 身份认证:
    server.set_debuglevel(1)
    server.user(email)
    server.pass_(msg_inf[1])  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似['1 82923', '2 2184', ...]
    print(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    for mail_item in range(index, 0, -1):
        resp, lines, octets = server.retr(mail_item)
        # # lines存储了邮件的原始文本的每一行,
        # # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('gb18030', errors='ignore')
        # # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        # 获取邮件时间
        tmp = msg.get("Date")
        tmp = tmp.split(" ")
        date1 = ""
        if len(tmp) == 5:
            if "" in tmp:
                tmp.remove("")
                tmp = " ".join(tmp[:4])
                date1 = time.strptime(tmp, "%a, %d %b %Y")
                break
            tmp = " ".join(tmp[:4])
            date1 = time.strptime(tmp, "%d %b %Y %H:%M:%S")
        elif len(tmp) == 8:
            if "" in tmp:
                tmp.remove("")
            tmp = " ".join(tmp[:5])
            date1 = time.strptime(tmp, '%a, %d %b %Y %H:%M:%S')
        else:
            tmp = " ".join(tmp[:5])
            date1 = time.strptime(tmp, '%a, %d %b %Y %H:%M:%S')
        if date1 == "":
            print(tmp)
        # date1 = time.strptime(msg.get("Date")[0:24],'%a, %d %b %Y %H:%M:%S') #格式化收件时间
        date2 = time.strftime("%Y%m%d", date1)  # 邮件时间格式转换
        # ------------------可能有问题--------------------------
        if (date2 < start): break
        # --------------------------------------------------------

        if (date2 > end or date2 < start):
            continue
        msg_list.append(msg)

    return msg_list


def get_baoxiao_info(str="19900101",end="20181013",filepath="."):
    # 需要获取的滴滴邮件附件的时间段
    """
      获取滴滴和地铁截图的附件，筛选条件为标题为滴滴出行或者地铁
    :param str: 起始日期
    :param end: 结束日期
    :param FilePath: 附件保持路径
    :return: 如果有，在路径内保存附件或者铁路文本信息，并且返回true，如果无则返回false


    """
    # 输入邮件地址, 口令和POP3服务器地址:
    # email = input('Email_username: ')
    # password = input('Password: ')
    # pop3_server = input('POP3 server: ')
    email, password, pop3_server, msg_inf = '', '', '', ''
    rst=False
    #邮箱账户读取位置
    with open(r'C:\Users\123456\Documents\MttQ\1.txt', 'rt', encoding='utf-8') as file:
        msg_inf = file.read().split('\n')
        file.close()
    if email == '':
        email = msg_inf[0]
    if pop3_server == '':
        pop3_server = 'pop.qq.com'
    print(email, password, pop3_server)

    # 连接到POP3服务器:
    server = poplib.POP3_SSL(pop3_server, 995)
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome())
    # 身份认证:
    server.set_debuglevel(1)
    server.user(email)
    server.pass_(msg_inf[1])  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似['1 82923', '2 2184', ...]
    print(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    for mail_item in range(index, 0, -1):
        resp, lines, octets = server.retr(mail_item)
        # # lines存储了邮件的原始文本的每一行,
        # # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('gb18030', errors='ignore')
        # # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        # 获取邮件时间
        tmp = msg.get("Date")
        tmp = tmp.split(" ")
        date1 = ""
        if len(tmp) == 5:
            if "" in tmp:
                tmp.remove("")
                tmp = " ".join(tmp[:4])
                date1 = time.strptime(tmp, "%a, %d %b %Y")
                break
            tmp = " ".join(tmp[:4])
            date1 = time.strptime(tmp, "%d %b %Y %H:%M:%S")
        elif len(tmp) == 8:
            if "" in tmp:
                tmp.remove("")
            tmp = " ".join(tmp[:5])
            date1 = time.strptime(tmp, '%a, %d %b %Y %H:%M:%S')
        else:
            tmp = " ".join(tmp[:5])
            date1 = time.strptime(tmp, '%a, %d %b %Y %H:%M:%S')
        if date1 == "":
            print(tmp)
        # date1 = time.strptime(msg.get("Date")[0:24],'%a, %d %b %Y %H:%M:%S') #格式化收件时间
        date2 = time.strftime("%Y-%m-%d", date1)  # 邮件时间格式转换
        # ------------------可能有问题--------------------------
        if (date2<str):break
        # --------------------------------------------------------

        if (date2 >end or date2 < str):
            continue
        txt = print_info(msg)
        i = txt.find('Subject:滴滴出行电子发票')
        ditie=False
        if i<0:
            i = txt.find('Subject:地铁')
            ditie=True
        c=txt.find('Subject:网上购票系统--用户支付通知')
        print(f"c:{c}")
        if c>0:
            if os.path.exists('tmp.txt'):
                print("tmp文件存在")
                txt = ''
                with open("tmp.txt", 'rt', encoding='gb18030') as f:

                    tmp = f.read()
                    soup = BeautifulSoup(tmp, features="html.parser")
                    for tag in soup.find_all('div'):
                        if tag.string is None:
                            continue
                        txt += tag.string
                    f.close()
                index = txt.find('张史龙')
                txt = txt[index:]
                index = txt.find("。")
                txt = txt[:index]
                # data = txt.split('，')
                with open(os.path.join(filepath,f"railway_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"),'wt') as f:
                    f.write(txt)
                    f.close()
                os.remove("tmp.txt")
                rst=True

        if i >= 0:
            print(date2)
            print(f"mail_item:{mail_item}  {i}:{True}")
            __get_attr(msg, filepath) if ditie else __get_attr(msg,filepath,"滴滴出行行程报销单")
            rst=True

        # get_attr(msg)
        # # 可以根据邮件索引号直接从服务器删除邮件:
        # # server.dele(index)
    # 关闭连接
    server.quit()
    return rst


from PIL import Image
import sys
import pyocr.builders
import pyocr.tesseract
import logging
import traceback
import os
from file_operate import file_operate
def export_txtfile(img,txtname,lang='chi_sim+chi_sim2'):
    """
    将图片中的中文文字识别后保存txt文档
    :param img: 图片路径
    :param txtname:输出的txt文档名字可以是绝对路径
    :parameter lang:学习库的文件名字
    :return: 如果成功返回true失败则返回false
    """
    # CHANGE THIS IF TESSERACT IS NOT IN YOUR PATH, OR IS NAMED DIFFERENTLY
    pyocr.tesseract.TESSERACT_CMD='C://Program Files (x86)//Tesseract-OCR//tesseract.exe'
    print(pyocr.tesseract.get_version())#版本错误会报--psm有问题
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        return False
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    # 需要使用的学习库和文件
    lang=lang

    # ########################

    txt = tool.image_to_string(
        Image.open(img),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )

    # with open(f'text_{lang}_{filename}.txt','wt',encoding='UTF-8') as file:
    with open(txtname,'wt',encoding='UTF-8') as file:

        if type(txt) == str:
            file.write(txt)
        else:
            #  对于builder=pyocr.builders.lineboxbuilder()和wordboxbuilder使用
            for line in txt:
                file.write(line.content)
        file.close()
        return True
def export_ditie_img_to_txt(import_path, export_path='.'):
    """
    扫描该路径将所有地铁png图片转为txt
    :param import_path: 扫描的文件夹路径
    :param export_path:输出的文件夹路径
    :return: 如果成功，为True，如果失败为False
    """


    rst=False
    # pdf识别路径
    img_files= file_operate.get_files_by_extension(import_path,extension_name='png')
    if img_files ==[]:
        print("文件夹没有文img文件")
        logging.warning('文件夹没有img文件')
        return False
    for img in img_files:
        try:
            txtname=os.path.join(export_path,f'{file_operate.split_path(img)[1]}ditie.txt')
            export_txtfile(img,txtname)
            rst=True
        except Exception as e:
            print(e)
            traceback.print_exc(file=open('log.txt','w+',encoding='utf-8'))
    return rst
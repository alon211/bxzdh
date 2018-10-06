import sys
sys.path.append(r'C:\Users\123456\PycharmProjects\usermodules')
from file_operate import file_operate
from MyException import MyException
from MyException.MyException import FILE_ERROR_INFOR
import fitz
import os
import traceback
print(fitz.__doc__)
print(fitz.version)
# pdf识别路径
pdf_file= file_operate.get_files_by_extension(extension_name='pdf')

def pdf2text(file_path,output_path='.'):
    """

    :param filename: 文件路径
    :return: filename.txt
    """
    if not file_operate.exist_file(file_path):
        raise MyException.FileErrorException(FILE_ERROR_INFOR['FILE_NOT_FOUNT'])
    if not file_operate.check_extension(file_path):
        raise MyException.FileErrorException(FILE_ERROR_INFOR['FILE_EXTESION_ERROR'])
    pdf_file =fitz.open(file_path)

    page1=pdf_file[0]
    text=page1.getText('text')
    try:
        with open(os.path.join(output_path,f'{file_operate.split_path(file_path)[1]}.txt'),'wt',encoding='UTF-8') as file:
            file.write(text)
            file.close()
            pdf_file.close()
    except Exception as e:
        print(e)
        pdf_file.close()
for pdf in pdf_file:
    try:
        pdf2text(pdf)
    except:
        traceback.print_exc(file=open('log.txt','w+',encoding='utf-8'))

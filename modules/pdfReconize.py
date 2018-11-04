from MyException import MyException
from MyException.MyException import FILE_ERROR_INFOR
import fitz
import os
import traceback
from file_operate import file_operate
import logging
# print(fitz.__doc__)
# print(fitz.version)
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
        traceback.print_exc(file=open('log.txt', 'w+', encoding='utf-8'))
        pdf_file.close()
def export_pdf_to_txt(import_path,export_path='.'):
    """
    扫描该路径将所有pdf文件转为txt
    :param import_path: 扫描的文件夹路径
    :param export_path:输出的文件夹路径
    :return: 如果成功，为True，如果失败为False
    """


    rst=False
    # pdf识别路径
    pdf_files= file_operate.get_files_by_extension(import_path,extension_name='pdf')
    if pdf_files ==[]:
        print("文件夹没有文pdf件")
        logging.warning('文件夹没有pdf文件')
        return False
    for pdf in pdf_files:
        try:
            pdf2text(pdf,export_path)
            rst=True
        except Exception as e:
            print(e)
            traceback.print_exc(file=open('log.txt','w+',encoding='utf-8'))
    return rst
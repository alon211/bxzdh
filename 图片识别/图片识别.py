from PIL import Image
import sys
import pyocr.builders
import pyocr.tesseract
import cv2
import os
import argparse
import numpy as np
# 最好图片是白底黑字，识别更加，如果不是先用opencv做处理
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image=cv2.imdecode(np.fromfile(args['image'],dtype=np.uint8),-1)
gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
print(filename)
cv2.imwrite(filename, gray)

# CHANGE THIS IF TESSERACT IS NOT IN YOUR PATH, OR IS NAMED DIFFERENTLY
pyocr.tesseract.TESSERACT_CMD='C://Program Files (x86)//Tesseract-OCR//tesseract.exe'
print(pyocr.tesseract.get_version())#版本错误会报--psm有问题
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

# 需要使用的学习库和文件
lang='chi_sim+chi_sim2'
filename='1.png'
# ########################

txt = tool.image_to_string(
    Image.open(filename),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)

with open(f'text_{lang}_{filename}.txt','wt',encoding='UTF-8') as file:
    if type(txt) == str:
        file.write(txt)
    else:
        #  对于builder=pyocr.builders.lineboxbuilder()和wordboxbuilder使用
        for line in txt:
            file.write(line.content)
    file.close()

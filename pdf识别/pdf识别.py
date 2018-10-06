import fitz

print(fitz.__doc__)
print(fitz.version)
# pdf识别路径
pdf=fitz.open(r'C:\Users\123456\PycharmProjects\报销自动化\pdf识别\2.pdf')
page1=pdf[0]
text=page1.getText('text')
try:
    with open('./1,txt','wt',encoding='UTF-8') as file:
        file.write(text)
        file.close()
        pdf.close()
except Exception as e:
    print(e)
    pdf.close()
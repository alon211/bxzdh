@echo off

c:

cd C:\Users\123456\Anaconda3\Scripts
CALL activate.bat baoxiaozidhua
python C:\Users\123456\PycharmProjects\报销自动化\邮箱获取滴滴出行单子\recieve_mail.py
CALL deactivate.bat

pause




import datetime
import os
import smtplib
import sys
import numpy as np


# print('{:0>3d}'.format(111))

# a = np.arange(24)
# # print (a.ndim)
# datetime.datetime.now().minute


# print (sys.path)

# smtplib.SMTP_SSL("smtp.qq.com", 465)

def is_weekend():
    """
    :return: if weekend return False else return True
    """
    now_time = datetime.datetime.now().strftime("%w")
    if now_time == "6" or now_time == "0":
        return False
    else:
        return True


file_list = []
for root, dirs, files in os.walk('video'):  # 生成器
    for fn in files:
        p = str(root + '/' + fn)
        file_list.append(p)

file_path = 'video/fnew.ts'
with open(file_path, 'wb+') as fw:
    for i in range(len(file_list)):
        fw.write(open(file_list[i], 'rb').read())

print(file_list)

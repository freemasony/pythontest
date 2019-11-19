import datetime
import smtplib
import sys
import numpy as np

a = np.arange(24)
#print (a.ndim)
datetime.datetime.now().minute
#print (sys.path)

#smtplib.SMTP_SSL("smtp.qq.com", 465)

def is_weekend():
    """
    :return: if weekend return False else return True
    """
    now_time = datetime.datetime.now().strftime("%w")
    if now_time == "6" or now_time == "0":
        return False
    else:
        return True

print (is_weekend())
# -*- coding: utf-8 -*-
import subprocess
import time
import sched
import datetime
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import configparser


config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg")
scheduler = sched.scheduler(time.time,time.sleep)
go_hour = int(config.get("time","go_hour"))
back_hour = int(config.get("time","back_hour"))
send_email_hour = int(config.get("time","send_email_hour"))
send_email_minute = int(config.get("time","send_email_minute"))
directory = config.get("ADB","directory")
sender = config.get("email","sender")
psw = config.get("email","psw")
receive = config.get("email","receive")
screen_dir = config.get("screen","screen_dir")

count = 0

# 打开钉钉，关闭钉钉封装为一个妆饰器函数
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        print("打开钉钉")
        operation_list = [self.adbpower, self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(10)
        print("open dingding success")
        print("打开打卡界面")
        operation_list1 = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
            time.sleep(5)
        time.sleep(10)
        print("open playcard success")
        # 包装函数
        func(self, *args, **kwargs)
        print("关闭钉钉")
    return wrapper


class dingding:

    # 初始化，设置adb目录
    def __init__(self,directory):
        self.directory = directory
        # 点亮屏幕
        self.adbpower = '"%s\\adb" shell input keyevent 26' % directory
        # 启动钉钉应用
        self.adbopen_dingding = '"%s\\adb" shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1' %directory
        # 启动mydemo应用
        self.adbopen_mydemo = '"%s\\adb" shell monkey -p com.nsa.mydemo -c android.intent.category.LAUNCHER 1' %directory
        # 点击工作
        self.adbselect_work = '"%s\\adb" shell input tap %s' % (directory,config.get("position","work_position"))
        # 点击考勤打卡
        self.adbselect_playcard = '"%s\\adb" shell input tap %s' % (directory,config.get("position","check_position"))
        # 设备截屏保存到sdcard
        self.adbscreencap = '"%s\\adb" shell screencap -p sdcard/screen.png' % directory
        # 传送到计算机
        self.adbpull = '"%s\\adb" pull sdcard/screen.png %s' % (directory,screen_dir)
        # 删除设备截屏
        self.adbrm_screencap = '"%s\\adb" shell rm -r sdcard/screen.png' % directory

    # 点亮屏幕 》》解锁 》》打开钉钉
    def open_mydemo(self):
        operation_list = [self.adbopen_mydemo]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(3)
        print("open mydemo success")


    # 上班(极速打卡)
    @with_open_close_dingding
    def goto_work(self,minute):
        self.screencap()
        self.sendEmail(minute)
        print("打卡成功")


    def send_email(self,minute):
        self.sendEmail(minute)
        print("发送邮件成功")


    # 截屏>> 发送到电脑 >> 删除手机中保存的截屏
    def screencap(self):
        operation_list = [self.adbscreencap,self.adbpull,self.adbrm_screencap]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("screencap to computer success")

    # 发送邮件（QQ邮箱）
    def sendEmail(self,minute):
        """
        qq邮箱 需要先登录网页版，开启SMTP服务。获取授权码，
        :return:
        """
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = MIMEMultipart('related')
        subject = now_time + '打卡'+'下次打卡随机分钟：'+str(minute)
        message['Subject'] = subject
        message['From'] = "日常打卡"
        message['To'] = receive
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')
        message.attach(content)
        file = open(screen_dir, "rb")
        img_data = file.read()
        file.close()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        message.attach(img)
        try:
            server = smtplib.SMTP_SSL("smtp.163.com", 465)
            server.login(sender, psw)
            server.sendmail(sender, receive, message.as_string())
            server.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)


    def sendEmailTest(self,minute):
        """
        qq邮箱 需要先登录网页版，开启SMTP服务。获取授权码，
        :return:
        """
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = MIMEMultipart('related')
        subject = now_time + '打卡'+'下次打卡随机分钟：'+str(minute)
        message['Subject'] = subject
        message['From'] = "日常打卡"
        message['To'] = receive
        content = MIMEText('<html><body><span>测试打卡成功</span></body></html>', 'html', 'utf-8')
        message.attach(content)
        try:
            server = smtplib.SMTP_SSL("smtp.163.com", 465)
            server.login(sender, psw)
            server.sendmail(sender, receive, message.as_string())
            server.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)


# 随机打卡时间段
def random_minute():
    return random.randint(30,50)

# 包装循环函数，传入随机打卡时间点
def incode_loop(func,minute):
    """
    包装start_loop任务调度函数，主要是为了传入随机分钟数。保证在不打卡的情况下能保持分钟数不变。
    :param func: star_loop
    :param minute: 随机分钟数
    :return: None
    """
    print (go_hour)
    print (back_hour)
    # 判断时间当超过上班时间则打下班卡。否则则打上班卡。
    if datetime.datetime.now().hour ==go_hour and datetime.datetime.now().minute >=back_hour and datetime.datetime.now().minute <=58:
        # 用来分类上班和下班。作为参数传入任务调度
        hourtype = 1
        print("下次将在", str(back_hour), ":", str(minute), "打卡")
    elif datetime.datetime.now().hour ==send_email_hour and datetime.datetime.now().minute >=send_email_minute and datetime.datetime.now().minute <=45:
        # 用来分类上班和下班。作为参数传入任务调度
        hourtype = 2
        print("下次将在", str(back_hour), ":", str(minute), "打卡")
    else:
        hourtype = 3
        print("下次将在", str(go_hour), ":", str(minute), "打卡")
    #执行任务调度函数
    func(hourtype,minute)


# 任务调度
def start_loop(hourtype,minute):
    """
    每次循环完成，携带生成的随机分钟数来再次进行循环，当打卡后，再重新生成随机数
    :param hourtype: 设置的上班时间点
    :param minute: 随机生成的分钟数（30-55）
    :return: None
    """
    now_time = datetime.datetime.now()
    now_hour = now_time.hour
    now_minute = now_time.minute
    global  count
    # 上班，不是周末（双休），小时对应，随机分钟对应
    if hourtype == 1 and is_weekend():
        random_time = random_minute()
        print("进入打开程序延时时间:",str(random_time))
        time.sleep(random_time)
        dingding(directory).goto_work(random_time)
        dingding(directory).open_mydemo()
        count = count + 1
        if count <= 2 :
          print("满足条件再次调用")
          hourtype = 3
          scheduler.enter(30+random_time,0,incode_loop,(start_loop,random_time,))
    if hourtype == 2 and is_weekend():
        random_time = random_minute()
        dingding(directory).sendEmailTest(random_time)
        scheduler.enter(60+random_time,0,incode_loop,(start_loop,random_time,))
    else:
        print(now_hour,':',now_minute)
        scheduler.enter(90,0,incode_loop,(start_loop,random_minute(),))

# 是否是周末
def is_weekend():
    """
    :return: if weekend return False else return True
    """
    now_time = datetime.datetime.now().strftime("%w")
    if now_time == "6" or now_time == "0":
        return False
    else:
        return True


if __name__ == "__main__":
    # ======formal
    scheduler.enter(0,0,incode_loop,(start_loop,random_minute(),))
    scheduler.run()
    # ====test
    #dingding  = dingding(directory)
    #dingding.sendEmailTest(1)
    # ==== weekend
    #print(is_weekend())

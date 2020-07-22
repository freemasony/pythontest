import socket
import urllib
from copy import copy
from multiprocessing import Process
from time import sleep
from urllib import request


class CatchVideo(object):
    def __init__(self):
        self.headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        self.url = ""

    def set_url(self, i):
        if i < 100:
            self.url = "https://wuji.zhulong-zuida.com/20190706/762_c260ca6c/800k/hls/36962c1a1b00000%02d.ts" % i
        elif i> 100 and i< 999:
            self.url = "https://wuji.zhulong-zuida.com/20190706/762_c260ca6c/800k/hls/36962c1a1b0000%03d.ts" % i
        else:
            self.url = "https://wuji.zhulong-zuida.com/20190706/762_c260ca6c/800k/hls/36962c1a1b000%04d.ts" % i

    # 获取并下载ts文件
    def dl_ts(self, i):
        rq = request.Request(self.url)
        rq.add_header('User-Agent', self.headers)
        response = request.urlopen(rq)
        resread = response.read()
        with open("video/"+'{:0>4d}'.format(i)+".ts", "wb") as f:
            f.write(resread)
        response.close()# 关闭urlopen方法，防止被ban

    def start_work(self, i):
        self.set_url(i)
        try:
            self.dl_ts(i)
            print(str(i) + ".ts  success")
            sleep(1)
        except urllib.error.URLError as e:
            print(e.reason)
            self.dl_ts(i)
        except socket.timeout as e2:
            print(e2.reason)
            self.dl_ts(i)

if __name__ == '__main__':

    catch_video = CatchVideo()
    socket.setdefaulttimeout(20)  # 设置socket层超时时间20秒
    I = 999
    while I < 2540 + 1:
        # 5个进程并发运行
        p_l = [Process(target=catch_video.start_work, args=(i,)) for i in range(I, I + 8)]
        for p in p_l:
            p.start()
        for p in p_l:
            p.join()
        I = I + 8
#https://wuji.zhulong-zuida.com/20190706/762_c260ca6c/index.m3u8
#https://wuji.zhulong-zuida.com/20190706/762_c260ca6c/800k/hls/36962c1a1b0000127.ts
#copy /b *.ts fnew.ts
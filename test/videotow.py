import os
import socket
import urllib
from multiprocessing import Process
from time import sleep
from urllib import request

import requests


class CatchVideo(object):
    def __init__(self):
        self.headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        self.url = ""
        self.index_url = ""

    def set_url(self, url):
        self.url = url

    def dl_ts(self, i):
        rq = request.Request(self.url)
        rq.add_header('User-Agent', self.headers)
        response = request.urlopen(rq)
        resread = response.read()
        with open("video/" + '{:0>4d}'.format(i) + ".ts", "wb") as f:
            f.write(resread)
        response.close()  # 关闭urlopen方法，防止被ban

    def get_ts_url(self):
        r = requests.get(self.index_url)
        r.encoding = 'utf-8'

        if r.text.split('\n')[-1] == '':
            hls_mark = r.text.split('\n')[-2]  # 以防\n结尾
        else:
            hls_mark = r.text.split('\n')[-1]
        url_m3u8_hls = self.index_url.replace('index.m3u8', hls_mark)

        print(url_m3u8_hls)
        base_url = url_m3u8_hls.replace('index.m3u8', '')

        r = requests.get(url_m3u8_hls)
        r.encoding = 'utf-8'

        text_bytes = list(r.iter_lines())

        # 转化成正常string
        text_string = [i.decode('utf-8') for i in text_bytes]

        ts_name = [i for i in text_string if not i.startswith('#')]

        return base_url, ts_name

    def file_walker(self, path):
        file_list = []
        for root, dirs, files in os.walk(path):  # 生成器
            for fn in files:
                p = str(root + '/' + fn)
                file_list.append(p)

        return file_list

    def combine(self, ts_path, combine_path, file_name):
        file_list = self.file_walker(ts_path)
        file_path = combine_path + file_name + '.ts'
        with open(file_path, 'wb+') as fw:
            for i in range(len(file_list)):
                fw.write(open(file_list[i], 'rb').read())

    def start_work(self, i, url):
        self.set_url(url)
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
    catch_video.index_url = 'https://wuji.zhulong-zuida.com/20190706/762_c260ca6c/index.m3u8'
    ts_url, ts_name = catch_video.get_ts_url()
    I = 104
    while I < 110:
        # 5个进程并发运行
        p_l = [Process(target=catch_video.start_work, args=(i, ts_url + ts_name[i])) for i in range(I, I + 8)]
        for p in p_l:
            p.start()
        for p in p_l:
            p.join()
        I = I + 8

    print('ts_download end....')
    catch_video.combine('video','video/','fnew')

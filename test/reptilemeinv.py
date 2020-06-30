import os
import re
import threading
import time

import requests
from bs4 import BeautifulSoup


class MeiNv:
    headers = {
        "Cookie": "__cfduid=d4c86067c3b6c4181c9d20440bac4a3953093326439",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/81.0.4044.138 Safari/537.36"
    }

    def get_cookies(self):
        url = "http://www.netbian.com/"
        response = requests.get(url=url)
        self.headers = {
            "Cookie": "__cfduid=" + response.cookies["__cfduid"],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/81.0.4044.138 Safari/537.36"
        }

    # 获取图片列表
    def get_image_list(self, url):
        try:
            time.sleep(2)
            response = requests.get(url=url, headers=self.headers, timeout=(3, 30))
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html.parser')
            li_list = soup.select("#main > div.list > ul > li")
            for li in li_list:
                a = li.select_one("li > a")
                if a is not None:
                    name = a.attrs["href"][a.attrs["href"].rfind('/') + 1:len(a.attrs["href"])].split('.')[0]
                    href = "http://www.netbian.com" + a.attrs["href"]
                    self.get_image(href, name)
        except Exception as e:
            self.get_cookies()
            print('get_image_list', e)

    def get_image(self, href, filename):
        try:
            response = requests.get(url=href, headers=self.headers, timeout=(3, 30))
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html.parser')
            image_href = "http://www.netbian.com" + soup.select_one("#main > div.endpage > div > p > a").attrs["href"]
            self.get_image_src(image_href, filename)
        except Exception as e:
            self.get_cookies()
            print('get_image', e)

    def get_image_src(self, href, filename):
        try:
            time.sleep(3)
            response = requests.get(url=href, headers=self.headers, timeout=(3, 30))
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html.parser')
            src = soup.select("img")[1].attrs["src"]
            self.download_image(src, filename)
        except Exception as e:
            self.get_cookies()
            print('get_image_src', e)

    # 下载图片
    def download_image(self, image_src, filename):
        try:
            title = filename.replace('.', '')
            end = os.path.splitext(image_src)[1]
            end = re.sub(r'[，。?？,/\\·]', '', end)
            image_path = "images/" + title + end,
            image_path = list(image_path)
            response = requests.get(image_src, headers=self.headers, timeout=(3, 30))
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            with open(image_path[0], 'wb') as f:
                f.write(img)
        except Exception as e:
            self.get_cookies()
            print('download_image', e)

    def create_dir(self, name):
        if not os.path.exists(name):
            os.makedirs(name)


if __name__ == '__main__':
    queue = [i for i in range(1, 20)]
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and len(queue) > 0:  # 最大线程数设置为 5
            cur_page = queue.pop(0)
            mv = MeiNv()
            mv.create_dir('images/')
            mv.get_cookies()
            url = "http://www.netbian.com/meinv/index_{}.htm".format(cur_page)
            thread = threading.Thread(target=mv.get_image_list, args=(url,))
            thread.start()
            threads.append(thread)
            time.sleep(1)
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))


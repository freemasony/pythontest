import os
import re
import threading

import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 '
                  'Safari/537.36'}


def get_pic_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find_all('img', class_='img-responsive')
    for i in pic_list:
        link = i.get('data-backup')
        if not link is None:
            end = os.path.splitext(link)[1]
            filename = link[link.rfind('/')+1:len(link)]
            # 去除特殊字符
            end = re.sub(r'[，。?？,/\\·]', '', end)
            download(link, filename)


def task_execute(url):
    page_html = request_page(url)
    get_pic_list(page_html)


def download(src, filename):
    try:
        # 请求图片地址
        response = requests.get(src, headers=headers)
        # 拼接图片地址

        path = "images/" + filename
        # 保存文件
        f = open(path, "wb")
        f.write(response.content)
        f.close()
    except Exception as e:
        print(e)


def request_page(url):
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return r.text


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main():
    create_dir('images')
    queue = [i for i in range(1, 5)]   # 构造 url 链接 页码。
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and len(queue) > 0:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            url = 'https://www.doutula.com/photo/list?page={}'.format(cur_page)
            thread = threading.Thread(target=task_execute, args=(url,))
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()

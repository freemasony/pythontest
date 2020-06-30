
import os
import urllib

import requests
from lxml import etree

# headers = {
#     'Referer':'http://music.163.com/',
#     'Host':'music.163.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     }

headers = {
    'Host':'f2.htqyy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cookie': '__cfduid=d0421cef33f4502f4acb9744e0e2fd5a91593514469; Hm_lvt_74e11efe27096f6ef1745cd53f168168=1593514529; blk=0; Hm_lpvt_74e11efe27096f6ef1745cd53f168168=1593514730'
    }

get = requests.get('http://f2.htqyy.com/play8/329/mp3/6', headers=headers)

# urllib.request.urlretrieve('http://f2.htqyy.com/play8/329/mp3/6', 'music/aa.mp3')
with open('music/a.mp3', "wb") as f:
    f.write(get.content)


url = "https://music.163.com/discover/toplist?id=3778678"
base_url = 'http://music.163.com/song/media/outer/url?id='
d = dict()
re = requests.get(url=url, headers=headers)
# 构造了一个XPath解析对象并对HTML文本进行自动修正

html = etree.HTML(re.content)
# XPath使用路径表达式来选取
x = html.xpath('//a[contains(@href,"/song?")]')

# 对取到的数据进行筛选
for data in x:
    # 获取到音乐url
    href = data.xpath('./@href')[0]
    id = href.split("=")[1]
    href = base_url + "%s.mp3" % id
    # 添加到字典
    if "$" not in id:
        # 获得到标签内的文本（即音乐的名称）
        name = data.xpath('./text()')[0]
        d[href] = name
for i in d:
    # 文件夹不存在，则创建文件夹
    save_path = 'music/'
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path)
    # 下载音乐到当前目录的music文件夹下
    get = requests.get('http://f2.htqyy.com/play8/329/mp3/6', headers=headers)

    # urllib.request.urlretrieve('http://f2.htqyy.com/play8/329/mp3/6', 'music/aa.mp3')
    with open('music/%s.mp3' % d[i], "wb") as f:
        print("正在下载歌曲 《%s》 ..." % d[i])
        f.write(get.content)

import re
import requests
from bs4 import BeautifulSoup
import time

# 去除content内的tag标签

def removeTag(content):
    _content = content.contents
    dr = re.compile(r'<[^>]+>', re.S)  # 匹配tag标签
    twitter = ''
    for i in _content:
        # 遍历传入的content所有的子节点
        j = str(i)
        dd = dr.sub('',j)
        if dd.find('http') == -1:
          twitter+=dd
    return twitter
    # return _content
# 将时间戳转化为时间的格式


def transformTimestamp(timestamp):
    time_local = time.localtime(int(timestamp))
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

# 判断images集合是否有img数据,如果有就返回,没有就返回空数组


def hasImage(images):
    _images = []
    if images:
        for i in images:
            _images.append(i['data-image-url'])
        return _images
    else:
        return _images

# 接收twitter_id发送请求


def InitSoup(userId):
    proxies = {
        'https': 'https://127.0.0.1:1087',
        'http': 'http://127.0.0.1:1087'
    }
    html = requests.get('https://twitter.com/'+userId, proxies=proxies)
    soup = BeautifulSoup(html.text, 'html.parser')
    # 获取主体
    body = soup.find_all(class_='route-profile')[0]
    return body

import requests
from bs4 import BeautifulSoup
import json
from utils import transformTimestamp


userId = 'lego'

proxies = {
    'https': 'https://127.0.0.1:1087',
    'http': 'http://127.0.0.1:1087'
}

html = requests.get('https://www.instagram.com/' + userId, proxies=proxies)
bs = BeautifulSoup(html.content, 'html.parser')
contents = bs.find_all('script', {'type': 'text/javascript'})[3]


instagrams = []


for content in contents:
    if 'window._sharedData' in content:
        jsonStr = content.string.strip('window._shareData = ')
        jsonStr = jsonStr.strip(';')
        jsonStr = json.loads(jsonStr)
        insPosts = jsonStr['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        # 这里使用loads转换为python格式的数据进行操作整理 导出应该用dumps转化为json数据
        # print(len(insPosts))
        for item in insPosts:
          if item['node']['is_video']:
            instagrams.append({
              'context': item['node']['edge_media_to_caption']['edges'][0]['node']['text'],
              'timer': transformTimestamp(item['node']['taken_at_timestamp']),
              'cover': item['node']['display_url'],
              'images': None,
              'source': 'instagram'
            })
          else:
            if "edge_sidecar_to_children" in item['node']:
              images = []
              for child in item['node']['edge_sidecar_to_children']['edges']:
                images.append(child['node']['display_url'])
              instagrams.append({
                'context': item['node']['edge_media_to_caption']['edges'][0]['node']['text'],
                'timer': transformTimestamp(item['node']['taken_at_timestamp']),
                'cover': item['node']['display_url'],
                'images': images,
                'source': 'instagram'
              })
            else:
              instagrams.append({
              'context': item['node']['edge_media_to_caption']['edges'][0]['node']['text'],
              'timer': transformTimestamp(item['node']['taken_at_timestamp']),
              'cover': item['node']['display_url'],
              'images': None,
              'source': 'instagram'
            })

return json.dumps(instagrams)
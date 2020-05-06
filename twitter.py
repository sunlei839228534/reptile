
from utils import removeTag, transformTimestamp, InitSoup, hasImage

getId = 'ev'

body = InitSoup(getId)

# 获取用户推文
# 转推的帖子不会被爬取到,只有用户自己推送的文字和图片会被爬取
# 返回格式
# {
#  context: String,
#  images: Array,
#  timer: Date,
# }


def getUserTwitter(body):
    twitters = []
    items = body.find_all(
        'li', class_='js-stream-item stream-item stream-item')
    for i in items:
        p = i.find('div')
        if p['data-screen-name'] == getId:  # 分辨转推还是个人推送,但是会有遗漏
            twitter = p.find(
                'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
            images = p.find_all(
                'div', class_='AdaptiveMedia-photoContainer js-adaptive-photo')
            timer = p.find('span', class_='_timestamp js-short-timestamp')
            # 多加一层判断,如果转推是没有timer的
            if timer:
                twitters.append({
                    'context': removeTag((twitter)),
                    'images': hasImage(images),
                    'timer': transformTimestamp(timer['data-time'])
                })
    return twitters

print(getUserTwitter(body))
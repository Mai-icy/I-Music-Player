import requests


# 相关信息 https://iobaka.com/blog/5.html
url = 'http://music.163.com/api/search/pc'
url_download = 'http://music.163.com/api/song/media?id=%d'

data = {
    's': 'mili',
    'offset': 0,
    'limit': 10,
    'type': 1,  # 类型(歌曲：1、专辑：10、歌手：100、歌单：1000、用户：1002、mv：1004)
}

a = requests.post(url, data=data)


b = requests.get(url_download % 435278010)

print(b.json())








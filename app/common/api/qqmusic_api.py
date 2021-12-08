import sys
import os
import base64
import requests

header = {
    "Referer": "https://y.qq.com/n/ryqq/search?w=miku&t=song&remoteplace=txt.yqq.top"
}

url = 'https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8' \
      '&notice=0&platform=h5&needNewCode=1&w=miku&zhidaqu=1&catZhida=1&t=0&flag=1&ie=utf-8&sem=1&aggr=0&perpage=20&n' \
      '=20&p=2&remoteplace=txt.mqq.all&_=1520833663464 '

a = requests.get(url, headers=header)
print(a.text)

class QMusicApi(object):
    def __init__(self):
        self.search_url = 'https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?g_tk=5381&uin=0&format=json&inCharset' \
                          '=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&w=%s&zhidaqu=1&catZhida=1&t=0' \
                          '&flag=1&ie=utf-8&sem=1&aggr=0&perpage=20&n=20&p=%d&remoteplace=txt.mqq.all&_=1520833663464'




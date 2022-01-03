import sys
import os
import base64
import requests

header = {
    "Referer": "https://y.qq.com/n/ryqq/search?w=miku&t=song&remoteplace=txt.yqq.top"
}

url = 'http://59.37.96.220/soso/fcgi-bin/client_search_cp?format=json&t=0&inCharset=GB2312&outCharset=utf-8&qqmusic_ver=1302&catZhida=0&p=1&n=2&w=miku'

a = requests.get(url, headers=header)
print(a.text)


class QQMusicApi(object):
    def __init__(self):
        self.__search_url = 'http://59.37.96.220/soso/fcgi-bin/client_search_cp?format=json&t=0&inCharset=GB2312&outCharset=utf-8&qqmusic_ver=1302&catZhida=0&p=%d&n=10&w=%s'
        self.__album_pic_url = "https://y.gtimg.cn/music/photo_new/T002R300x300%s.jpg"

    def search_data(self, word: str, page: int = 1) -> list:
        word = word.replace('#', '')
        res_json = requests.get(self.__search_url % (page, word)).json()
        res_list = []
        if res_json["code"] != 0 or len(list(res_json["data"]["song"]["list"])) == 0:
            return []
        for data in res_json["result"]["songs"]["list"]:
            duration = data["interval"]
            artists_list = []
            for artist_info in data["singer"]:
                artists_list.append(artist_info["name"])
            song_data = {
                "songId": str(data['id']),
                "songName": data['name'],
                "singer": ','.join(artists_list),
                "duration": '%d:%d%d' % (duration // 60, duration % 60 // 10, duration % 10),
            }





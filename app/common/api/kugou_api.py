import sys
import os
import base64
import requests


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1'}


class KuGouApi(object):
    def __init__(self):
        # 获取hash值需要搜索关键词。获取access_key和id需要hash值。下载文件需要access_key和id
        self.get_hash_search_url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=%d&pagesize=20&showtype=1'
        self.get_key_search_url = 'http://krcs.kugou.com/search?ver=1&man=yes&client=mobi&keyword=&duration=&hash=%s&album_audio_id='
        self.download_url = 'http://lyrics.kugou.com/download?ver=1&client=pc&id=%s&accesskey=%s&fmt=%s&charset=utf8'

        self.hash_list = []
        self.id_key_list = []

        self.download_path = 'download\\Lyric'
        self.music_name = ''

    def search_hash(self, keyword: str, page=1, is_change_hash=True) -> (int, list):
        if is_change_hash:
            self.hash_list.clear()
        self.id_key_list.clear()
        res_data_list = []
        url = self.get_hash_search_url % (keyword, page)
        res_json = requests.get(url, headers=header).json()
        total_num = res_json['data']['total']
        for data in res_json['data']['info']:
            print(data)
            if is_change_hash:
                self.hash_list.append((data['songname'], data['hash']))
            res_data_list.append((data['songname'], data['singername'], data['album_name'], data['duration']))
        return total_num, res_data_list

    def search_id_key(self, hash_list_index, hash_=None) -> list:
        self.id_key_list.clear()
        res_data_list = []
        self.music_name = self.hash_list[hash_list_index][0]
        hash_value = self.hash_list[hash_list_index][1]
        if hash_:
            hash_value = hash_
        url = self.get_key_search_url % hash_value
        res_json = requests.get(url, headers=header).json()
        if res_json['errcode'] == 200:
            if not len(res_json['candidates']):
                return []
            for data in res_json['candidates']:
                id_key = (data['id'], data['accesskey'])
                self.id_key_list.append(id_key)
                res_data_list.append((data['product_from'], data['nickname'], data['score'], data['duration']))
            return res_data_list
        else:
            print('api接受发送错误')
            sys.exit(0)

    def download_krc_or_lrc(self, id_key_list_index, fmt='krc') -> None:
        id_key = self.id_key_list[id_key_list_index]
        url = self.download_url % (id_key[0], id_key[1], fmt)
        res_json = requests.get(url).json()
        content = res_json['content']
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)
        if fmt == 'krc':
            result = base64.b64decode(content.encode())
            with open('%s\\%s.krc' % (self.download_path, self.music_name), 'wb') as f:
                f.write(result)
                f.close()

    def search_hash_2(self, keyword: str, page=1, is_change_hash=True) -> (int, list):
        if is_change_hash:
            self.hash_list.clear()
        self.id_key_list.clear()
        res_data_list = []
        url = self.get_hash_search_url % (keyword, page)
        res_json = requests.get(url, headers=header).json()
        total_num = res_json['data']['total']
        for data in res_json['data']['info']:
            song_info = {
                "singer": data['singername']

            }
            print(data)
            if is_change_hash:
                self.hash_list.append((data['songname'], data['hash']))
            res_data_list.append((data['songname'], data['singername'], data['album_name'], data['duration']))
        return total_num, res_data_list


class KugouApi(object):
    def __init__(self):
        # 获取hash值需要搜索关键词。获取access_key和id需要hash值。下载文件需要access_key和id
        self.get_hash_search_url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=%d&pagesize=20&showtype=1'
        self.get_key_search_url = 'http://krcs.kugou.com/search?ver=1&man=yes&client=mobi&keyword=&duration=&hash=%s&album_audio_id='
        self.download_url = 'http://lyrics.kugou.com/download?ver=1&client=pc&id=%s&accesskey=%s&fmt=%s&charset=utf8'
        self.album_info_url = 'http://mobilecdn.kugou.com/api/v3/album/song?version=9108&albumid=%d&plat=0&pagesize=100&area_code=1&page=1&with_res_tag=1'

    def test(self):
        res_json = requests.get(self.get_hash_search_url % ('miku', 1), headers=header).json()
        print(res_json)

    def test2(self):
        q = 'a728537143d00dd12ff80fcc85be6275'
        res_json = requests.get(self.album_info_url % 32275716).text
        print(res_json)


if __name__ == '__main__':
    a = KugouApi()
    a.test()
    # a = KuGouApi()
    # w1 = a.search_hash('mili', 1)
    # w2 = a.search_id_key(0)
    # a.download_krc_or_lrc(0, 'krc')

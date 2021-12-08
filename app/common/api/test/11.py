import requests






search_url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=1&pagesize=20&showtype=1'


url2 = 'http://krcs.kugou.com/search?ver=1&man=yes&client=mobi&keyword=&duration=&hash=%s&album_audio_id='

url3 = 'http://lyrics.kugou.com/download?ver=1&client=pc&id=%d&accesskey=%s&fmt=krc&charset=utf8'

res1 = requests.get(search_url % 'Mili - Camelia')

res = requests.get(url2 % '295157d168a2a19fd2b015ebc9c6f0bb')

res = requests.get(url3 % (28546081, 'E7C5E004674DF3FDFE59D88A722E2BBE'))

print(res1.json())
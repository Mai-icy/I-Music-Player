import common.song_metadata as sm
import common.api.cloud_api as api

import os


song_path = r"Z:\KuGou\2021.6.21"

song_list = os.listdir(song_path)


song_name_list = list(map(lambda x: os.path.splitext(x)[0], song_list))

song_path_list = list(map(lambda x: song_path + '\\' + x, song_list))

api_c = api.CloudMusicWebApi()

sm.PIC_SAVE_PATH = r'..\\..\\resource\\album_pic\\%s.jpg'

# song_data_list = list(map(lambda x: sm.get_song_metadata(x), song_path_list))
# print(song_data_list)
for song in song_path_list:
    try:
        song_da = sm.get_song_metadata(song)

        search_data = api_c.search_data(song_da['songName'] + ' - ' + song_da['singer'])
        print(search_data)
        order = int(input("请选择："))
        if order == -1:
            continue
        song_id = search_data[order - 1]["songId"]
        song_data = api_c.search_song_info(song_id)
        print(song_data)
        flag = input('yn?')
        if flag:
            sm.write_song_metadata.write_mp3_metadata(song.replace('\\', '/'), song_data)
    except:
        print('1')
        continue


















#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import io

import requests
from mutagen import id3
from mutagen.flac import FLAC, Picture

from common.path import LRC_PATH, PLAYLIST_SAVE_PATH


def write_flac_metadata(song_path: str, song_info: dict, pic_buffer: io.BytesIO = None):
    """
    Write metadata of flac file. If FLAC has multiple images, clear them all and write only one.
    :param song_path: the path of song
    :param song_info: the info of song
    :param pic_buffer: the buffer of cover picture(jpg)
    :return: Return false if the image url connection times out
    """
    try:
        audio = FLAC(song_path)
        if song_info['songName']:
            audio["TITLE"] = song_info['songName']
        if song_info['singer']:
            audio["ARTIST"] = song_info['singer']
        if song_info['album']:
            audio["ALBUM"] = song_info['album']
        if song_info['trackNumber']:
            audio["TRACKNUMBER"] = song_info['trackNumber']
        if song_info['year']:
            audio["DATE"] = song_info['year']
        if song_info['genre']:
            audio["GENRE"] = song_info['genre']
        # audio["ALBUMARIST"] = song_info['singer']
        pic = Picture()
        pic.type = id3.PictureType.COVER_FRONT
        pic.mime = u"image/jpeg"
        pic.width = 500
        pic.height = 500
        pic.depth = 16  # color depth
        if pic_buffer and pic_buffer.getvalue():
            pic.data = pic_buffer.getvalue()
            if len(audio.pictures):
                audio.clear_pictures()
            audio.add_picture(pic)
        elif song_info["picUrl"]:
            pic_url = song_info["picUrl"]
            try:
                pic_data = requests.get(pic_url, timeout=(4, 8))
                pic.data = pic_data.content
                audio.add_picture(pic)
            except requests.exceptions.RequestException:
                return False
        audio.save()
        return True
    except Exception:
        return False


def write_mp3_metadata(song_path: str, song_info: dict, pic_buffer: io.BytesIO = None) -> bool:
    """
    Write id3 metadata of mp3 file.
    :param song_path: the path of song
    :param song_info: the info of song
    :param pic_buffer: the buffer of cover picture(jpg)
    :return: Return false if the image url connection times out
    """
    try:
        audio = id3.ID3(song_path)
    except Exception:
        return False
    if song_info["songName"]:
        audio["TIT2"] = id3.TIT2(text=song_info["songName"])
    if song_info["singer"]:
        audio["TPE1"] = id3.TPE1(text=song_info["singer"])
    if song_info["album"]:
        audio["TALB"] = id3.TALB(text=song_info["album"])
    if song_info["trackNumber"]:
        audio["TRCK"] = id3.TRCK(text=song_info["trackNumber"])
    if song_info["year"]:
        audio["TYER"] = id3.TYER(text=song_info["year"])
    if song_info["genre"]:
        audio["TCON"] = id3.TCON(text=song_info["genre"])
    if pic_buffer and pic_buffer.getvalue():
        audio["APIC:"] = id3.APIC(encoding=3, mime='image/jpeg', type=3, data=pic_buffer.getvalue())
    elif song_info["picUrl"]:
        pic_url = song_info["picUrl"]
        try:
            pic_data = requests.get(pic_url, timeout=(4, 8))
        except requests.exceptions.RequestException:
            return False
        audio["APIC:"] = id3.APIC(encoding=3, mime='image/jpeg', type=3, data=pic_data.content)
    audio.update_to_v23()
    audio.save(v2_version=3)
    return True


def update_md5_to_file(old_md5: str, new_md5: str) -> bool:
    """
    Update the content and file names of playlists and lyrics files with the new MD5

    :param old_md5: Previous MD5 value
    :param new_md5: Change the MD5 value of the file
    :return:
    """
    lrc_file_list = os.listdir(LRC_PATH)
    for lrc_file in lrc_file_list:
        """ old
        file_name_list = os.path.splitext(lrc_file)[0].split('-')
        lrc_hash = file_name_list[2]
        if old_md5 == lrc_hash:
            lrc_path = LRC_PATH + lrc_file
            file_name_list[2] = new_md5
            os.rename(lrc_path, '-'.join(file_name_list))
            break
        """
        if lrc_file == old_md5 + ".mrc":
            os.rename(LRC_PATH + lrc_file, new_md5 + ".mrc")

    playlist_file_list = os.listdir(PLAYLIST_SAVE_PATH)
    for playlist_file in playlist_file_list:
        file_data = open(PLAYLIST_SAVE_PATH + playlist_file, 'r+', encoding='utf-8').read()
        with open(PLAYLIST_SAVE_PATH + playlist_file, 'w', encoding='utf-8') as f:
            f.write(file_data.replace(old_md5, new_md5))
    return True


if __name__ == "__main__":
    pass

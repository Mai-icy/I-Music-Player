from mutagen.flac import FLAC, Picture
from mutagen import id3
import requests


def write_flac_metadata(song_path: str, song_info: dict, pic_path=None):
    """
    Write metadata of flac file.

    :param song_path: the path of song
    :param song_info: the info of song
    :param pic_path: the path of cover picture(jpg)
    :return: Return false if the image url connection times out
    """
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
    if pic_path:
        with open(pic_path, "rb") as f:
            pic.data = f.read()
        audio.add_picture(pic)
    elif song_info["picUrl"]:
        pic_url = song_info["picUrl"]
        try:
            pic_data = requests.get(pic_url, timeout=(4, 8))
            pic.data = pic_data
            audio.add_picture(pic)
        except requests.exceptions.RequestException:
            return False
    audio.save()
    return True


def write_mp3_metadata(song_path: str, song_info: dict, pic_path=None) -> bool:
    """
    Write id3 metadata of mp3 file.

    :param song_path: the path of song
    :param song_info: the info of song
    :param pic_path: the path of cover picture(jpg)
    :return: Return false if the image url connection times out
    """
    audio = id3.ID3(song_path)
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
    if pic_path:
        audio["APIC:"] = id3.APIC(encoding=3, mime='image/jpeg', type=3, data=open(pic_path, 'rb').read())
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


if __name__ == "__main__":
    pass



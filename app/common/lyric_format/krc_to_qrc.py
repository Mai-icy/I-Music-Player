# coding:utf-8
import zlib

krc_keys = [64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105]
# Key      {'@','G','a','w', '^','2','t','G','Q','6', '1','-','Î', 'ò', 'n', 'i' }


class Decoder(object):
    def __init__(self, data=None, file_name=None):
        self._load(data, file_name)

    @staticmethod
    def decode(data):
        zd = bytes()
        for i in range(4, len(data)):
            zd += bytes([data[i] ^ krc_keys[(i - 4) % 16]])
        return zlib.decompress(zd).decode()[1:]

    def _load(self, data, file_name):
        if data:
            self._data = data
        elif file_name:
            with open(file_name, 'rb') as f_:
                self._data = f_.read()
                f_.close()
        else:
            self._data = ''

    def get_decoded(self):
        return self.decode(self._data)


if __name__ == '__main__':
    # decoder = Decoder(fileName='../test/Lucy-In-The-Sky-With-Diamonds.krc')
    # print(decoder.getDecoded())
    # f='../test/Real-love.krc'
    f = 'まふまふ - 空腹-74977ed9d20f5264a0aff0c4c1ab170d-53353527-00000000.krc'
    decoder = Decoder(file_name=f)
    print(decoder.get_decoded())

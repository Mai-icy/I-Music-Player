import codecs
import zlib
import re


def decompress_krc(krc_bytes):
    key = bytearray([0x0040,
                     0x0047,
                     0x0061,
                     0x0077,
                     0x005e,
                     0x0032,
                     0x0074,
                     0x0047,
                     0x0051,
                     0x0036,
                     0x0031,
                     0x002d,
                     0x00ce,
                     0x00d2,
                     0x006e,
                     0x0069])
    decompress_bytes = []
    i = 0
    for ch in krc_bytes[4:]:
        decompress_bytes.append(ch ^ key[i % 16])
        i = i + 1
    decode_bytes = zlib.decompress(
        bytearray(decompress_bytes)).decode('utf-8-sig')
    decode_bytes = re.sub(r'<[^>]*>', '', decode_bytes)
    for match in re.finditer(r'\[(\d*),\d*\]', decode_bytes):
        ms = int(match.group(1))
        # time = '[%.2d:%.2d.%.2d]' % ((ms % (
        #     1000 * 60 * 60)) / (1000 * 60), (ms % (1000 * 60)) / 1000, (ms % (1000 * 60)) % 100)  # 时间不准确爬
        time = '[%.2d:%.2d.%.3d]' % ((ms % (
                1000 * 60 * 60)) / (1000 * 60), (ms % (1000 * 60)) / 1000, (ms % (1000 * 60)) % 1000)
        decode_bytes = decode_bytes.replace(match.group(0), time)
    return decode_bytes


def krc2lrc(file, save_to):
    with codecs.open(file, 'rb') as f:
        decode_bytes = decompress_krc(bytearray(f.read()))
        fp = codecs.open(save_to, "w", 'utf-8')
        fp.write(decode_bytes)
        fp.close()


if __name__ == "__main__":
    krc2lrc('..\\api\\1.krc', '1.lrc')
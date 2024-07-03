import struct
from dataclasses import dataclass
import numpy as np


# BitMap 클래스
class Bitmap:
    def __init__(self, filename):
        with open(filename, "rb") as f:
            # BitmapFileHeader (14 bytes)
            bf_header_bits = f.read(14)
            bf_header = struct.unpack('<2sIHHI', bf_header_bits)
            self.bitmap_file_header = BitmapFileHeader(*bf_header)

            # BitmapInfoHeader (40 bytes)
            bi_header_bits = f.read(40)
            bi_header = struct.unpack('<IIIHHIIIIII', bi_header_bits)
            self.bitmap_info_header = BitmapInfoHeader(*bi_header)

            bi_width = self.bitmap_info_header.biWidth
            bi_height = self.bitmap_info_header.biHeight
            bi_bit_count = self.bitmap_info_header.biBitCount

            # Pixel Data
            if bi_bit_count != 24:
                palette_num = 2 ** bi_bit_count
                self.palette = np.frombuffer(f.read(4 * palette_num), dtype=np.uint8).reshape((palette_num, 4))[:, :3]

                pixel_data_size = (((bi_width * bi_bit_count // 8) + 3) & ~3) * bi_height

                color_index = np.frombuffer(f.read(pixel_data_size), dtype=np.uint8)
                self.pixel_data = self.palette[color_index].reshape(bi_height, bi_width, 3)
            else:
                pixel_data_size = 3 * ((bi_width + 3) & ~3) * bi_height
                self.pixel_data = np.frombuffer(f.read(pixel_data_size), dtype=np.uint8).reshape(bi_height, bi_width, 3)


# 비트맵 파일 헤더
@dataclass
class BitmapFileHeader:
    bfType: bytes
    bfSize: int
    bfReserved1: int
    bfReserved2: int
    bfOffBits: int


# 비트맵 정보 헤더
@dataclass
class BitmapInfoHeader:
    biSize: int
    biWidth: int
    biHeight: int
    biPlanes: int
    biBitCount: int
    biCompression: int
    biSizeImage: int
    biXPelsPerMeter: int
    biYPelsPerMeter: int
    biClrUsed: int
    biClrImportant: int


# RGBQuad
@dataclass
class RGBQuad:
    rgbBlue: int
    rgbGreen: int
    rgbRed: int
    rgbReserved: int


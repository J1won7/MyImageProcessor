import struct
from dataclasses import dataclass
from PIL import Image


# BitMap 클래스
class Bitmap:
    def __init__(self, filename):
        with open(filename, "rb") as f:
            # BitmapFileHeader (14 bytes)
            bf_header_bits = f.read(14)
            bf_header = struct.unpack('<2sIHHI', bf_header_bits)
            self.bitmapFileHeader = BitmapFileHeader(*bf_header)

            # BitmapInfoHeader (40 bytes)
            bi_header_bits = f.read(40)
            bi_header = struct.unpack('<IIIHHIIIIII', bi_header_bits)
            self.bitmapInfoHeader = BitmapInfoHeader(*bi_header)

            # 색상 테이블(팔레트)
            self.palette = []
            if self.bitmapInfoHeader.biBitCount != 24:
                palette_num = 2 ** self.bitmapInfoHeader.biBitCount
                rgbQuad_bits = struct.unpack('<' + 'BBBB' * palette_num, f.read(4 * palette_num))
                for i in range(0, len(rgbQuad_bits), 4):
                    self.palette.append(RGBQuad(*rgbQuad_bits[i:i+4]))

            # Pixel Data
            image_size = ((self.bitmapInfoHeader.biWidth * self.bitmapInfoHeader.biHeight // 8) + 3 & ~3) * self.bitmapInfoHeader.biBitCount
            self.pixelData = f.read(image_size)

    def get_image(self):
        bi = self.bitmapInfoHeader
        width = bi.biWidth
        height = bi.biHeight
        bit_count = bi.biBitCount
        data = self.pixelData

        if bit_count == 24:  # 24-bit bitmap (True Color)
            img = Image.frombytes('RGB', (width, height), data, 'raw', 'BGR', 0, 1)
        else:  # n-bit bitmap (Indexed Color)
            img = Image.frombytes('P', (width, height), data, 'raw', 'P', 0, 1)
            palette_data = []
            for rgb_quad in self.palette:
                palette_data.extend([rgb_quad.rgbRed, rgb_quad.rgbGreen, rgb_quad.rgbBlue])
            img.putpalette(palette_data)

        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # 상하 반전
        return img


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


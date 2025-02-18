# coding: utf-8
from math import floor
import time
import numpy as np
from colorthief import ColorThief


class DominantColor:
    """ 图像主题色类 """

    @classmethod
    def getDominantColor(cls, imagePath: str):
        """ 获取指定图片的主题色

        Parameters
        ----------
        imagePath: str
            图片路径

        Returns
        -------
        r, g, b: int
            主题色各个通道的灰度值
        """
        start_time = time.time()
        colorThief = ColorThief(imagePath)

        # 调整图像大小，加快运算速度
        if max(colorThief.image.size) > 400:
            colorThief.image = colorThief.image.resize((400, 400))

        palette = colorThief.get_palette(quality=9)

        # 调整调色板明度
        palette = cls.__adjustPaletteValue(palette)
        for rgb in palette[:]:
            h, s, v = cls.rgb2hsv(rgb)
            if h < 0.02:
                palette.remove(rgb)
                if len(palette) <= 2:
                    break

        # 挑选主题色
        palette = palette[:5]
        palette.sort(key=lambda rgb: cls.colorfulness(*rgb), reverse=True)
        end_time = time.time()
        execute_time = (end_time - start_time) * 1000
        print(f"execute_time: {execute_time}", palette[0])
        return palette[0]

    @classmethod
    def __adjustPaletteValue(cls, palette: list):
        """ 调整调色板的明度 """
        newPalette = []
        for rgb in palette:
            h, s, v = cls.rgb2hsv(rgb)

            if v > 0.9:
                factor = 0.8
            elif 0.8 < v <= 0.9:
                factor = 0.9
            elif 0.7 < v <= 0.8:
                factor = 0.95
            else:
                factor = 1

            v *= factor
            newPalette.append(cls.hsv2rgb(h, s, v))

        return newPalette

    @staticmethod
    def rgb2hsv(rgb: tuple) -> tuple:
        """ rgb空间变换到hsv空间 """
        r, g, b = [i / 255 for i in rgb]
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        s = 0 if mx == 0 else df / mx
        v = mx
        return h, s, v

    @staticmethod
    def hsv2rgb(h, s, v) -> tuple:
        """ hsv空间变换到rgb空间 """
        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    @staticmethod
    def colorfulness(r: int, g: int, b: int):
        rg = np.absolute(r - g)
        yb = np.absolute(0.5 * (r + g) - b)

        rg_mean, rg_std = np.mean(rg), np.std(rg)
        yb_mean, yb_std = np.mean(yb), np.std(yb)

        std_root = np.sqrt(rg_std ** 2 + yb_std ** 2)
        mean_root = np.sqrt(rg_mean ** 2 + yb_mean ** 2)

        return std_root + 0.3 * mean_root


DominantColor().getDominantColor('./images/cover1.jpg')
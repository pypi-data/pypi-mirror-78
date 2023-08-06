# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PIL import Image, ImageOps

OVERLAY_NAME = "kgw.png"


class Generator:
    """
    Generates a profile picture


    Attributes:
        background (PIL.Image): An Image object representing the picture
            on that the overlay will be printed.
        overlay (PIL.Image, optional): An Image object representing the picture
            that will be used as an overlay. By default it will use the
            overlay specified by the module
        scale (:obj:`int`, optional): How thick the border
            should be. Defaults to 0
        size (tuple, optional): Defines the size of the result.
            Background will be scaled to this size.
            Defaults to `(640, 640)`
    """

    def __init__(self, background, overlay=None, scale=0, size=(640, 640)):
        self.module_path = os.path.dirname(os.path.abspath(__file__))
        self.overlay = overlay or Image.open(f"{self.module_path}/"
                                             f"templates/{OVERLAY_NAME}")
        self.background = background
        self.scale = scale
        self.size = size

    @classmethod
    def _add_border(cls, img, border):
        if isinstance(border, int) or isinstance(border, tuple):
            bimg = ImageOps.expand(img, border=border)
        else:
            raise RuntimeError('Border is not an integer or tuple!')
        return bimg

    def process(self):
        """Renders the profile picture

        Returns:
            PIL.Image: The rendered picture

        """
        background = self.background.resize(self.size)
        background = background.convert('RGBA')
        background = self._add_border(background, self.scale)
        foreground = self.overlay.convert('RGBA').resize(background.size)

        result = Image.alpha_composite(background, foreground)
        return result

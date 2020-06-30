import numpy as np

from math import pi, sin, cos
from random import random, choice

from PIL.Image import Image

from skimage.util import random_noise, crop
from skimage.color import gray2rgb
from skimage.transform import rotate, resize

from torch.utils.data import Dataset


class Noise(object):
    def __init__(self, p=0.1):

        self.noise = random() < p

    def __call__(self, image):

        return random_noise(image, seed=0) if self.noise else image

    def __repr__(self):

        return "{}(noise={})".format(self.__class__.__name__, self.noise)


class FlipLR(object):
    def __init__(self, p=0.5):

        self.flip = random() < p

    def __call__(self, image):

        return np.fliplr(image) if self.flip else image

    def __repr__(self):

        return "{}(flip={})".format(self.__class__.__name__, self.flip)


class FlipUD(object):
    def __init__(self, p=0.5):

        self.flip = random() < p

    def __call__(self, image):

        return np.flipud(image) if self.flip else image

    def __repr__(self):

        return "{}(flip={})".format(self.__class__.__name__, self.flip)


class Rotate(object):
    def __init__(self, angle=np.arange(0, 180, 5)):

        if not isinstance(angle, np.ndarray):
            raise ValueError("angle must be an list of numbers")

        self.angle = choice(angle)

    def largest_rotated_rect(self, w, h, angle):

        width_is_longer = w >= h
        side_long, side_short = (w, h) if width_is_longer else (h, w)

        sin_a, cos_a = abs(sin(angle)), abs(cos(angle))

        if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a -
                                                               cos_a) < 1e-10:
            x = 0.5 * side_short
            wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a,
                                                                     x / sin_a)
        else:
            cos_2a = cos_a * cos_a - sin_a * sin_a
            wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a -
                                                        w * sin_a) / cos_2a

        return wr, hr

    def __call__(self, image):

        a = pi * self.angle / 180

        h0, w0 = image.shape[0], image.shape[1]

        image = rotate(image, self.angle, resize=True)

        h1, w1 = image.shape[0], image.shape[1]

        wx, hx = self.largest_rotated_rect(w0, h0, a)

        w2 = int((w1 - wx) / 2)
        h2 = int((h1 - hx) / 2)

        return crop(image, ((h2, h2), (w2, w2), (0, 0)), copy=False)

    def __repr__(self):

        return "{}(angle={})".format(self.__class__.__name__, self.angle)


class Square(object):
    def __init__(self):

        self.pos = random()

    def __call__(self, image):

        (h, w, _) = image.shape

        if h == w:
            return image

        if h < w:

            d = int(self.pos * (w - h))

            return crop(image, ((0, 0), (d, w - h - d), (0, 0)))

        else:

            d = int(self.pos * (h - w))

            return crop(image, ((d, h - w - d), (0, 0), (0, 0)))

    def __repr__(self):

        return "{}(pos={})".format(self.__class__.__name__, self.pos)


class Resize(object):
    def __init__(self, width=512, height=None):

        height = width if height is None else height

        self.width = width
        self.height = height

    def __call__(self, image):

        return resize(image, (self.height, self.width))

    def __repr__(self):

        return "{}(width={}, height={})".format(self.__class__.__name__,
                                                self.width, self.height)
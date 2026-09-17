import numpy as np
from PIL import Image


IMAGE_SIZE = (64, 64)


def image_to_matrix(image_path):
    original = Image.open(image_path).convert('L')
    resampling = getattr(Image, 'Resampling', Image)
    resample = getattr(resampling, 'LANCZOS', Image.BICUBIC)
    resized = original.resize(IMAGE_SIZE, resample)
    return np.asarray(resized, dtype=np.float64) / 255.0

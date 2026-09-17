from io import BytesIO
import base64

import numpy as np
from PIL import Image


def matrix_to_data_uri(matrix):
    image = Image.fromarray(np.uint8(np.clip(matrix, 0, 1) * 255), mode='L')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}'


def matrix_preview(matrix, rows=8, cols=8):
    limited = matrix[:rows, :cols]
    return [[round(float(value), 3) for value in row] for row in limited]


def eigenvalue_preview(eigenvalues, count=20):
    return [round(float(value), 4) for value in eigenvalues[:count]]

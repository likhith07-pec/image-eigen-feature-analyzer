import numpy as np


def matrix_size(matrix):
    return f'{matrix.shape[0]} x {matrix.shape[1]}'


def calculate_rank(matrix):
    return int(np.linalg.matrix_rank(matrix))


def matrix_min(matrix):
    return float(np.min(matrix))


def matrix_max(matrix):
    return float(np.max(matrix))


def analyze_matrix(matrix):
    return {
        'shape': matrix_size(matrix),
        'rank': calculate_rank(matrix),
        'minimum': matrix_min(matrix),
        'maximum': matrix_max(matrix),
    }

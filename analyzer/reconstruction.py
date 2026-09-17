import numpy as np


def select_components(eigenvectors, requested_k, max_k):
    selected_k = int(max(1, min(requested_k, max_k)))
    return selected_k, eigenvectors[:, :selected_k]


def project_matrix(matrix, selected_eigenvectors):
    return matrix @ selected_eigenvectors


def reconstruct_matrix(projection, selected_eigenvectors):
    return projection @ selected_eigenvectors.T


def calculate_frobenius_error(original_matrix, reconstructed_matrix):
    return float(np.linalg.norm(original_matrix - reconstructed_matrix, ord='fro'))


def calculate_relative_error(original_matrix, reconstructed_matrix):
    original_norm = np.linalg.norm(original_matrix, ord='fro')
    return float(calculate_frobenius_error(original_matrix, reconstructed_matrix) / original_norm)


def compare_components(original_matrix, eigenvectors, component_list):
    valid_k_values = sorted({k for k in component_list if 1 <= k <= original_matrix.shape[1]})
    original_norm = np.linalg.norm(original_matrix, ord='fro')
    rows = []

    for k in valid_k_values:
        vk = eigenvectors[:, :k]
        reconstructed = reconstruct_matrix(project_matrix(original_matrix, vk), vk)
        error = np.linalg.norm(original_matrix - reconstructed, ord='fro')
        rows.append(
            {
                'k': k,
                'error': round(float(error), 4),
                'relative_error': round(float(error / original_norm * 100), 4),
            }
        )

    return rows

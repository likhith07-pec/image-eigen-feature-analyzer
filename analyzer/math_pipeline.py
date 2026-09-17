import numpy as np

from .eigen_analysis import calculate_eigen_features, check_orthogonality
from .image_processing import image_to_matrix
from .matrix_analysis import analyze_matrix
from .reconstruction import (
    calculate_frobenius_error,
    calculate_relative_error,
    compare_components,
    project_matrix,
    reconstruct_matrix,
    select_components,
)
from .visualization import eigenvalue_preview, matrix_preview, matrix_to_data_uri


COMPONENT_LIST = [1, 5, 10, 20, 32, 64]


def analyze_image(image_path, requested_k):
    matrix = image_to_matrix(image_path)
    matrix_info = analyze_matrix(matrix)

    eigen_result = calculate_eigen_features(matrix)
    covariance_matrix = eigen_result['covariance_matrix']
    eigenvalues = eigen_result['eigenvalues']
    eigenvectors = eigen_result['eigenvectors']

    selected_k, vk = select_components(eigenvectors, requested_k, matrix.shape[1])
    projection = project_matrix(matrix, vk)
    reconstruction = reconstruct_matrix(projection, vk)
    orthogonality = check_orthogonality(vk)

    absolute_error = calculate_frobenius_error(matrix, reconstruction)
    relative_error_percent = calculate_relative_error(matrix, reconstruction) * 100
    eigen_tolerance = 1e-10
    eigenvalues_sorted = bool(np.all(np.diff(eigenvalues) <= eigen_tolerance))
    eigenvalues_nonnegative = bool(np.min(eigenvalues) >= -eigen_tolerance)

    return {
        'selected_k': selected_k,
        'max_k': matrix.shape[1],
        'matrix_shape': matrix_info['shape'],
        'matrix_rows': matrix.shape[0],
        'matrix_cols': matrix.shape[1],
        'covariance_shape': f'{covariance_matrix.shape[0]} x {covariance_matrix.shape[1]}',
        'vk_shape': f'{vk.shape[0]} x {vk.shape[1]}',
        'vk_transpose_shape': f'{vk.T.shape[0]} x {vk.T.shape[1]}',
        'projection_shape': f'{projection.shape[0]} x {projection.shape[1]}',
        'reconstruction_shape': f'{reconstruction.shape[0]} x {reconstruction.shape[1]}',
        'rank': matrix_info['rank'],
        'matrix_min': matrix_info['minimum'],
        'matrix_max': matrix_info['maximum'],
        'matrix_normalized': matrix_info['minimum'] >= 0 and matrix_info['maximum'] <= 1,
        'eigenvalues_sorted': eigenvalues_sorted,
        'eigenvalues_nonnegative': eigenvalues_nonnegative,
        'minimum_eigenvalue': float(np.min(eigenvalues)),
        'frobenius_error': absolute_error,
        'relative_error': relative_error_percent,
        'orthogonality_error': orthogonality['error'],
        'orthogonality_status': 'Verified' if orthogonality['verified'] else 'Not Verified',
        'original_image': matrix_to_data_uri(matrix),
        'reconstructed_image': matrix_to_data_uri(reconstruction),
        'matrix_preview': matrix_preview(matrix, rows=10, cols=10),
        'projection_preview': matrix_preview(projection, rows=10, cols=min(selected_k, 8)),
        'eigenvalues': eigenvalue_preview(eigenvalues),
        'dominant_eigenvalues': eigenvalue_preview(eigenvalues, count=6),
        'dominant_eigenvector_shape': f'{eigenvectors[:, :5].shape[0]} x {eigenvectors[:, :5].shape[1]}',
        'dominant_eigenvectors_preview': matrix_preview(eigenvectors[:, :5], rows=10, cols=5),
        'eigenvectors_preview': matrix_preview(eigenvectors[:, : min(selected_k, 6)], rows=8, cols=min(selected_k, 6)),
        'error_series': compare_components(matrix, eigenvectors, COMPONENT_LIST),
        'dimension_equation': f'({matrix.shape[0]} x {matrix.shape[1]})({vk.shape[0]} x {vk.shape[1]}) = {projection.shape[0]} x {projection.shape[1]}',
        'reconstruction_dimension_equation': f'({projection.shape[0]} x {projection.shape[1]})({vk.T.shape[0]} x {vk.T.shape[1]}) = {reconstruction.shape[0]} x {reconstruction.shape[1]}',
        'pipeline': [
            ('01', 'Upload'),
            ('02', 'Matrix'),
            ('03', 'Rank'),
            ('04', 'Eigen Analysis'),
            ('05', 'Components'),
            ('06', 'Projection'),
            ('07', 'Reconstruction'),
            ('08', 'Error'),
        ],
    }

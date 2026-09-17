import numpy as np


def calculate_covariance_matrix(matrix):
    return matrix.T @ matrix


def calculate_eigenpairs(covariance_matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    order = np.argsort(eigenvalues)[::-1]

    return {
        'eigenvalues': eigenvalues[order],
        'eigenvectors': eigenvectors[:, order],
    }


def calculate_eigen_features(matrix):
    covariance_matrix = calculate_covariance_matrix(matrix)
    eigenpairs = calculate_eigenpairs(covariance_matrix)

    return {
        'covariance_matrix': covariance_matrix,
        'eigenvalues': eigenpairs['eigenvalues'],
        'eigenvectors': eigenpairs['eigenvectors'],
    }


def check_orthogonality(eigenvectors):
    orthogonality_matrix = eigenvectors.T @ eigenvectors
    identity = np.eye(orthogonality_matrix.shape[0])
    error = float(np.linalg.norm(orthogonality_matrix - identity, ord='fro'))

    return {
        'matrix': orthogonality_matrix,
        'error': error,
        'verified': error < 1e-8,
    }

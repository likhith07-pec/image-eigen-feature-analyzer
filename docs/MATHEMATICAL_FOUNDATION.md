# Mathematical Foundation

This file explains the mathematics actually used by the current application.

## 1. Image as a Matrix

An image can be represented as a matrix:

```text
A in R^(m x n)
```

Each entry `A[i, j]` represents the grayscale intensity of the pixel at row `i` and column `j`.

In this project, the image is resized to:

```text
A in R^(64 x 64)
```

So the image becomes a matrix with 64 rows and 64 columns.

## 2. Grayscale Normalization

The uploaded image is converted to grayscale using Pillow. A grayscale pixel normally has intensity from `0` to `255`.

The current implementation normalizes this by dividing by `255.0`:

```text
A[i, j] = grayscale_pixel_value / 255.0
```

Therefore:

```text
0 <= A[i, j] <= 1
```

This normalization is implemented in `image_processing.py` in `image_to_matrix`.

## 3. Matrix Rank

The rank of a matrix is:

```text
rank(A)
```

It represents the number of linearly independent rows or columns in the matrix.

In this project, `rank(A)` describes how many independent dimensions exist in the image matrix. A lower effective rank indicates that the image may be represented using fewer independent components.

The implementation uses:

```python
np.linalg.matrix_rank(matrix)
```

inside `matrix_analysis.py`.

Rank is not the same as selected `k`. Rank is a property of the matrix `A`; `k` is the number of selected dominant eigenvectors used for reconstruction.

## 4. Symmetric Matrix Construction

The project constructs:

```text
C = A^T A
```

For the current implementation:

```text
A = 64 x 64
A^T = 64 x 64
C = A^T A = 64 x 64
```

`C` is square because the number of columns of `A` determines the size of `A^T A`.

`C` is symmetric:

```text
C^T = (A^T A)^T = A^T (A^T)^T = A^T A = C
```

`C` is positive semidefinite because for any vector `x`:

```text
x^T C x = x^T A^T A x = (Ax)^T(Ax) = ||Ax||^2 >= 0
```

This construction is implemented in `eigen_analysis.py` in `calculate_covariance_matrix`.

## 5. Eigenvalue/Eigenvector Equation

The eigenvalue equation is:

```text
C v = lambda v
```

where:

- `C` is the symmetric matrix `A^T A`
- `v` is an eigenvector
- `lambda` is the eigenvalue corresponding to `v`

An eigenvector is a direction that remains on the same line when multiplied by `C`. The eigenvalue tells how strongly that direction is scaled.

The project uses:

```python
np.linalg.eigh(C)
```

because `C` is symmetric.

## 6. Eigenvalue Ordering

The eigenvalues are sorted in descending order:

```text
lambda_1 >= lambda_2 >= ... >= lambda_64
```

The eigenvectors are reordered in the same order. Dominant eigenvectors correspond to the largest eigenvalues because they represent directions with stronger contribution in the matrix structure.

This sorting happens in `eigen_analysis.py` in `calculate_eigenpairs`.

## 7. Orthogonality

For selected eigenvectors:

```text
V_k = [v_1 v_2 ... v_k]
```

orthogonality is checked using:

```text
V_k^T V_k ~= I_k
```

The project calculates orthogonality error as:

```text
||V_k^T V_k - I_k||_F
```

using NumPy's Frobenius norm. The project marks the result as verified if the error is less than `1e-8`.

This is implemented in `eigen_analysis.py` in `check_orthogonality`.

## 8. Component Selection

The user selects a value `k`. The project selects:

```text
V_k = [v_1 v_2 ... v_k]
```

where the selected eigenvectors are the first `k` columns after sorting by descending eigenvalue.

Implemented in `reconstruction.py` in `select_components`.

## 9. Projection

Projection is:

```text
P = A V_k
```

For the current `64 x 64` matrix:

```text
A = 64 x 64
V_k = 64 x k
P = 64 x k
```

Projection expresses the image matrix in the selected eigenvector subspace.

Implemented in `reconstruction.py` in `project_matrix`.

## 10. Reconstruction

Reconstruction is:

```text
A_k = P V_k^T
```

Since:

```text
P = 64 x k
V_k^T = k x 64
A_k = 64 x 64
```

`A_k` is the approximation of the original image matrix using `k` selected dominant eigen-components.

Implemented in `reconstruction.py` in `reconstruct_matrix`.

## 11. Frobenius Error

The absolute reconstruction error is:

```text
||A - A_k||_F
```

The Frobenius norm measures total difference between the original matrix and reconstructed matrix.

Implemented in `reconstruction.py` in `calculate_frobenius_error`.

## 12. Relative Reconstruction Error

The relative error is:

```text
||A - A_k||_F / ||A||_F x 100
```

The implementation calculates the ratio in `calculate_relative_error`, then `math_pipeline.py` multiplies by `100` for display as a percentage.

## 13. Relationship Between k and Reconstruction Quality

`k` controls how many dominant eigenvectors are used.

- Smaller `k`: fewer directions, stronger compression, larger error.
- Larger `k`: more directions, better reconstruction, smaller error.
- `k = 64`: all available eigenvectors for a `64 x 64` matrix are used, so reconstruction should be complete up to floating-point precision.

The current project compares:

```text
k = 1, 5, 10, 20, 32, 64
```

using `compare_components` in `reconstruction.py`.


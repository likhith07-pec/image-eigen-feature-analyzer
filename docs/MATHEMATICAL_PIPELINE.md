# Mathematical Pipeline

This file documents the exact computational pipeline currently implemented.

## Pipeline Summary

```text
IMAGE
  -> MATRIX
  -> RANK
  -> EIGEN ANALYSIS
  -> ORTHOGONALITY
  -> COMPONENT SELECTION
  -> PROJECTION
  -> RECONSTRUCTION
  -> ERROR
  -> COMPONENT COMPARISON
```

The coordinating function is:

```text
analyzer/math_pipeline.py -> analyze_image(image_path, requested_k)
```

## Stage 1 - Image -> Matrix

Input:

Uploaded image file path.

Mathematical operation:

Convert image to grayscale, resize to `64 x 64`, and normalize pixel values.

Formula:

```text
A[i, j] = grayscale_pixel(i, j) / 255.0
```

Output:

```text
A in R^(64 x 64)
0 <= A[i, j] <= 1
```

Implementation:

```text
analyzer/image_processing.py
image_to_matrix(image_path)
```

## Stage 2 - Matrix Analysis

Input:

```text
A
```

Mathematical operation:

Calculate matrix dimensions, rank, minimum, and maximum.

Formula:

```text
rank(A)
```

Output:

- Matrix shape
- Rank
- Minimum value
- Maximum value

Implementation:

```text
analyzer/matrix_analysis.py
analyze_matrix(matrix)
calculate_rank(matrix)
matrix_min(matrix)
matrix_max(matrix)
```

## Stage 3 - Eigen Analysis

Input:

```text
A
```

Mathematical operation:

Construct the symmetric matrix:

```text
C = A^T A
```

Then solve:

```text
C v = lambda v
```

using a symmetric eigensolver.

Dimensions:

```text
A = 64 x 64
C = A^T A = 64 x 64
```

Output:

- Covariance-like symmetric matrix `C`
- Eigenvalues sorted in descending order
- Eigenvectors sorted according to eigenvalue order

Implementation:

```text
analyzer/eigen_analysis.py
calculate_covariance_matrix(matrix)
calculate_eigenpairs(covariance_matrix)
calculate_eigen_features(matrix)
```

The eigensolver is:

```python
np.linalg.eigh(covariance_matrix)
```

## Stage 4 - Orthogonality

Input:

Selected eigenvector matrix `V_k`.

Mathematical operation:

Check whether selected eigenvectors are orthonormal.

Formula:

```text
V_k^T V_k ~= I_k
||V_k^T V_k - I_k||_F
```

Output:

- Orthogonality matrix
- Orthogonality error
- Verified / Not Verified status

Implementation:

```text
analyzer/eigen_analysis.py
check_orthogonality(eigenvectors)
```

## Stage 5 - Component Selection

Input:

- Sorted eigenvectors
- User-selected `k`

Mathematical operation:

Select the first `k` dominant eigenvectors:

```text
V_k = [v_1 v_2 ... v_k]
```

Dimensions:

```text
V_k = 64 x k
```

Output:

Selected `k` and selected eigenvector matrix `V_k`.

Implementation:

```text
analyzer/reconstruction.py
select_components(eigenvectors, requested_k, max_k)
```

## Stage 6 - Projection

Input:

```text
A, V_k
```

Mathematical operation:

```text
P = A V_k
```

Dimensions:

```text
A = 64 x 64
V_k = 64 x k
P = 64 x k
```

Output:

Projected representation `P`.

Implementation:

```text
analyzer/reconstruction.py
project_matrix(matrix, selected_eigenvectors)
```

## Stage 7 - Reconstruction

Input:

```text
P, V_k
```

Mathematical operation:

```text
A_k = P V_k^T
```

Dimensions:

```text
P = 64 x k
V_k^T = k x 64
A_k = 64 x 64
```

Output:

Reconstructed matrix `A_k`.

Implementation:

```text
analyzer/reconstruction.py
reconstruct_matrix(projection, selected_eigenvectors)
```

## Stage 8 - Error Analysis

Input:

```text
A, A_k
```

Mathematical operation:

Absolute error:

```text
E_absolute = ||A - A_k||_F
```

Relative error:

```text
E_relative = ||A - A_k||_F / ||A||_F x 100
```

Output:

- Frobenius error
- Relative reconstruction error percentage

Implementation:

```text
analyzer/reconstruction.py
calculate_frobenius_error(original_matrix, reconstructed_matrix)
calculate_relative_error(original_matrix, reconstructed_matrix)
```

The multiplication by `100` is done in `math_pipeline.py`.

## Stage 9 - Component Comparison

Input:

```text
A, eigenvectors, [1, 5, 10, 20, 32, 64]
```

Mathematical operation:

For each listed `k`:

```text
V_k = first k eigenvectors
P = A V_k
A_k = P V_k^T
error = ||A - A_k||_F
relative_error = error / ||A||_F x 100
```

Output:

Table rows containing:

- `k`
- Frobenius error
- Relative error percentage

Implementation:

```text
analyzer/reconstruction.py
compare_components(original_matrix, eigenvectors, component_list)
```

The list `[1, 5, 10, 20, 32, 64]` is defined in `math_pipeline.py` as `COMPONENT_LIST`.


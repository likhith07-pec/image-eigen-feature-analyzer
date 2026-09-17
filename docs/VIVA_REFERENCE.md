# Viva Reference

## 1. What is the aim of the project?

The aim is to demonstrate Linear Algebra concepts by converting an uploaded image into a matrix, analyzing rank and eigen-features, reconstructing the image using selected components, and calculating reconstruction error.

## 2. Why is an image represented as a matrix?

A grayscale image is a grid of pixel intensities, so it naturally becomes a matrix where each entry represents one pixel value.

## 3. What is matrix rank?

`rank(A)` is the number of linearly independent rows or columns of matrix `A`.

## 4. Why do we calculate A^T A?

The matrix `A^T A` is square and symmetric, which makes it suitable for stable eigenvalue/eigenvector analysis using `np.linalg.eigh`.

## 5. Why is A^T A symmetric?

Because:

```text
(A^T A)^T = A^T A
```

So `C = A^T A` is symmetric.

## 6. What is an eigenvalue?

An eigenvalue `lambda` is the scalar by which an eigenvector is scaled when multiplied by matrix `C`.

## 7. What is an eigenvector?

An eigenvector is a nonzero vector whose direction does not change under multiplication by `C`; only its magnitude changes.

## 8. What does C v = lambda v mean?

It means multiplying `C` by eigenvector `v` gives the same vector direction scaled by `lambda`.

## 9. Why are eigenvalues sorted?

They are sorted in descending order so the strongest or most dominant directions are selected first.

## 10. Why are dominant eigenvectors selected?

Dominant eigenvectors correspond to the largest eigenvalues and represent the most significant directions in the image matrix's vector space.

## 11. What is vector space in this project?

The vector space is the space formed by the columns and directions of the image matrix. Eigenvectors provide important directions in that space.

## 12. What is orthogonality?

Orthogonality means vectors are perpendicular or independent in direction. For selected eigenvectors, the project checks:

```text
V_k^T V_k ~= I_k
```

## 13. Why should eigenvectors be orthogonal?

Since `C = A^T A` is symmetric, its eigenvectors can form an orthonormal set.

## 14. What is V_k?

`V_k` is the matrix containing the first `k` dominant eigenvectors:

```text
V_k = [v_1 v_2 ... v_k]
```

## 15. What is projection?

Projection means representing the original matrix in the subspace formed by selected eigenvectors.

## 16. Why is P = A V_k?

Multiplying `A` by `V_k` gives the coordinates of the image matrix along the selected eigenvector directions.

## 17. What is reconstruction?

Reconstruction means rebuilding an approximation of the original image matrix from projected data.

## 18. Why is A_k = P V_k^T?

After projecting with `P = A V_k`, multiplying by `V_k^T` maps the projected representation back into the original matrix dimension.

## 19. What is the Frobenius norm?

The Frobenius norm is a matrix norm that measures total magnitude of all matrix entries. It is used here to measure total reconstruction difference.

## 20. How is reconstruction error calculated?

Absolute error:

```text
||A - A_k||_F
```

Relative error:

```text
||A - A_k||_F / ||A||_F x 100
```

## 21. What happens when k increases?

More eigenvectors are used, so more information is retained and reconstruction error generally decreases.

## 22. Why does k = 64 reconstruct the matrix completely or approximately?

For a `64 x 64` matrix, using all 64 eigenvectors uses the full available eigenvector basis, so reconstruction should match the original up to floating-point precision.

## 23. What is the role of NumPy?

NumPy performs matrix operations, rank calculation, eigenvalue/eigenvector calculation, projections, reconstructions, and norms.

## 24. Why is this not an AI/ML model?

The project does not train a model, make predictions, or classify images. It directly applies deterministic Linear Algebra formulas.

## 25. Why is Django used?

Django provides the web interface for uploading images, selecting `k`, and displaying mathematical results.

## 26. What happens when an image is uploaded?

The image is saved, converted to grayscale, resized to `64 x 64`, normalized to a matrix, analyzed mathematically, reconstructed, and displayed with error results.

## 27. What is the sequential computational process?

```text
Image
-> Matrix A
-> rank(A)
-> C = A^T A
-> eigenvalues/eigenvectors
-> select V_k
-> P = A V_k
-> A_k = P V_k^T
-> error
-> interpretation
```

## 28. What are the dimensions of A, V_k, P, and A_k?

For the current implementation:

```text
A = 64 x 64
V_k = 64 x k
P = 64 x k
A_k = 64 x 64
```

For `k = 10`:

```text
A = 64 x 64
V_10 = 64 x 10
P = 64 x 10
V_10^T = 10 x 64
A_10 = 64 x 64
```

## 29. How is orthogonality verified?

The project calculates:

```text
||V_k^T V_k - I_k||_F
```

If the error is below `1e-8`, it displays `Verified`.

## 30. What happens if the input image changes?

All matrix values, rank, eigenvalues, eigenvectors, projection, reconstruction, and errors are recalculated from the new uploaded image.


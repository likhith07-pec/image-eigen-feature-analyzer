# Data Flow

This file documents how data moves through the current implementation.

## Data Flow Table

| Stage | Input | Processing | Output |
|---|---|---|---|
| Upload | User-selected image | Django receives file through `ImageUploadForm` | Uploaded file object |
| Save image | Uploaded file | `FileSystemStorage` saves file to `media/uploads` | Image path |
| Image processing | Image path | Pillow grayscale conversion, resize to `64 x 64`, NumPy conversion, divide by `255.0` | Normalized matrix `A` |
| Matrix analysis | `A` | Shape, rank, min, max | Matrix metadata |
| Symmetric matrix | `A` | `C = A^T A` | `C` |
| Eigen analysis | `C` | `np.linalg.eigh(C)`, descending sort | Eigenvalues, eigenvectors |
| Component selection | Eigenvectors, requested `k` | Clamp k to valid range and select first k vectors | `V_k` |
| Projection | `A`, `V_k` | `P = A V_k` | Projection matrix `P` |
| Reconstruction | `P`, `V_k` | `A_k = P V_k^T` | Reconstructed matrix `A_k` |
| Orthogonality | `V_k` | `V_k^T V_k`, compare with identity | Orthogonality error/status |
| Error analysis | `A`, `A_k` | Frobenius and relative error | Error values |
| Component comparison | `A`, all eigenvectors | Repeat projection/reconstruction/error for k list | Comparison table |
| Visualization | Matrices/eigenvalues | Data URI conversion, rounded previews, canvas values | HTML-renderable values |
| Template rendering | Result dictionary | Django template interpolation | Final web page |

## Dimensions

Current image size:

```text
A = 64 x 64
```

Symmetric matrix:

```text
C = A^T A = 64 x 64
```

Selected eigenvectors:

```text
V_k = 64 x k
```

Projection:

```text
P = A V_k = (64 x 64)(64 x k) = 64 x k
```

Reconstruction:

```text
A_k = P V_k^T = (64 x k)(k x 64) = 64 x 64
```

## Django Upload-to-HTML Flow

1. Browser sends a POST request with uploaded image and selected `k`.
2. `analyzer/views.py` validates `ImageUploadForm`.
3. If a new image exists, it is saved with `FileSystemStorage` in `media/uploads`.
4. `views.py` builds an image path.
5. `views.py` calls `analyze_image(image_path, requested_k)` from `services.py`.
6. `services.py` points to `math_pipeline.py`.
7. `math_pipeline.py` performs the full mathematical sequence and returns a result dictionary.
8. `views.py` passes the result dictionary to `home.html`.
9. `home.html` displays formulas, values, images, previews, and tables.
10. `app.js` updates slider text and draws the eigenvalue chart from template-provided eigenvalues.

## Important Data Objects

| Name | Meaning | Current Dimension |
|---|---|---|
| `A` | Normalized grayscale image matrix | `64 x 64` |
| `C` | Symmetric matrix `A^T A` | `64 x 64` |
| `eigenvalues` | Sorted eigenvalues of `C` | 64 values |
| `eigenvectors` | Sorted eigenvectors of `C` | `64 x 64` |
| `V_k` | First k dominant eigenvectors | `64 x k` |
| `P` | Projection `A V_k` | `64 x k` |
| `A_k` | Reconstruction `P V_k^T` | `64 x 64` |
| `error_series` | Error table for fixed k values | rows for `1, 5, 10, 20, 32, 64` |


# Project Overview

## Project Title

Image Transformation and Eigen-Feature Analyzer

## Project Purpose

This project demonstrates core Linear Algebra concepts using an uploaded image as numerical data. The Django application is the interface; the central work is the mathematical pipeline that converts an image into a matrix, analyzes its rank and eigen-features, projects it into a selected eigenvector subspace, reconstructs it, and measures error.

This is not an AI or machine learning model. It does not train, predict, classify, or use PCA/sklearn. It is a Linear Algebra computational application.

## Problem Statement

Given an uploaded image, represent it as a matrix and use Linear Algebra operations to study how dominant eigen-components can reconstruct an approximation of the image.

## Aim

To build a web application that demonstrates:

- Matrix representation of an image
- Rank of a matrix
- Eigenvalues and eigenvectors
- Orthogonality
- Projection into a vector subspace
- Reconstruction from selected components
- Frobenius and relative reconstruction error

## Objectives

- Accept an uploaded image through a Django interface.
- Convert the image to grayscale.
- Resize it to `64 x 64`.
- Normalize pixel values to `[0, 1]`.
- Treat the image as a matrix `A`.
- Compute `rank(A)`.
- Construct `C = A^T A`.
- Compute eigenvalues and eigenvectors using a symmetric eigensolver.
- Sort eigenvalues and eigenvectors in descending eigenvalue order.
- Select the first `k` dominant eigenvectors.
- Compute projection `P = A V_k`.
- Compute reconstruction `A_k = P V_k^T`.
- Compute absolute Frobenius error and relative error percentage.
- Compare reconstruction error for `k = 1, 5, 10, 20, 32, 64`.

## Input

An image uploaded by the user through the web interface.

## Output

The application displays:

- Original normalized grayscale image
- Reconstructed image
- Matrix dimensions
- Matrix rank
- Pixel minimum and maximum
- Eigenvalue spectrum
- Eigenvector preview
- Orthogonality verification
- Projection preview
- Frobenius error
- Relative reconstruction error
- Component comparison table
- Mathematical interpretation

## Technologies Used

| Technology | Role |
|---|---|
| Django | Web application framework, routing, form handling, template rendering |
| HTML/CSS/JavaScript | Frontend interface and canvas-based eigenvalue chart |
| NumPy | Matrix operations, rank, eigenvalue/eigenvector calculation, norms |
| Pillow | Image loading, grayscale conversion, resizing, image generation for display |
| SQLite | Configured as Django default database; the current analyzer workflow does not use database models |
| Matplotlib | Not used in the current implementation |

## Django Role

Django handles:

- URL routing
- Image upload form
- Saving uploaded images under `media/uploads`
- Calling the mathematical pipeline
- Rendering calculated results into HTML templates

Django does not contain the core mathematical formulas in `views.py`.

## NumPy Role

NumPy performs the mathematical calculations:

- Matrix creation and manipulation
- Rank calculation
- `C = A^T A`
- Eigenvalue/eigenvector calculation using `np.linalg.eigh`
- Projection and reconstruction
- Frobenius norms

## Pillow Role

Pillow performs image operations:

- Open uploaded image
- Convert image to grayscale
- Resize image to `64 x 64`
- Convert matrix data back to image data for display

## Main Mathematical Concepts

- Matrix
- Rank
- Eigenvalues
- Eigenvectors
- Vector space
- Orthogonality
- Projection
- Reconstruction
- Error analysis

## Complete Processing Pipeline

```text
Image
  -> 64 x 64 normalized grayscale matrix A
  -> rank(A)
  -> C = A^T A
  -> eigenvalues and eigenvectors
  -> orthogonality verification
  -> select k dominant eigenvectors V_k
  -> projection P = A V_k
  -> reconstruction A_k = P V_k^T
  -> Frobenius and relative error
  -> component comparison
  -> mathematical interpretation
```

## Current Project Folder Structure

```text
maths/
|-- manage.py
|-- requirements.txt
|-- sample_upload_image.png
|-- db.sqlite3
|-- ImageEigenAnalyzer/
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- analyzer/
|   |-- __init__.py
|   |-- apps.py
|   |-- forms.py
|   |-- views.py
|   |-- urls.py
|   |-- services.py
|   |-- math_pipeline.py
|   |-- image_processing.py
|   |-- matrix_analysis.py
|   |-- eigen_analysis.py
|   |-- reconstruction.py
|   |-- visualization.py
|   |-- migrations/
|   |   `-- __init__.py
|   |-- templates/
|   |   `-- analyzer/
|   |       |-- home.html
|   |       `-- table_preview.html
|   |-- static/
|   |   `-- analyzer/
|   |       |-- styles.css
|   |       `-- app.js
|-- media/
|   `-- uploads/
|-- server.out.log
|-- server.err.log
`-- docs/
```

`db.sqlite3`, `media/uploads`, and server log files are runtime/development artifacts.

## Important Files and Purpose

| File | Purpose |
|---|---|
| `analyzer/views.py` | Handles upload form, saves image, calls `analyze_image`, sends result to template |
| `analyzer/services.py` | Re-exports `analyze_image` from `math_pipeline.py` |
| `analyzer/math_pipeline.py` | Coordinates the full mathematical sequence |
| `analyzer/image_processing.py` | Image to normalized `64 x 64` grayscale matrix |
| `analyzer/matrix_analysis.py` | Matrix size, rank, min, max |
| `analyzer/eigen_analysis.py` | `C = A^T A`, eigenpairs, orthogonality |
| `analyzer/reconstruction.py` | Component selection, projection, reconstruction, errors, comparison |
| `analyzer/visualization.py` | Matrix previews and image data URIs for display |
| `analyzer/templates/analyzer/home.html` | Main UI and mathematical result presentation |
| `analyzer/static/analyzer/styles.css` | Clean engineering/scientific styling |
| `analyzer/static/analyzer/app.js` | k-slider output and eigenvalue canvas chart |


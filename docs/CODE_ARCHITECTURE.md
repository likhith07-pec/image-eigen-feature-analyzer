# Code Architecture

This file documents the current code structure and responsibilities.

## High-Level Call Flow

```text
browser upload
  -> analyzer/views.py
  -> analyzer/services.py
  -> analyzer/math_pipeline.py
  -> analyzer/image_processing.py
  -> analyzer/matrix_analysis.py
  -> analyzer/eigen_analysis.py
  -> analyzer/reconstruction.py
  -> analyzer/visualization.py
  -> analyzer/templates/analyzer/home.html
```

## Django Project Files

### `manage.py`

Django command-line entry point.

Used to run commands such as:

```text
py -3.13 manage.py check
py -3.13 manage.py runserver
```

### `ImageEigenAnalyzer/settings.py`

Defines Django settings.

Important current settings:

- `INSTALLED_APPS` contains `analyzer` and `django.contrib.staticfiles`
- `ALLOWED_HOSTS` includes `127.0.0.1`, `localhost`, and `testserver`
- `MEDIA_ROOT = BASE_DIR / 'media'`
- `MEDIA_URL = 'media/'`
- SQLite is configured, but the current analyzer workflow does not define or use data models

### `ImageEigenAnalyzer/urls.py`

Routes the root URL to the analyzer app:

```python
path('', include('analyzer.urls'))
```

It also serves media files in development using `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`.

## Analyzer App Files

### `analyzer/urls.py`

Maps the root analyzer route to:

```text
views.analyzer_home
```

### `analyzer/views.py`

Handles web/UI logic:

- Creates `ImageUploadForm`
- Receives POST data and uploaded files
- Saves uploaded images to `media/uploads`
- Reads the requested `k`
- Calls `analyze_image(image_path, requested_k)`
- Sends result data to `home.html`

It does not implement the mathematical formulas directly.

### `analyzer/forms.py`

Defines:

```text
ImageUploadForm
```

Fields:

- `image`: optional image upload field
- `k`: optional integer field, minimum value `1`, initial value `8`
- `image_name`: hidden field used to remember the uploaded image name

### `analyzer/services.py`

Contains:

```python
from .math_pipeline import analyze_image
```

It is a small compatibility/service layer so views import from `services.py` instead of directly from the pipeline.

### `analyzer/math_pipeline.py`

Coordinates the complete mathematical process in:

```text
analyze_image(image_path, requested_k)
```

It calls:

- `image_to_matrix`
- `analyze_matrix`
- `calculate_eigen_features`
- `select_components`
- `project_matrix`
- `reconstruct_matrix`
- `check_orthogonality`
- `calculate_frobenius_error`
- `calculate_relative_error`
- `compare_components`
- visualization helper functions

It also prepares values for the template, such as:

- shapes
- matrix range
- eigenvalue checks
- image data URIs
- previews
- error table
- displayed formulas/dimensions

### `analyzer/image_processing.py`

Contains:

```text
IMAGE_SIZE = (64, 64)
image_to_matrix(image_path)
```

Responsibilities:

- Open image using Pillow
- Convert to grayscale using `.convert('L')`
- Resize to `64 x 64`
- Convert to NumPy `float64`
- Normalize by dividing by `255.0`

### `analyzer/matrix_analysis.py`

Contains:

- `matrix_size(matrix)`
- `calculate_rank(matrix)`
- `matrix_min(matrix)`
- `matrix_max(matrix)`
- `analyze_matrix(matrix)`

Responsibilities:

- Matrix dimensions
- Matrix rank using `np.linalg.matrix_rank`
- Matrix minimum and maximum

### `analyzer/eigen_analysis.py`

Contains:

- `calculate_covariance_matrix(matrix)`
- `calculate_eigenpairs(covariance_matrix)`
- `calculate_eigen_features(matrix)`
- `check_orthogonality(eigenvectors)`

Responsibilities:

- Construct `C = A^T A`
- Calculate eigenvalues and eigenvectors using `np.linalg.eigh`
- Sort eigenvalues/eigenvectors in descending order
- Check `V_k^T V_k ~= I_k`
- Calculate orthogonality error

### `analyzer/reconstruction.py`

Contains:

- `select_components(eigenvectors, requested_k, max_k)`
- `project_matrix(matrix, selected_eigenvectors)`
- `reconstruct_matrix(projection, selected_eigenvectors)`
- `calculate_frobenius_error(original_matrix, reconstructed_matrix)`
- `calculate_relative_error(original_matrix, reconstructed_matrix)`
- `compare_components(original_matrix, eigenvectors, component_list)`

Responsibilities:

- Select dominant eigenvectors
- Compute projection `P = A V_k`
- Compute reconstruction `A_k = P V_k^T`
- Compute reconstruction errors
- Compare multiple k values

### `analyzer/visualization.py`

Contains:

- `matrix_to_data_uri(matrix)`
- `matrix_preview(matrix, rows=8, cols=8)`
- `eigenvalue_preview(eigenvalues, count=20)`

Responsibilities:

- Convert normalized matrices to displayable PNG data URIs
- Prepare rounded matrix previews for HTML tables
- Prepare eigenvalue values for display/charting

## Templates

### `analyzer/templates/analyzer/home.html`

Main page template.

Displays:

- Project heading
- Sequential workflow
- Upload form
- k slider
- Summary result cards
- Original and reconstructed images
- Mathematical formula sections
- Eigenvalue/eigenvector analysis
- Eigenvector preview
- Component comparison
- Eigenvalue spectrum canvas
- Matrix/projection previews
- Orthogonality verification

### `analyzer/templates/analyzer/table_preview.html`

Reusable table partial for matrix-like preview data.

## Static Files

### `analyzer/static/analyzer/styles.css`

Defines the visual style:

- Light background
- Dark readable text
- Subtle borders
- Academic/scientific cards
- Responsive layout

### `analyzer/static/analyzer/app.js`

Handles:

- Updating the visible k value beside the slider
- Drawing the eigenvalue spectrum on an HTML canvas

The eigenvalue chart is implemented with vanilla JavaScript canvas, not Matplotlib.


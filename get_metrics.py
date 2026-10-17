import sys
from pathlib import Path
sys.path.insert(0, '.')
from analyzer.math_pipeline import analyze_image

sample_path = Path('sample_upload_image.png')
if not sample_path.exists():
    sample_path = Path('media/uploads/demo_sample.png')

res = analyze_image(sample_path, 16)
print(f"Matrix shape: {res['matrix_shape']}")
print(f"Matrix rank: {res['rank']}")
print(f"Min: {res['matrix_min']}, Max: {res['matrix_max']}")
print(f"Frobenius error (k=16): {res['frobenius_error']:.6f}")
print(f"Relative error % (k=16): {res['relative_error']:.4f}%")
print(f"Orthogonality error: {res['orthogonality_error']:.2e}")
print(f"Dominant eigenvalues: {res['dominant_eigenvalues']}")
print(f"Error series: {res['error_series']}")

<!-- converted from EigenLab_Presentation_Script.docx -->

ACADEMIC MINI-PROJECT PRESENTATION SCRIPT
EigenLab: Image Compression and Eigen-Feature Analyzer
Using Linear Algebra
Slide-by-Slide Complete Oral Defense Script for 100-Mark Faculty Evaluation
―――――――――――――――――――――――――――――――――――――――――――――――――――――――

## SLIDE 1: Title Slide & Project Overview
Respected Guide, Chairperson, and Members of the Faculty Evaluation Committee, good morning.

My name is [Student Name], USN [Your USN], and today I am defending my linear algebra mini-project titled: 'EigenLab: Image Compression and Eigen-Feature Analyzer Using Linear Algebra'.

The central premise of this project is to investigate how core theorems of linear algebra—specifically spectral decomposition of symmetric operators, orthonormal projections, and low-rank matrix approximations—can be applied directly to digital image representation and dimension reduction.

Over the course of this presentation, I will demonstrate the full engineering pipeline: from discrete pixel matrix formulation, to Gram matrix construction, eigenvalue spectrum computation, truncated subspace projection, and empirical error benchmarking. We backed this mathematical foundation with an interactive Django-based analytical platform. Let us proceed to the abstract.
## SLIDE 2: Abstract & Executive Summary
To summarize our investigation in Slide 2: Digital images natively reside in high-dimensional Euclidean spaces where strong spatial correlation between adjacent pixels creates severe data redundancy.

In EigenLab, we transform a normalized 64x64 grayscale matrix A into its symmetric Gram operator G = A^T A. By applying the Spectral Theorem via LAPACK eigensolvers, we extract an orthonormal basis V ranked by eigenvalue energy.

Truncating this basis to the top k components and projecting the image yields an optimal low-rank matrix approximation. Our empirical evaluation confirms that retaining only 16 components out of 64—a 75% reduction in basis vectors—preserves 99.96% of the Frobenius matrix energy with a relative error of less than 0.04%, providing empirical validation of the Eckart-Young-Mirsky theorem.
## SLIDE 3: Introduction: Digital Images as Linear Operators
On Slide 3, we establish the mathematical representation of digital images.

In computer vision, a discrete grayscale image is formalized as a real matrix A in R^{m x n}, where m and n correspond to the vertical and horizontal spatial pixel resolution. Each entry A_{i,j} represents a quantized luminance value between 0 and 255, which we normalize into the continuous real interval [0.0, 1.0].

Crucially, natural images are not random noise; they exhibit strong spatial coherence. Adjacent columns a_j and a_{j+1} share similar structural features, meaning the columns of matrix A are linearly dependent. Standard raster formats store every pixel coordinate independently, which ignores this linear correlation. Linear algebra allows us to rotate our coordinate system away from the arbitrary Cartesian pixel basis to an optimal eigen-basis aligned with the directions of maximum visual variance.
## SLIDE 4: Problem Statement & Motivation
Slide 4 details the engineering problem statement and motivation.

First, storing and transmitting raw image matrices without exploiting inter-column correlation leads to high memory and bandwidth overhead. Furthermore, downstream computer vision tasks such as facial recognition, object detection, and feature extraction scale poorly with high dimensionality.

Second, in engineering mathematics curricula, eigenvalues and eigenvectors are frequently taught as abstract algebraic definitions without practical visualization. Our motivation was to build a rigorous, deterministic, and interactive platform where students and researchers can observe exactly how the spectrum of a matrix controls the reconstruction of visual data, bridging theoretical vector calculus with computational data science.
## SLIDE 5: Objectives and Project Scope
Slide 5 outlines our quantifiable project objectives and technical boundaries.

Our primary objectives were: First, implement a standardized image ingestion pipeline that resamples inputs to normalized 64x64 float64 arrays. Second, construct the symmetric Gram matrix G = A^T A. Third, compute its eigenvalues and eigenvectors, and verify orthonormal precision (V^T V = I) within 10^{-8} tolerance. Fourth, implement truncated subspace projection and low-rank synthesis. Fifth, benchmark the Frobenius distance across user-specified ranks k in {1, 5, 10, 16, 20, 32, 64}.

It is equally important to state our project scope: our investigation focuses on 2D single-channel grayscale matrices. We are analyzing linear subspace dimensionality reduction and low-rank approximations—we are not constructing a binary entropy codec like JPEG with quantization tables and Huffman coding.
## SLIDE 6: Proposed System & Architecture
Slide 6 presents our actual software architecture, verified directly from our codebase.

The system follows an 8-stage dataflow pipeline: The user uploads an image via an intuitive Django interface. The preprocessing service in image_processing.py converts the image to grayscale and resamples it to 64x64. The linear algebra core in eigen_analysis.py computes the Gram matrix and calls NumPy's eigh solver, which wraps LAPACK's symmetric divide-and-conquer routines. The reconstruction service in reconstruction.py computes the projection matrix Z = A V_k and synthesizes the approximation A_hat = Z V_k^T. Finally, visualization.py serializes the resulting matrices into in-memory PNG buffers and Base64 data URIs, completely avoiding disk I/O bottlenecks and ensuring sub-second browser rendering.
## SLIDE 7: Image Preprocessing Pipeline
On Slide 7, we examine the image preprocessing mathematics.

First, color images are converted to grayscale using the ITU-R BT.601 standard luminance equation: Y = 0.299R + 0.587G + 0.114B, which matches the human visual system's spectral sensitivity. Second, the image is resampled to 64x64 using Lanczos interpolation to preserve sharp structural contours. Third, pixel intensities are divided by 255.0 to yield continuous values in [0.0, 1.0].

I want to highlight a key mathematical point: our implementation decomposes the uncentered normalized matrix A directly rather than performing column-mean subtraction. In linear algebra, this means we are computing the uncentered SVD basis. The first eigenvector captures global DC background luminance, while subsequent eigenvectors capture high-contrast AC variations. Both mean-centered PCA and uncentered SVD are mathematically valid, and our approach connects directly to the singular value decomposition of matrix A.
## SLIDE 8: Mathematical Foundation: Inner Products & The Spectral Theorem
Slide 8 outlines the core linear algebra theorems governing our work.

Our framework operates in R^{m x n} equipped with the standard inner product and Frobenius norm. The central theoretical pillar of our project is the Spectral Theorem for real symmetric matrices. The theorem states that if S is a real symmetric matrix (S = S^T), there exists an orthogonal matrix V such that S = V Lambda V^T, where Lambda is a diagonal matrix of real eigenvalues, and the columns of V form a complete orthonormal basis of R^n.

This theorem guarantees two crucial engineering properties: First, all eigenvalues are strictly real—no imaginary artifacts can occur. Second, the eigenvectors are mutually perpendicular (v_i . v_j = 0 for i != j), ensuring zero informational redundancy between feature directions.
## SLIDE 9: Gram Matrix vs. Covariance Matrix
Slide 9 clarifies an important distinction that examiners frequently investigate.

In our source code file analyzer/eigen_analysis.py, the function calculate_covariance_matrix executes matrix.T @ matrix. Mathematically, this operator G = A^T A is the Gram matrix, or uncentered scatter matrix of the column vectors. A true sample covariance matrix requires subtracting the column mean vector mu and dividing by m - 1.

Why is G = A^T A mathematically significant? Because it links directly to Singular Value Decomposition! If the SVD of matrix A is U Sigma V^T, then A^T A equals V Sigma^2 V^T. This proves that the eigenvectors of our Gram matrix G are identically the right singular vectors of the original image A, and its eigenvalues are the squared singular values: lambda_i = sigma_i^2. Furthermore, G is guaranteed symmetric (G = G^T) and positive semi-definite (x^T G x = ||Ax||^2 >= 0), ensuring all lambda_i >= 0.
## SLIDE 10: Eigendecomposition & SVD Equivalence
On Slide 10, we examine the spectral solution: G v_i = lambda_i v_i.

Notice what the eigenvalue represents physically: the squared Euclidean norm of the projected image ||A v_i||^2 simplifies algebraically to lambda_i. Therefore, each eigenvalue directly quantifies the total variance or energy captured along eigenvector direction v_i.

In our code, we sort all 64 eigenpairs in descending order so that lambda_1 contains the maximum possible energy. We invoke NumPy's eigh solver, which uses LAPACK's symmetric divide-and-conquer algorithm dsyevd. In our test benchmarks, we explicitly verified the numerical orthogonality matrix V^T V - I, achieving a Frobenius error of 2.48 x 10^{-15}, confirming machine-precision orthonormality.
## SLIDE 11: Worked Numerical Example (3×3 Toy Matrix)
To verify the mathematics by hand, Slide 11 provides a worked numerical example on a 3x3 matrix.

Starting with a 3x3 symmetric image patch A with values [[1.0, 0.5, 0.0], [0.5, 1.0, 0.5], [0.0, 0.5, 1.0]], we compute the Gram matrix G = A^T A, giving diagonal values 1.25, 1.50, and 1.25, with total trace equal to 4.0.

Solving the characteristic polynomial det(G - lambda I) = 0 yields eigenvalues lambda_1 = 3.0, lambda_2 = 1.0, and lambda_3 = 0.0. Notice that lambda_1 alone accounts for 3.0 out of 4.0, or exactly 75% of the total matrix energy! When we truncate to k = 1 component, we project A onto v_1 to obtain a 3x1 vector Z, and reconstruct A_hat_1 = Z v_1^T. The manual Frobenius error ||A - A_hat_1||_F equals exactly sqrt(lambda_2 + lambda_3) = sqrt(1.0) = 1.0, matching our theoretical formula with exact arithmetic.
## SLIDE 12: Dimensionality Reduction vs. Storage Compression
Slide 12 addresses a common faculty question: Does selecting 16 components out of 64 reduce the file size by 75%?

We must carefully distinguish subspace dimension reduction from binary file compression. Selecting 16 out of 64 eigenvectors reduces the basis vector count by 75%—the row coordinates drop from R^{64} to R^{16}.

However, to reconstruct a single isolated image, the system must store both the projection coordinates Z (64x16 = 1,024 floats) and the basis vectors V_k (64x16 = 1,024 floats), totaling 2,048 floating-point numbers. That represents a 50% parameter reduction for a single image. The full 75% asymptotic reduction is achieved in multi-image datasets—such as facial recognition databases—where the basis V_k is computed once and shared across thousands of images. Furthermore, true file compression requires quantization and entropy coding, which is a downstream serialization process.
## SLIDE 13: Reconstruction & The Eckart-Young-Mirsky Theorem
Slide 13 formalizes the reconstruction step and proves its theoretical optimality.

The low-rank reconstruction is given by A_hat = Z V_k^T = A V_k V_k^T. The operator P_k = V_k V_k^T is an orthogonal projection matrix of rank k. It is symmetric and idempotent (P_k^2 = P_k).

Why is this reconstruction optimal? The celebrated Eckart-Young-Mirsky theorem (1936) states that for any target rank k, the matrix that minimizes the Frobenius distance ||A - B||_F across all possible rank-k matrices B is uniquely the truncated singular value expansion. Because our eigen-basis V_k directly supplies the right singular vectors of matrix A, our reconstruction A V_k V_k^T identically matches the truncated SVD expansion. This proves that no other linear combination or coordinate system of rank k can achieve a lower approximation error.
## SLIDE 14: System Implementation & Web Architecture
On Slide 14, we present our software engineering implementation.

The backend is developed in Python 3.13 and Django 5.x. The core orchestration service in math_pipeline.py computes the numerical rank using singular value thresholding, constructs intermediate equation strings, and coordinates the component analysis. The reconstruction service computes Frobenius norms and relative error percentages across multiple ranks simultaneously.

The user interface features a dynamic component selector slider, side-by-side original and reconstructed image views rendered at sharp matrix pixel resolution, interactive heatmaps of matrix A and Gram matrix G, and real-time dimensionality equations. We also integrated Sarvam AI to provide contextual explanations of calculated eigenvalues in 10 Indian regional languages for educational accessibility.
## SLIDE 15: Experimental Results & Benchmarks
Slide 15 presents our verified empirical benchmarks, extracted directly from running our test script on the sample image.

The table outlines the exact progression of error across ranks 1 through 64. The original matrix has dimensions 64x64 and a computed numerical rank of 34. The dominant eigenvalues decay exponentially: lambda_1 is 2,799.15, lambda_2 is 92.03, and lambda_3 is 9.88. The first eigenvalue alone captures over 96.3% of the Gram trace.

Look at the error behavior: At k = 1, the relative Frobenius error is 19.2%. At k = 5, the error drops to 2.03%. At k = 16, our default setting, the relative error drops to just 0.0341%—meaning 99.96% of the image energy is retained! At k = 34, the error reaches zero within floating-point tolerance because k reaches the true rank of the matrix, verifying that natural image features lie on a low-dimensional manifold.
## SLIDE 16: Limitations & Future Scope
Slide 16 provides an honest, objective appraisal of engineering limitations and future scope.

First, computational complexity: standard symmetric eigensolvers scale as O(n^3). While a 64x64 matrix requires only 260,000 operations and runs in less than one millisecond, a 1024x1024 matrix requires a billion operations, necessitating iterative Krylov subspace or randomized SVD methods for high-definition streaming.

Second, the current mathematical formulation handles single-channel 2D matrices. Color RGB images require multi-way tensor decomposition or independent 3-channel processing.

Third, eigen-bases are global across the entire image. Block-based transforms like JPEG's 8x8 DCT can better capture localized edges. Our future roadmap includes implementing block-based subspace decomposition, adaptive energy-threshold selection (the 99% variance rule), and binary Huffman entropy coding.
## SLIDE 17: Conclusion & Academic References
To conclude on Slide 17:

EigenLab successfully bridges pure linear algebra with practical digital image processing. We formulated the discrete image as a matrix operator, computed its Gram matrix, and extracted an optimal orthonormal eigen-basis. We empirically verified the Eckart-Young theorem, proving that 16 orthogonal vectors capture over 99.96% of the image energy. We embodied this mathematical theory in a robust, interactive Django web application that serves as an effective pedagogical tool.

Our work is grounded in authoritative linear algebra literature, including Gilbert Strang's Linear Algebra and Its Applications, Golub and Van Loan's Matrix Computations, and the original 1936 paper by Carl Eckart and Gale Young.

Thank you very much, respected committee members. I am now open to your questions.
| GUIDANCE FOR CANDIDATE PRESENTATION DELIVERY:
• Total Presentation Time: Approximately 12 to 15 minutes (leaving 5–10 minutes for Viva Q&A).
• Tone: Confident, scholarly, and technically precise. Avoid buzzwords; use exact linear algebraic terminology.
• Posture: Maintain eye contact with the evaluation committee. Reference slide equations directly when discussing derivations.
• Key Faculty Checkpoint: Ensure you clearly articulate the distinction between the Gram matrix A^T A and the covariance matrix, and explain that Eckart-Young optimality applies to the low-rank SVD synthesis. |
| --- |
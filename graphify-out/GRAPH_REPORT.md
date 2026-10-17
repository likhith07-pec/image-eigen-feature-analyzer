# Graph Report - maths  (2026-10-14)

## Corpus Check
- 38 files · ~49,013 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 209 nodes · 248 edges · 30 communities (16 shown, 14 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `443eff55`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- math_pipeline.py
- views.py
- analyze_matrix
- Viva Reference
- UI and Features
- app.js
- AnalyzerConfig
- What Each Test Proves
- create_presentation.py
- main
- asgi.py
- settings.py
- ImageEigenAnalyzer/urls.py
- wsgi.py
- Code Architecture
- Mathematical Foundation
- Mathematical Pipeline
- Project Overview
- Sample Upload Image
- Data Flow
- rules/graphify.md
- workflows/graphify.md
- EigenLab_Presentation_Script_ab86610b.md
- EigenLab_Viva_Questions_81cc65bd.md
- build_documents.py
- build_presentation.py

## God Nodes (most connected - your core abstractions)
1. `Viva Reference` - 31 edges
2. `analyze_image()` - 17 edges
3. `UI and Features` - 16 edges
4. `What Each Test Proves` - 13 edges
5. `sendQuestion()` - 9 edges
6. `analyze_matrix()` - 7 edges
7. `generate_mathematical_insight()` - 6 edges
8. `ask_sarvam_question()` - 6 edges
9. `translate_sarvam_text()` - 6 edges
10. `Testing and Verification` - 6 edges

## Surprising Connections (you probably didn't know these)
- `analyzer_home()` --calls--> `analyze_image()`  [INFERRED]
  analyzer/views.py → analyzer/math_pipeline.py
- `analyze_image()` --calls--> `analyze_matrix()`  [EXTRACTED]
  analyzer/math_pipeline.py → analyzer/matrix_analysis.py
- `api_sarvam_chat()` --calls--> `ask_sarvam_question()`  [EXTRACTED]
  analyzer/views.py → analyzer/sarvam_ai.py
- `api_sarvam_translate()` --calls--> `translate_sarvam_text()`  [EXTRACTED]
  analyzer/views.py → analyzer/sarvam_ai.py
- `analyze_image()` --calls--> `calculate_eigen_features()`  [EXTRACTED]
  analyzer/math_pipeline.py → analyzer/eigen_analysis.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Project Documentation** — docs_code_architecture, docs_mathematical_foundation, docs_mathematical_pipeline, docs_project_overview [EXTRACTED 1.00]

## Communities (30 total, 14 thin omitted)

### Community 0 - "math_pipeline.py"
Cohesion: 0.23
Nodes (15): calculate_covariance_matrix(), calculate_eigen_features(), calculate_eigenpairs(), check_orthogonality(), image_to_matrix(), analyze_image(), calculate_frobenius_error(), calculate_relative_error() (+7 more)

### Community 1 - "views.py"
Cohesion: 0.20
Nodes (13): ImageUploadForm, ask_sarvam_question(), clean_sarvam_response(), generate_mathematical_insight(), get_sarvam_api_key(), Answers a student's custom question regarding their analyzed image     in the re, Translates mathematical synthesis text into an Indian language     using Sarvam, Removes thinking tags <think>...</think> and markdown code fences. (+5 more)

### Community 2 - "analyze_matrix"
Cohesion: 0.60
Nodes (5): analyze_matrix(), calculate_rank(), matrix_max(), matrix_min(), matrix_size()

### Community 3 - "Viva Reference"
Cohesion: 0.06
Nodes (31): 10. Why are dominant eigenvectors selected?, 11. What is vector space in this project?, 12. What is orthogonality?, 13. Why should eigenvectors be orthogonal?, 14. What is V_k?, 15. What is projection?, 16. Why is P = A V_k?, 17. What is reconstruction? (+23 more)

### Community 4 - "UI and Features"
Cohesion: 0.12
Nodes (16): Component Comparison, Eigenvalue Spectrum, Eigenvector Preview, k / Component Selector, Mathematical Formula Sections, Mathematical Interpretation, Matrix Preview, Original and Reconstructed Images (+8 more)

### Community 5 - "app.js"
Cohesion: 0.20
Nodes (12): appendBotMessage(), appendSystemNotice(), appendUserMessage(), escHtml(), formatBotContent(), getAnalysisContext(), getTimeStr(), removeTypingIndicators() (+4 more)

### Community 7 - "What Each Test Proves"
Cohesion: 0.10
Nodes (20): C = A^T A Verification, Component Comparison Test Result, Component Comparison Verification, Django System Check, Eigenvalue Nonnegative Tolerance Check, Eigenvalue Sorting Verification, Image Upload Test, Known Limitations and Edge Cases (+12 more)

### Community 9 - "main"
Cohesion: 0.50
Nodes (3): main(), Django's command-line utility for administrative tasks., Run administrative tasks.

### Community 23 - "Data Flow"
Cohesion: 0.33
Nodes (5): Data Flow, Data Flow Table, Dimensions, Django Upload-to-HTML Flow, Important Data Objects

### Community 26 - "EigenLab_Presentation_Script_ab86610b.md"
Cohesion: 0.11
Nodes (17): SLIDE 10: Eigendecomposition & SVD Equivalence, SLIDE 11: Worked Numerical Example (3×3 Toy Matrix), SLIDE 12: Dimensionality Reduction vs. Storage Compression, SLIDE 13: Reconstruction & The Eckart-Young-Mirsky Theorem, SLIDE 14: System Implementation & Web Architecture, SLIDE 15: Experimental Results & Benchmarks, SLIDE 16: Limitations & Future Scope, SLIDE 17: Conclusion & Academic References (+9 more)

### Community 27 - "EigenLab_Viva_Questions_81cc65bd.md"
Cohesion: 0.18
Nodes (10): Q10: Why did you build a web application instead of writing a standalone Python script?, Q1: What is the exact mathematical difference between the Gram matrix and the covariance matrix in your project?, Q2: Why do you decompose the Gram matrix G = A^T A instead of decomposing image matrix A directly?, Q3: Does selecting 16 out of 64 components reduce the actual file size by 75%?, Q4: State the Eckart-Young-Mirsky Theorem and explain why it applies to your project., Q5: Why did you use np.linalg.eigh instead of np.linalg.eig in NumPy?, Q6: Why does the reconstructed image appear slightly smoothed or blurred at low k values?, Q7: What is the physical and geometric interpretation of an eigenvalue and eigenvector in image processing? (+2 more)

### Community 28 - "build_documents.py"
Cohesion: 0.47
Nodes (4): create_script_document(), build_documents.py Generates: 1. EigenLab_Presentation_Script.docx (Slide-by-sli, set_cell_background(), set_cell_margins()

## Knowledge Gaps
- **100 isolated node(s):** `graphify`, `Workflow: graphify`, `Data Flow Table`, `Dimensions`, `Django Upload-to-HTML Flow` (+95 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `analyze_image()` connect `math_pipeline.py` to `views.py`, `analyze_matrix`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `analyzer_home()` connect `views.py` to `math_pipeline.py`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **What connects `graphify`, `Workflow: graphify`, `Data Flow Table` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Viva Reference` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._
- **Should `UI and Features` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `What Each Test Proves` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `EigenLab_Presentation_Script_ab86610b.md` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
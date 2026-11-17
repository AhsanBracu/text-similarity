# Document Similarity Detection Using Shingling and MinHash

## 1. Overview

This project implements document similarity detection using character-based shingling, Jaccard similarity, and MinHash signatures.

The implementation is written in Python and evaluates similarity between tweets from the **Health News in Twitter** dataset.

Four main components are implemented:

1. **Shingling:** Generate unique character-based k-shingles and represent documents as sorted sets of hashed integers.
2. **CompareSets:** Calculate exact Jaccard similarity between hashed-shingle sets.
3. **MinHashing:** Generate fixed-length MinHash signatures using multiple hash functions.
4. **CompareSignatures:** Estimate Jaccard similarity by calculating the fraction of matching signature components.

The project also includes unit tests and scalability experiments.

## 2. Project Structure

```text
document-similarity/
├── src/
│   ├── __init__.py
│   ├── shingling.py
│   ├── compare_sets.py
│   ├── minhashing.py
│   ├── compare_signatures.py
│   ├── data_loader.py
│   └── normalization.py
├── tests/
│   └── test_similarity.py
├── data/
│   └── documents/       # Dataset files (not submitted)
├── main.py
├── benchmark.py
├── Makefile
├── README.md
└── report.pdf
```

## 3. Dataset

**Dataset:** Health News in Twitter  
**Source:** UCI Machine Learning Repository  
**Dataset URL:** https://archive.ics.uci.edu/dataset/438/health+news+in+twitter

### Download Instructions

1. Open the dataset URL.
2. Download the dataset archive.
3. Extract the `.txt` files into `data/documents/`.
4. Ensure the extracted files are directly accessible in this folder.

Each dataset line represents one tweet:

```text
tweet_id|timestamp|tweet_text
```

The implementation uses the tweet ID as the document identifier and the tweet text as the document content. Timestamps are excluded from similarity calculations.

Because the source files contain mixed text encodings, the loader attempts UTF-8 decoding first and falls back to Windows-1252 (CP1252) when necessary.

**Important:** Dataset files are not included in the submission ZIP.

## 4. Requirements

- Python 3.10 or later (recommended)
- No third-party Python packages required
- Make (optional, for running Makefile commands)

The implementation uses Python's standard library, including `hashlib`, `random`, `itertools`, `time`, `statistics`, `pathlib`, and `unittest`.

## 5. Running the Application

From the project root:

```bash
python3 main.py
```

Alternatively, if using the Makefile:

```bash
make run
```

The application loads tweets, computes hashed shingles and MinHash signatures, and compares document pairs.

It displays the five pairs with the highest exact Jaccard similarity and identifies pairs satisfying the chosen similarity threshold.

### Experiment Configuration

| Parameter | Value | Description |
|---|---|---|
| `k` | 5 | Characters per shingle |
| `n` | 100 | Number of MinHash functions and signature components |
| `s` | 0.8 | Minimum exact Jaccard similarity for similar documents |
| Dataset sizes | 10, 100, 1,000 | Number of tweets evaluated |
| Random seed | 42 | Reproducible MinHash function generation |

These parameters are currently configured in the Python source code rather than through command-line arguments.

## 6. Implementation Details

### Shingling

Each document is divided into overlapping character shingles of length `k=5`.

Each unique textual shingle is hashed using BLAKE2b with a four-byte digest, producing a 32-bit integer.

The resulting unique integer hashes are returned in sorted order.

### Exact Jaccard Similarity

For two hashed-shingle sets A and B, similarity is computed as:

\[
J(A,B)=\frac{|A\cap B|}{|A\cup B|}
\]

A result of 1.0 indicates identical shingle sets; 0.0 indicates no common hashed shingles.

### MinHashing

A MinHash signature is generated using `n=100` hash functions of the form:

\[
h_i(x)=(a_i x+b_i)\bmod p
\]

where \(p=4294967311\).

For each function, the minimum hash value across the document's shingles is stored in the signature.

The same hash functions are reused for every document.

### Signature Similarity

Two signatures are compared position by position:

\[
\widehat J(A,B)=\frac{\text{Number of matching positions}}{n}
\]

This produces an approximation of the exact Jaccard similarity.

### Similarity Threshold

Two documents are classified as similar when their exact Jaccard similarity is at least:

\[
s=0.8
\]

## 7. Benchmarking

Run:

```bash
python3 benchmark.py
```

Or:

```bash
make benchmark
```

Each dataset-size experiment is repeated three times, and median execution times are reported.

The benchmark measures shingling, MinHash generation, exact Jaccard comparisons, MinHash signature comparisons, and mean absolute estimation error.

### Benchmark Results

| Metric | 10 documents | 100 documents | 1,000 documents |
|---|---:|---:|---:|
| Shingling time | 0.0011 s | 0.0091 s | 0.0926 s |
| MinHash generation time | 0.0210 s | 0.1744 s | 1.6649 s |
| Exact Jaccard comparison time | 0.0004 s | 0.0315 s | 2.9902 s |
| MinHash comparison time | 0.0001 s | 0.0102 s | 1.0938 s |
| Mean absolute error | 0.0163 | 0.0182 | 0.0165 |
| Total document pairs | 45 | 4,950 | 499,500 |

### Threshold-Based Similarity Results

Using `s=0.8`:

| Documents | Total pairs | Similar pairs |
|---|---:|---:|
| 10 | 45 | 0 |
| 100 | 4,950 | 2 |
| 1,000 | 499,500 | 7 |

The results demonstrate that MinHash signature comparison is faster than exact Jaccard comparison for this dataset.

However, both methods still compare every possible document pair, resulting in quadratic growth in comparison count.

## 8. Unit Tests

Run all tests:

```bash
python3 -m unittest discover -s tests -v
```

Or:

```bash
make test
```

The project contains 12 unit tests covering:

- Shingle generation and uniqueness
- Sorted hashed-shingle representation
- Exact Jaccard similarity
- Identical, disjoint, and empty sets
- MinHash signature length and deterministic behavior
- Empty MinHash input handling
- Signature similarity and length validation

All 12 unit tests passed during development.

## 9. Limitations

- MinHash provides approximate similarity, so its results can differ from exact Jaccard similarity.
- Linear hash functions approximate random permutations rather than implementing true random permutations.
- The current implementation compares all document pairs, requiring quadratic comparison work.
- Documents producing empty shingle sets are excluded from signature generation and pair comparisons.
- Dataset loading time is excluded from the reported benchmark timings.

## 10. Future Work

Locality-Sensitive Hashing (LSH) can be added to group documents into buckets based on MinHash signature bands.

This could reduce the number of candidate pairs requiring comparison and improve scalability for larger datasets.

## 11. Submission Notes

The submission ZIP should include the source code, unit tests, scripts, README, and PDF report.

The downloaded dataset, virtual environment, temporary files, and Python cache directories should be excluded.

Dataset access and preparation instructions are provided in Section 3.

from itertools import combinations
from statistics import median
from time import perf_counter

from src.data_loader import load_documents
from src.normalization import normalize_text
from src.shingling import Shingling
from src.compare_sets import CompareSets
from src.minhashing import MinHashing
from src.compare_signatures import CompareSignatures
from src.lsh import LSH

THRESHOLD = 0.8
SIGNATURE_LENGTH = 100

def run_benchmark(documents, shingling, compare_sets,
                  minhash, compare_signatures, lsh):

    # 1. Shingling
    start = perf_counter()

    shingle_sets = {}

    for tweet_id, text in documents.items():
        normalized_text = normalize_text(text)

        hashed = set(
            shingling.generate_hashed_shingles(normalized_text)
        )

        if hashed:
            shingle_sets[tweet_id] = hashed

    shingling_time = perf_counter() - start

     # 2. MinHash generation
    start = perf_counter()

    signatures = {
        tweet_id: minhash.generate_signature(shingles)
        for tweet_id, shingles in shingle_sets.items()
    }

    minhash_time = perf_counter() - start

    ids = list(signatures.keys())
    pair_count = len(ids) * (len(ids) - 1) // 2

    # 3. Exact Jaccard comparison
    start = perf_counter()

    for id1, id2 in combinations(ids, 2):
        compare_sets.jaccard_similarity(
            shingle_sets[id1],
            shingle_sets[id2]
        )

    exact_time = perf_counter() - start


    # 4. MinHash comparison
    start = perf_counter()

    for id1, id2 in combinations(ids, 2):
        compare_signatures.similarity(
            signatures[id1],
            signatures[id2]
        )

    signature_time = perf_counter() - start

    # 5. LSH (bonus): find similar pairs without checking all pairs
    start = perf_counter()

    lsh.find_similar_pairs(signatures, THRESHOLD)

    lsh_time = perf_counter() - start

    # 6. Accuracy measurement
    total_error = 0.0

    for id1, id2 in combinations(ids, 2):
        exact = compare_sets.jaccard_similarity(
            shingle_sets[id1],
            shingle_sets[id2]
        )

        estimated = compare_signatures.similarity(
            signatures[id1],
            signatures[id2]
        )

        total_error += abs(exact - estimated)

    mae = total_error / pair_count if pair_count else 0.0

    return {
        "documents": len(shingle_sets),
        "pairs": pair_count,
        "shingling": shingling_time,
        "minhash_generation": minhash_time,
        "exact_comparison": exact_time,
        "signature_comparison": signature_time,
        "lsh": lsh_time,
        "mae": mae
    }

def main():
    all_documents = load_documents(
        "data/documents",
        limit=1000
    )

    shingling = Shingling(k=5)
    compare_sets = CompareSets()
    minhash = MinHashing(n=SIGNATURE_LENGTH)
    compare_signatures = CompareSignatures()
    lsh = LSH.from_threshold(n=SIGNATURE_LENGTH, threshold=THRESHOLD)

    for size in [10, 100, 1000]:
        documents = dict(
            list(all_documents.items())[:size]
        )

        # Repeat to reduce timing noise
        results = [
            run_benchmark(
                documents,
                shingling,
                compare_sets,
                minhash,
                compare_signatures,
                lsh
            )
            for _ in range(3)
        ]

        def med(key):
            return median(result[key] for result in results)

        print(f"\nDataset size: {size}")
        print(f"Processed documents: {results[0]['documents']}")
        print(f"Pairs: {results[0]['pairs']}")
        print(f"Shingling: {med('shingling'):.4f} s")
        print(f"MinHash generation: {med('minhash_generation'):.4f} s")
        print(f"Exact Jaccard: {med('exact_comparison'):.4f} s")
        print(f"MinHash comparison: {med('signature_comparison'):.4f} s")
        print(f"LSH (s = {THRESHOLD}): {med('lsh'):.4f} s")
        print(f"Mean absolute error: {med('mae'):.4f}")


if __name__ == "__main__":
    main()
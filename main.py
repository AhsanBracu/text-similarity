# from src.data_loader import load_documents

# documents = load_documents("data/documents", limit=10)

# for tweet_id, text in documents.items():
#     print(tweet_id, ":", text)

from itertools import combinations
from time import perf_counter

from src.compare_sets import CompareSets
from src.data_loader import load_documents
from src.minhashing import MinHashing
from src.normalization import normalize_text
from src.shingling import Shingling
from src.compare_signatures import CompareSignatures

# shingling = Shingling(k=2)

# result = shingling.generate_hashed_shingles("BANANA")

# print(result)
# print("Unique hashed shingles:", len(result))

# compare = CompareSets()

# doc1 = {10, 20, 30, 40}
# doc2 = {10, 20, 50}
# doc3 = {60, 70, 80}

# print("D1 vs D2:", compare.jaccard_similarity(doc1, doc2))
# print("D1 vs D3:", compare.jaccard_similarity(doc1, doc3))

# shingling = Shingling(k=5)
# minhash = MinHashing(n=2)

# text1 = "Machine learning is useful"
# text2 = "Machine learning is powerful"

# set1 = set(shingling.generate_hashed_shingles(text1))
# set2 = set(shingling.generate_hashed_shingles(text2))

# signature1 = minhash.generate_signature(set1)
# signature2 = minhash.generate_signature(set2)

# print("Document 1 signature:", signature1)
# print("Document 2 signature:", signature2)



# compare = CompareSignatures()

# signature1 = [10, 20, 30, 40]
# signature2 = [10, 50, 30, 60]

# similarity = compare.similarity(signature1, signature2)

# print("Estimated Jaccard similarity:", similarity)


def run_experiment(documents, shingling, compare_sets,
                   minhash, compare_signatures):

    shingle_sets = {}
    signatures = {}

    # Step 1: Shingling and MinHashing
    start = perf_counter()

    for tweet_id, text in documents.items():
        normalized_text = normalize_text(text)

        shingle_sets[tweet_id] = set(
            shingling.generate_hashed_shingles(normalized_text)
        )

        if not shingle_sets[tweet_id]:
            continue

        signatures[tweet_id] = minhash.generate_signature(
            shingle_sets[tweet_id]
        )

    preprocessing_time = perf_counter() - start

    # Step 2: Compare documents
    start = perf_counter()
    top_pairs = []

    threshold = 0.8
    similar_pairs = []

    comparisons = 0

    for id1, id2 in combinations(signatures.keys(), 2):

        exact = compare_sets.jaccard_similarity(
            shingle_sets[id1],
            shingle_sets[id2]
        )

        estimated = compare_signatures.similarity(
            signatures[id1],
            signatures[id2]
        )

        comparisons += 1

        if exact >= threshold:
            similar_pairs.append((id1, id2, exact, estimated))

        # Don't print every pair during benchmarking.
        top_pairs.append((exact, estimated, id1, id2))

    comparison_time = perf_counter() - start
    top_pairs.sort(reverse=True)

    print("\nTop 5 most similar document pairs:")

    # Step 3: Print top 5 pairs

    for exact, estimated, id1, id2 in top_pairs[:5]:
        print(
            f"{id1} vs {id2} | "
            f"Exact: {exact:.4f} | "
            f"MinHash: {estimated:.4f}"
        )

    print(f"\nSimilar document pairs (threshold = {threshold}):")

    for id1, id2, exact, estimated in similar_pairs:
        print(
            f"{id1} vs {id2} | "
            f"Exact: {exact:.4f} | "
            f"MinHash: {estimated:.4f}"
        )

    print(f"Total similar pairs: {len(similar_pairs)}")

    return preprocessing_time, comparison_time, comparisons


# Initialize algorithms once
shingling = Shingling(k=5)
compare_sets = CompareSets()
minhash = MinHashing(n=100)
compare_signatures = CompareSignatures()

# Load the largest dataset once
all_documents = load_documents("data/documents", limit=1000)

for size in [10, 100, 1000]:
    documents = dict(list(all_documents.items())[:size])

    preprocessing_time, comparison_time, comparisons = run_experiment(
        documents,
        shingling,
        compare_sets,
        minhash,
        compare_signatures
    )

    print(f"\nDataset size: {len(documents)}")
    print(f"Document comparisons: {comparisons}")
    print(f"Preprocessing time: {preprocessing_time:.4f} seconds")
    print(f"Comparison time: {comparison_time:.4f} seconds")


# documents = load_documents("data/documents", limit=10)

# all_documents = load_documents(
#     "data/documents",
#     limit=1000
# )

# for size in [10, 100, 1000]:
#     documents = dict(
#         list(all_documents.items())[:size]
#     )

#     print(f"Testing {len(documents)} documents")

# shingling = Shingling(k=5)
# compare_sets = CompareSets()
# minhash = MinHashing(n=100)
# compare_signatures = CompareSignatures()

# shingle_sets = {}
# signatures = {}

# for tweet_id, text in documents.items():
#     normalized_text = normalize_text(text)

#     shingle_sets[tweet_id] = set(
#         shingling.generate_hashed_shingles(normalized_text)
#     )

#     signatures[tweet_id] = minhash.generate_signature(
#         shingle_sets[tweet_id]
#     )

# for id1, id2 in combinations(documents.keys(), 2):
#     exact = compare_sets.jaccard_similarity(
#         shingle_sets[id1],
#         shingle_sets[id2]
#     )

#     estimated = compare_signatures.similarity(
#         signatures[id1],
#         signatures[id2]
#     )

#     print(
#         f"{id1} vs {id2} | "
#         f"Exact: {exact:.4f} | "
#         f"MinHash: {estimated:.4f}"
#     )

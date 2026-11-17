from itertools import combinations

from src.compare_signatures import CompareSignatures


class LSH:
    def __init__(self, bands: int = 10, rows: int = 10):
        if bands <= 0 or rows <= 0:
            raise ValueError("bands and rows must be positive")

        self.bands = bands
        self.rows = rows

    @classmethod
    def from_threshold(cls, n: int, threshold: float) -> "LSH":
        if n <= 0:
            raise ValueError("n must be positive")

        if not 0 < threshold <= 1:
            raise ValueError("threshold must be in (0, 1]")

        best_bands = None
        best_distance = None

        # Try every bands * rows = n split.
        # Prefer an LSH threshold just below t, so fewer real pairs are missed.
        for bands in range(1, n + 1):
            if n % bands != 0:
                continue

            rows = n // bands
            lsh_threshold = (1 / bands) ** (1 / rows)

            if lsh_threshold > threshold:
                continue

            distance = threshold - lsh_threshold

            if best_distance is None or distance < best_distance:
                best_bands = bands
                best_distance = distance

        return cls(bands=best_bands, rows=n // best_bands)

    def approximate_threshold(self) -> float:
        return (1 / self.bands) ** (1 / self.rows)

    def find_candidate_pairs(
        self,
        signatures: dict[str, list[int]]
    ) -> set[tuple[str, str]]:

        candidate_pairs = set()

        for signature in signatures.values():
            if len(signature) != self.bands * self.rows:
                raise ValueError(
                    "Signature length must equal bands * rows"
                )

        for band in range(self.bands):
            buckets = {}
            start = band * self.rows

            # Documents with the same band slice go into the same bucket
            for doc_id, signature in signatures.items():
                band_slice = tuple(signature[start:start + self.rows])
                buckets.setdefault(band_slice, []).append(doc_id)

            # Every pair inside a bucket becomes a candidate
            for doc_ids in buckets.values():
                for id1, id2 in combinations(sorted(doc_ids), 2):
                    candidate_pairs.add((id1, id2))

        return candidate_pairs

    def find_similar_pairs(
        self,
        signatures: dict[str, list[int]],
        threshold: float,
        candidate_pairs: set[tuple[str, str]] | None = None
    ) -> list[tuple[str, str, float]]:

        if not 0 < threshold <= 1:
            raise ValueError("threshold must be in (0, 1]")

        # Reuse candidates if they were already computed
        if candidate_pairs is None:
            candidate_pairs = self.find_candidate_pairs(signatures)

        compare_signatures = CompareSignatures()
        similar_pairs = []

        # Only check the candidates, not all pairs
        for id1, id2 in candidate_pairs:
            similarity = compare_signatures.similarity(
                signatures[id1],
                signatures[id2]
            )

            if similarity >= threshold:
                similar_pairs.append((id1, id2, similarity))

        similar_pairs.sort(key=lambda pair: pair[2], reverse=True)

        return similar_pairs

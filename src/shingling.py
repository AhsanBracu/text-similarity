import hashlib


# Turns a document into a set of hashed character k-shingles.
class Shingling:
    def __init__(self, k: int = 5):
        if k < 1:
            raise ValueError("k must be at least 1")

        self.k = k

    # Every substring of length k. It's a set so duplicates are dropped.
    def generate_shingles(self, text: str) -> set[str]:
        shingles = set()

        for i in range(len(text) - self.k + 1):
            shingle = text[i:i + self.k]
            shingles.add(shingle)

        return shingles

    # 4 byte blake2b hash, so each shingle becomes a 32-bit int.
    # Not using Python's hash() because it changes between runs.
    def hash_shingle(self, shingle: str) -> int:
        hash_bytes = hashlib.blake2b(
            shingle.encode("utf-8"),
            digest_size=4,
        ).digest()

        return int.from_bytes(hash_bytes, byteorder="big")

    def generate_hashed_shingles(self, text: str) -> list[int]:
        shingles = self.generate_shingles(text)

        hashed_shingles = {
            self.hash_shingle(shingle)
            for shingle in shingles
        }

        # sorted, since the task asks for an ordered set
        return sorted(hashed_shingles)

import hashlib


class Shingling:
    def __init__(self, k: int = 5):
        if k < 1:
            raise ValueError("k must be at least 1")

        self.k = k

    def generate_shingles(self, text: str) -> set[str]:
        shingles = set()

        for i in range(len(text) - self.k + 1):
            shingle = text[i:i + self.k]
            shingles.add(shingle)

        return shingles

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

        return sorted(hashed_shingles)

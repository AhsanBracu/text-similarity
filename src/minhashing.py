import random


class MinHashing:
    def __init__(self, n: int = 100):
        if n <= 0:
            raise ValueError("n must be positive")

        self.n = n
        self.prime = 4294967311  # Prime larger than 2^32

        rng = random.Random(42)

        self.hash_functions = [
            (
                rng.randint(1, self.prime - 1),
                rng.randint(0, self.prime - 1)
            )
            for _ in range(n)
        ]

    def generate_signature(self, shingles: set[int]) -> list[int]:
     if not shingles:
        raise ValueError("Cannot generate MinHash for an empty set")

     signature = []

     for a, b in self.hash_functions:
        min_hash = min(
         (a * shingle + b) % self.prime
            for shingle in shingles
        )

        signature.append(min_hash)

     return signature
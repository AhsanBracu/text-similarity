import random


class MinHashing:
    def __init__(self, n: int = 100):
        if n <= 0:
            raise ValueError("n must be positive")

        self.n = n
        # Hash functions are h(x) = (a*x + b) mod p.
        # p has to be bigger than 2^32 because the shingle hashes are 32-bit.
        self.prime = 4294967311  # Prime larger than 2^32

        # fixed seed so we get the same signatures every run
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

     # for every hash function keep the smallest value over all shingles
     signature = []

     for a, b in self.hash_functions:
        min_hash = min(
         (a * shingle + b) % self.prime
            for shingle in shingles
        )

        signature.append(min_hash)

     return signature
class CompareSignatures:

    def similarity(
        self,
        signature1: list[int],
        signature2: list[int]
    ) -> float:

        if len(signature1) != len(signature2):
            raise ValueError("Signatures must have the same length")

        if not signature1:
            raise ValueError("Signatures cannot be empty")

        matches = sum(
            1
            for a, b in zip(signature1, signature2)
            if a == b
        )

        return matches / len(signature1)
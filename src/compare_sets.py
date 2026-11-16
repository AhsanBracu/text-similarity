class CompareSets:

    def jaccard_similarity(
        self,
        set1: set[int],
        set2: set[int]
    ) -> float:

        if not set1 and not set2:
            return 1.0

        intersection = set1.intersection(set2)
        union = set1.union(set2)

        return len(intersection) / len(union)

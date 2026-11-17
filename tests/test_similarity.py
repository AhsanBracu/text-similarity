
import unittest

from src.shingling import Shingling
from src.compare_sets import CompareSets
from src.minhashing import MinHashing
from src.compare_signatures import CompareSignatures


class TestShingling(unittest.TestCase):

    def test_generate_shingles(self):
        shingling = Shingling(k=2)

        result = shingling.generate_shingles("BANANA")

        self.assertEqual(result, {"BA", "AN", "NA"})

    def test_hashed_shingles_are_unique_and_sorted(self):
        shingling = Shingling(k=2)

        result = shingling.generate_hashed_shingles("BANANA")

        self.assertEqual(result, sorted(set(result)))
        self.assertTrue(all(isinstance(x, int) for x in result))


class TestCompareSets(unittest.TestCase):

    def test_jaccard_similarity(self):
        compare = CompareSets()

        set1 = {10, 20, 30}
        set2 = {10, 20, 40}

        result = compare.jaccard_similarity(set1, set2)

        self.assertAlmostEqual(result, 0.5)

    def test_identical_sets(self):
        compare = CompareSets()

        result = compare.jaccard_similarity(
            {10, 20, 30},
            {10, 20, 30}
        )

        self.assertEqual(result, 1.0)

    def test_disjoint_sets(self):
        compare = CompareSets()

        result = compare.jaccard_similarity(
            {10, 20},
            {30, 40}
        )

        self.assertEqual(result, 0.0)

    def test_empty_sets(self):
        compare = CompareSets()

        self.assertEqual(
            compare.jaccard_similarity(set(), set()),
            1.0
        )


class TestMinHashing(unittest.TestCase):

    def test_signature_length(self):
        minhash = MinHashing(n=100)

        signature = minhash.generate_signature(
            {10, 20, 30}
        )

        self.assertEqual(len(signature), 100)

    def test_same_document_same_signature(self):
        minhash = MinHashing(n=100)

        shingles = {10, 20, 30}

        sig1 = minhash.generate_signature(shingles)
        sig2 = minhash.generate_signature(shingles)

        self.assertEqual(sig1, sig2)

    def test_empty_shingles(self):
        minhash = MinHashing(n=100)

        with self.assertRaises(ValueError):
            minhash.generate_signature(set())


class TestCompareSignatures(unittest.TestCase):

    def test_similarity(self):
        compare = CompareSignatures()

        sig1 = [10, 20, 30, 40]
        sig2 = [10, 50, 30, 60]

        self.assertEqual(
            compare.similarity(sig1, sig2),
            0.5
        )

    def test_identical_signatures(self):
        compare = CompareSignatures()

        self.assertEqual(
            compare.similarity(
                [10, 20, 30],
                [10, 20, 30]
            ),
            1.0
        )

    def test_different_lengths(self):
        compare = CompareSignatures()

        with self.assertRaises(ValueError):
            compare.similarity(
                [10, 20, 30],
                [10, 20]
            )


if __name__ == "__main__":
    unittest.main()

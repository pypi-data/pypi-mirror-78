import unittest
from basicCompare import ValComparator

class TestNum(unittest.TestCase):
    # Test 1 
    def test1_greater(self):
        self.assertEqual(ValComparator(7.5, 5.5).greater(), True)
    def test1_equal(self):
        self.assertEqual(ValComparator(7.5, 5.5).equal(), False)
    def test1_less(self):
        self.assertEqual(ValComparator(7.5, 5.5).less(), False)

    # Test 2
    def test2_greater(self):
        self.assertEqual(ValComparator(2.15, 2.15).greater(), False)
    def test2_equal(self):
        self.assertEqual(ValComparator(2.15, 2.15).equal(), True)
    def test2_less(self):
        self.assertEqual(ValComparator(2.15, 2.15).less(), False)

    # Test 3
    def test3_greater(self):
        self.assertEqual(ValComparator(2.5, 5.25).greater(), False)
    def test3_equal(self):
        self.assertEqual(ValComparator(2.5, 5.25).equal(), False)
    def test3_less(self):
        self.assertEqual(ValComparator(2.5, 5.25).less(), True)

if __name__ == '__main__':
    unittest.main()
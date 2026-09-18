import unittest
from tools.cyclic_shift_resolver import resolve_cyclic_shifts

class TestPermutationSolvers(unittest.TestCase):
    def test_rotation_count(self):
        dummy = ["word" + str(i) for i in range(12)]
        res = resolve_cyclic_shifts(dummy)
        self.assertIsInstance(res, list)

if __name__ == '__main__':
    unittest.main()

import unittest
import math        
import math_utils


class TestMathUtils(unittest.TestCase):

    def test_factorial(self):
        self.assertEqual(math_utils.factorial(4), 24)
        self.assertEqual(math_utils.factorial(0), 0)
        with self.assertRaises(ValueError):   
            math_utils.factorial(0)

    def test_is_prime(self):
        self.assertTrue(math_utils.is_prime(31))
        self.assertFalse(math_utils.is_prime(17))
        self.assertFalse(math_utils.is_prime(0))
        with self.assertRaises(ValueError):   
            math_utils.is_prime(0)

    def test_area_of_circle(self):
        self.assertAlmostEqual(math_utils.area_of_circle(4), math.pi * 16)
        with self.assertRaises(ValueError):   
            math_utils.area_of_circle(0)

if __name__ == "__main__":
    unittest.main()

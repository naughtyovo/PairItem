from fractions import Fraction
from utils import fraction_to_mixed,mixed_to_fraction
import unittest


# 假设 fraction_to_mixed 和 mixed_to_fraction 函数已经定义在上面的代码块中

class TestFractionConversion(unittest.TestCase):
    def test_fraction_to_mixed_proper_fraction(self):
        # 测试真分数
        frac = Fraction(1, 3)
        expected = "1/3"
        result = fraction_to_mixed(frac)
        self.assertEqual(result, expected, msg="Failed to convert proper fraction to string")

    def test_fraction_to_mixed_improper_fraction(self):
        # 测试假分数
        frac = Fraction(7, 3)
        expected = "2'1/3"
        result = fraction_to_mixed(frac)
        self.assertEqual(result, expected, msg="Failed to convert improper fraction to mixed string")

    def test_fraction_to_mixed_whole_number(self):
        # 测试整数（可以视为分母为1的分数）
        frac = Fraction(5, 1)
        expected = "5"
        result = fraction_to_mixed(frac)
        self.assertEqual(result, expected, msg="Failed to convert whole number fraction to string")

    def test_mixed_to_fraction_mixed_number(self):
        # 测试带分数
        mixed_str = "2'1/3"
        expected = Fraction(7, 3)
        result = mixed_to_fraction(mixed_str)
        self.assertEqual(result, expected, msg="Failed to convert mixed number string to Fraction")

    def test_mixed_to_fraction_simple_fraction(self):
        # 测试简单分数
        simple_str = "3/4"
        expected = Fraction(3, 4)
        result = mixed_to_fraction(simple_str)
        self.assertEqual(result, expected, msg="Failed to convert simple fraction string to Fraction")

    def test_mixed_to_fraction_invalid_input(self):
        # 测试无效输入（不包含 '/'）
        invalid_str = "2'1"
        with self.assertRaises(ValueError, msg="Expected ValueError for invalid input"):
            mixed_to_fraction(invalid_str)

    def test_mixed_to_fraction_integer_input(self):
        # 测试整数输入（虽然不是带分数，但函数应该能够处理）
        integer_str = "5"
        expected = Fraction(5, 1)
        result = mixed_to_fraction(integer_str)
        self.assertEqual(result, expected, msg="Failed to convert integer string to Fraction")


if __name__ == '__main__':
    unittest.main()
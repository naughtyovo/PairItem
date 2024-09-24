import unittest
from unittest.mock import patch
from random import Random
from fractions import Fraction
from question import Question  # 假设你的类在 question.py 中


class TestQuestion(unittest.TestCase):

    @patch('question.Random')  # 模拟 Random 类
    def test_generate_question(self, mock_random):
        # 初始化 Mock 随机数生成器的行为
        mock_random.return_value = Random(42)  # 让随机数生成器有可预期的输出
        question = Question()

        question.generate_question(max_value=10, num=3)

        # 检查生成的运算符
        self.assertEqual(len(question.symbols), question.total - 1)
        # 检查操作数的个数是否正确
        self.assertEqual(len(question.rational_numbers), question.total)
        # 确保结果是 Fraction 类型并且结果为正数
        self.assertTrue(isinstance(question.result, Fraction))
        self.assertGreater(question.result, 0)

    def test_generate_symbols(self):
        question = Question(total=4)
        question.generate_symbols()
        # 确保 symbols 数量和 total - 1 是一致的
        self.assertEqual(len(question.symbols), 3)
        for symbol in question.symbols:
            self.assertIn(symbol, question.operators)

    @patch('random.Random.choice')
    def test_generate_bracket_no_symbols(self, mock_choice):
        # 测试当 symbols 列表长度小于等于1时，不应生成括号
        question = Question(total=2, symbols=[])
        question.generate_bracket()
        self.assertEqual(question.bracket, -2)  # 确保没有生成括号

    @patch('random.Random.choice')
    def test_generate_bracket_with_addition(self, mock_choice):
        # 测试当 symbols 中包含加法运算时，括号生成的位置
        mock_choice.return_value = True  # 强制使得 choice 返回 True，以便生成括号
        question = Question(total=3, symbols=['+', '*'])
        question.generate_bracket()
        # 确保括号生成在加法符号的位置
        self.assertEqual(question.bracket, 0)

    @patch('random.Random.choice')
    def test_generate_bracket_with_subtraction(self, mock_choice):
        # 测试当 symbols 中包含减法运算时，括号生成的位置
        mock_choice.return_value = True  # 强制使得 choice 返回 True，以便生成括号
        question = Question(total=4, symbols=['*', '-'])
        question.generate_bracket()
        # 确保括号生成在减法符号的位置
        self.assertEqual(question.bracket, 1)

    @patch('random.Random.choice')
    def test_no_bracket_generated(self, mock_choice):
        # 测试当 Random.choice 返回 False 时，不应生成括号
        mock_choice.return_value = False  # 强制 choice 返回 False
        question = Question(total=4, symbols=['+', '-'])
        question.generate_bracket()
        self.assertEqual(question.bracket, -2)  # 确保没有生成括号

    def test_generate_rational_numbers(self):
        question = Question(total=3)
        try:
            question.generate_symbols()  # 生成符号
            question.generate_rational_numbers(max_value=9)
            # 检查生成的操作数数量
            self.assertEqual(len(question.rational_numbers), 3)
            for num in question.rational_numbers:
                # 检查操作数是否为整数或 Fraction 类型
                self.assertTrue(isinstance(num, int) or isinstance(num, Fraction))
        except ValueError as e:
            self.fail(f"生成的操作数无效: {str(e)}")

    def test_generate_string(self):
        question = Question(total=3, rational_numbers=[1, Fraction(1, 2), 3], symbols=['+', '*'])
        question.generate_string()
        expected_string = "1+(1/2)*3"
        self.assertEqual(question.string_ver, expected_string)

    def test_calculate_result(self):
        question = Question(total=3, rational_numbers=[1, Fraction(1, 2), 3], symbols=['+', '*'])
        question.generate_string()
        result = question.calculate_result()
        # 检查计算结果
        self.assertEqual(result, Fraction(5, 2))

    def test_validate_rational_numbers(self):
        question = Question(total=3, rational_numbers=[5, 3, 2], symbols=['-', '+'])
        with self.assertRaises(ValueError):
            question.validate_rational_numbers()  # 应该抛出 ValueError，因为 5 - 3 = 2, 3 - 2 = 1 是有效的

    # def test_validate_rational_numbers(self):
    #     question = Question(total=3, rational_numbers=[5, 4, 3], symbols=['-', '-', '+'])
    #     result = question.validate_rational_numbers()  # 这里5-4=1, 4-3=1都是有效的，改变数值或符号以确保抛出异常
    #     print("+++++++++")
    #     print(result)


if __name__ == '__main__':
    unittest.main()

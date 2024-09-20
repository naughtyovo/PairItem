from fractions import Fraction
from random import Random


class Question:
    # 运算符列表，包含加、减、乘、除四种运算
    operators = ['+', '-', '*', '/']

    def __init__(self, total=0, symbols=None, bracket=-2, rational_numbers=None, string_ver=""):
        # 初始化函数，设置类的属性，默认值为0或空列表
        if symbols is None:
            symbols = []  # 用于存储运算符
        if rational_numbers is None:
            rational_numbers = []  # 用于存储有理数
        self.total = total  # 表示题目中操作数的数量
        self.symbols = symbols  # 用于存储运算符列表
        self.bracket = bracket  # 表示括号位置，-2 表示无括号
        self.rational_numbers = rational_numbers  # 用于存储生成的操作数（包括整数和分数）
        self.string_ver = string_ver  # 表示题目的字符串形式
        self.result = -1  # 用于存储最终计算的结果
        self.ran = Random()  # 用于生成随机数

    def generate_question(self, maxium, num=4):
        """
        生成一道数学题。包括生成运算符、操作数、括号、以及字符串形式的题目。
        还会计算题目的最终结果，确保其为正数。
        :param maxium: 题目中操作数的最大值
        :param num: 操作数的最大数量
        """
        # 随机选择操作数的数量（至少为2个）
        total = self.ran.randint(2, num)
        self.total = total

        # 生成运算符
        self.generate_symbols(total)

        # 生成括号的位置（如果有）
        self.generate_bracket(total, self.symbols)

        # 生成操作数（包括整数和分数）
        self.generate_rational_numbers(total, maxium, self.symbols)

        # 将生成的题目转换为字符串形式
        self.generate_string()

        # 计算题目的结果，并将其限制为有理数形式
        result = Fraction(eval(self.string_ver)).limit_denominator(1024)

        # 确保结果大于0
        if result <= 0:
            raise ValueError  # 如果结果不为正，抛出异常
        self.result = result  # 存储计算结果

    def generate_symbols(self, total):
        """
        生成 total-1 个运算符，并存储到 symbols 列表中。
        :param total: 操作数的数量
        """
        # 随机选择运算符并存入 symbols 列表
        self.symbols = [self.ran.choice(self.operators) for _ in range(total - 1)]

    def generate_bracket(self, total, symbols):
        """
        根据运算符的位置，决定是否添加括号，并确定括号的位置。
        :param total: 操作数的数量
        :param symbols: 生成的运算符列表
        """
        # 初始化括号位置为 -2，表示无括号
        self.bracket = -2

        # 当运算符数量不止一个时，可能会添加括号
        if len(symbols) != 1:
            for i in range(total - 1):
                # 如果当前运算符为加法或减法，且随机选择为 True，则添加括号
                if symbols[i] in ['+', '-'] and self.ran.choice([True, False]):
                    self.bracket = i
                    break

    def generate_rational_numbers(self, total, maxium, symbols):
        """
        生成 total 个操作数，可能是整数或分数。
        :param total: 操作数的数量
        :param maxium: 操作数的最大值
        :param symbols: 运算符列表，用于在生成减法时检查操作数
        """
        self.rational_numbers = []

        for i in range(total):
            # 随机选择生成整数或分数
            if self.ran.choice([True, False]):
                # 生成整数
                self.rational_numbers.append(self.ran.randint(1, maxium))
            else:
                # 生成分数，分母范围为 2 到 maxium 之间的随机数，分子小于分母
                denominator = self.ran.randint(2, maxium)
                numerator = self.ran.randint(1, denominator - 1)
                self.rational_numbers.append(Fraction(numerator=numerator, denominator=denominator))

            # 如果前一个运算符是减法，并且操作数的结果为负数，则抛出异常
            if i > 0 and symbols[i - 1] == '-' and self.rational_numbers[i - 1] - self.rational_numbers[i] <= 0:
                raise ValueError

    def generate_string(self):
        """
        根据生成的操作数和运算符，构建数学表达式的字符串形式。
        """
        string_ver = ""

        # 遍历操作数和运算符，构建表达式字符串
        for i in range(self.total - 1):
            if self.bracket == i:
                string_ver += '('  # 如果当前索引等于括号位置，添加左括号
            # 如果当前操作数是分数，将其包裹在括号中
            if isinstance(self.rational_numbers[i], Fraction):
                string_ver += '(' + str(self.rational_numbers[i]) + ')'
            else:
                string_ver += str(self.rational_numbers[i])  # 否则直接添加整数
            if self.bracket + 1 == i:
                string_ver += ')'  # 添加右括号
            string_ver += self.symbols[i]  # 添加运算符

        # 添加最后一个操作数
        if isinstance(self.rational_numbers[-1], Fraction):
            string_ver += '(' + str(self.rational_numbers[-1]) + ')'
        else:
            string_ver += str(self.rational_numbers[-1])

        # 如果括号位置在最后一个运算符处，添加右括号
        if self.bracket == i:
            string_ver += ')'

        # 将生成的表达式存储为字符串形式
        self.string_ver = string_ver

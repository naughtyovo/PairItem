from fractions import Fraction
from random import Random


class Question:
    # 可用的运算符列表
    operators = ['+', '-', '*', '/']

    def __init__(self, total=0, symbols=None, bracket=-2, rational_numbers=None, string_ver=""):
        """
        初始化 Question 类实例，定义表达式的相关属性。

        :param total: 操作数的数量，默认值为 0。
        :param symbols: 运算符列表，默认值为空列表。
        :param bracket: 括号的位置，默认值为 -2 表示没有括号。
        :param rational_numbers: 操作数的列表，包含整数或分数，默认值为空列表。
        :param string_ver: 数学表达式的字符串形式，默认值为空字符串。
        """
        self.total = total or 0  # 操作数数量，默认为 0
        self.symbols = symbols or []  # 运算符列表，默认为空
        self.bracket = bracket  # 括号位置，默认为 -2，表示无括号
        self.rational_numbers = rational_numbers or []  # 操作数列表（整数或分数）
        self.string_ver = string_ver  # 数学表达式的字符串形式
        self.result = -1  # 表达式结果，默认为 -1 表示未计算
        self.ran = Random()  # 随机数生成器

    def generate_question(self, max_value, num=4):
        """
        生成一个数学表达式问题，包括随机生成的操作数和运算符。

        :param max_value: 操作数的最大值。
        :param num: 操作数的最大数量，默认值为 4。
        """
        self.total = self.ran.randint(2, num)  # 随机生成操作数的数量，最少 2 个
        self.generate_symbols()  # 生成运算符
        self.generate_bracket()  # 生成括号
        self.generate_rational_numbers(max_value)  # 生成操作数
        self.generate_string()  # 生成表达式的字符串形式
        self.result = self.calculate_result()  # 计算表达式结果

    def generate_symbols(self):
        """
        随机生成运算符。
        根据操作数数量，从操作符列表中随机选择运算符。
        """
        self.symbols = [self.ran.choice(self.operators) for _ in range(self.total - 1)]

    def generate_bracket(self):
        """
        随机决定是否添加括号，并确定括号位置。
        如果操作符数量大于1，且是加法或减法运算，随机添加括号。
        """
        if len(self.symbols) > 1:
            # 当符号是加法或减法时，有一定几率在符号位置插入括号
            self.bracket = next(
                (i for i in range(self.total - 1) if self.symbols[i] in ['+', '-'] and self.ran.choice([True, False])),
                -2)

    def generate_rational_numbers(self, max_value):
        """
        生成操作数，随机决定每个操作数是整数或分数。

        :param max_value: 操作数的最大值。
        """
        self.rational_numbers = [
            # 随机决定操作数是整数还是分数
            self.ran.randint(1, max_value) if self.ran.choice([True, False])
            else Fraction(self.ran.randint(1, self.ran.randint(2, max_value) - 1), self.ran.randint(2, max_value))
            for _ in range(self.total)
        ]
        self.validate_rational_numbers()  # 验证生成的操作数是否有效

    def validate_rational_numbers(self):
        """
        验证操作数的有效性，确保减法运算不会导致非正数。
        如果操作数导致结果为负数或零，抛出异常。
        """
        for i in range(1, self.total):
            # 如果符号是减法，且前后两个操作数相减结果为 0 或负数，则抛出异常
            if self.symbols[i - 1] == '-' and self.rational_numbers[i - 1] - self.rational_numbers[i] <= 0:
                raise ValueError  # 抛出异常以重新生成问题

    def generate_string(self):
        """
        根据生成的操作数和运算符，构建数学表达式的字符串形式。
        """
        string_ver = ""  # 初始化空字符串，用于存储表达式

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

    def calculate_result(self):
        """
        计算表达式的结果，并确保结果是正数。

        :return: 计算后的表达式结果，使用 Fraction 确保分数表示。
        """
        # 使用 eval 函数计算字符串形式的表达式结果，并将其转换为 Fraction 类型
        result = Fraction(eval(self.string_ver)).limit_denominator(1024)

        # 确保结果大于0
        if result <= 0:
            raise ValueError  # 如果结果不为正，抛出异常

        self.result = result  # 存储计算结果
        return result  # 返回结果

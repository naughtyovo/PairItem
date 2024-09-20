"""
四则运算生成器
"""
import argparse
import os
from fractions import Fraction
from random import Random


class Question:
    """问题类"""
    operators = ['+', '-', '*', '/']  # 运算符

    def __init__(self,
                 total=0,
                 symbols=None,
                 bracket=-2,
                 rational_numbers=None,
                 string_ver=""):
        if symbols is None:
            symbols = []
        if rational_numbers is None:
            rational_numbers = []
        self.total = total
        self.symbols = symbols
        self.bracket = bracket
        self.rational_numbers = rational_numbers
        self.string_ver = string_ver
        self.result = -1

        # 构造随机数生成器
        ran = Random()
        self.ran = ran

    def generate_question(self, maxium, num=4):
        """生成题目"""
        total = self.ran.randint(2, num)  # 此题中运算数个数
        self.total = total

        # 运算符序列生成
        self.generate_symbols(total)
        # print(self.symbols)

        # 括号首元素索引生成（只生成一个括号）
        self.generate_bracket(total, self.symbols)
        # print(self.bracket)

        # 运算数序列生成
        self.generate_rational_numbers(total, maxium, self.symbols)
        # print(self.rational_numbers)

        # 转换为生成字符串
        self.generate_string()
        # print(self.string_ver)

        # 结果检查
        result = Fraction(eval(self.string_ver)).limit_denominator(1024)
        if result <= 0:
            raise ValueError
        self.result = result
        # print(result)

    def generate_symbols(self, total):
        """生成符号列表"""
        symbols = []
        for _ in range(total - 1):
            symbols.append(self.ran.choice(self.operators))
        self.symbols = symbols

    def generate_bracket(self, total, symbols):
        """生成括号首元素索引"""
        bracket = -2  # 若依然是-1则说明没有括号
        if len(symbols) != 1:
            for i in range(total - 1):
                # 只有加减两端应该生成括号，概率50%，生成一次后break
                if symbols[i] in ['+', '-']:
                    if self.ran.choice([True, False]):
                        bracket = i
                        break
        self.bracket = bracket

    def generate_rational_numbers(self, total, maxium, symbols):
        """生成有理数列表"""
        rational_numbers = []
        for i in range(total):
            # 生成一个数，插入序列
            if self.ran.choice([True, False]):
                rational_numbers.append(self.ran.randint(1, maxium))
            else:
                denominator = self.ran.randint(2, maxium)
                numerator = self.ran.randint(1, denominator - 1)
                # if numerator - (numerator // denominator * denominator) != 0:
                #     rational_numbers.append(Fraction(denominator=denominator, numerator=numerator))
                # else:
                #     rational_numbers.append(numerator // denominator)
                rational_numbers.append(Fraction(denominator=denominator, numerator=numerator))

            # 大小检查
            if i > 0 and symbols[i - 1] == '-':
                if rational_numbers[i - 1] - rational_numbers[i] <= 0:
                    raise ValueError
        self.rational_numbers = rational_numbers

    def generate_string(self):
        """
        将成员中的有理数，符号，括号生成为字符串
        结果将存入成员变量string_ver中
        """
        i = 0
        string_ver = ""
        for i in range(self.total - 1):
            if self.bracket == i:
                string_ver += '('
            if isinstance(self.rational_numbers[i], Fraction):
                string_ver += '(' + str(self.rational_numbers[i]) + ')'
            else:
                string_ver += str(self.rational_numbers[i])
            if self.bracket + 1 == i:
                string_ver += ')'
            string_ver += self.symbols[i]

        if isinstance(self.rational_numbers[-1], Fraction):
            string_ver += '(' + str(self.rational_numbers[-1]) + ')'
        else:
            string_ver += str(self.rational_numbers[-1])
        if self.bracket == i:
            string_ver += ')'
        self.string_ver = string_ver


def answer_questions(r, n, answer_mode=False):
    """答题模式"""
    # q = Question(r)
    correct_answers = 0
    wrong_answers = 0

    # 创建并清空文件
    with open("file\\Exercise.txt", 'w', encoding="UTF-8"):
        pass
    with open("file\\Answer.txt", 'w', encoding="UTF-8"):
        pass

    with open("file\\Exercise.txt", 'a', encoding="UTF-8") as fp1, \
            open("file\\Answer.txt", 'a', encoding="UTF-8") as fp2:
        # qlist = []
        for question_num in range(1, n + 1):
            # 生成题目类
            while True:
                try:
                    question = Question()
                    question.generate_question(r)
                    # qlist.append(question)
                except ValueError:
                    continue
                break
                # question = Question()
                # question.generate_question(r)
                # qlist.append(question)

            # 写入题目与答案到文件
            fp1.write(f"({question_num}){question.string_ver} = \n")
            fp2.write(f"({question_num}){fraction_to_mixed(question.result)}\n")

            if answer_mode:
                # 打印题目
                # print(f"{fraction_to_mixed(question.result)}")
                answer = input(f"({question_num}){question.string_ver} = ")

                # 判断对错
                answer = mixed_to_fraction(answer)
                if answer == question.result:
                    print("√")
                    correct_answers += 1
                else:
                    print(f"×    | The correct answer is: {fraction_to_mixed(question.result)}")
                    wrong_answers += 1

    if answer_mode:
        # 打印统计信息
        print(f""
              f"正确题目数：{correct_answers}\n"
              f"错误题目数：{wrong_answers}")
    else:
        print("生成已经完成！")


def check_answer(exercise_file, answer_file):
    """
    检查模式
    :param exercise_file: 习题
    :param answer_file: 答案
    :return: 检查结果，正确数与错误数
    """
    correct_answers = 0
    correct_list = []
    wrong_answers = 0
    wrong_list = []

    with open(exercise_file, 'r', encoding="UTF-8") as fp1, open(answer_file, 'r', encoding="UTF-8") as fp2:
        counter = 1
        exe_line = fp1.readline()
        ans_line = fp2.readline()
        while exe_line and ans_line:
            # 找到第一个右括号，即为题目的开始
            exe_line = exe_line[exe_line.index(')') + 1:-3]
            ans_line = ans_line[ans_line.index(')') + 1:]
            ans_line = str(mixed_to_fraction(ans_line))
            result_exe = Fraction(eval(exe_line)).limit_denominator(1024)
            result_ans = Fraction(eval(ans_line)).limit_denominator(1024)
            if result_ans == result_exe:
                correct_answers += 1
                correct_list.append(counter)
            else:
                wrong_answers += 1
                wrong_list.append(counter)
            # print(result_exe, result_ans)
            exe_line = fp1.readline()
            ans_line = fp2.readline()
            counter += 1
    with open("file\\Grade.txt", 'w', encoding="UTF-8") as fp:
        line = f"Correct: {correct_answers} {tuple(correct_list)}\n"
        print(line)
        fp.write(line)
        line = f"Wrong: {wrong_answers} {tuple(wrong_list)}\n"
        print(line)
        fp.write(line)
    print("输出结果已写入到同目录下file文件夹中的Grade.txt")


def fraction_to_mixed(frac: Fraction) -> str:
    """
    将Fraction分数转换为带分数字符串
    :param frac: 分数
    :return: 带分数字符串
    """
    if frac.numerator <= frac.denominator or frac.denominator == 1:
        return str(frac)

    result = ""
    result += str(frac.numerator // frac.denominator)
    result += "'"
    result += str(frac - frac.numerator // frac.denominator)
    return result


def mixed_to_fraction(string: str) -> Fraction:
    """
    将字符串转换为Fraction分数或整型
    :param string:字符串
    :return:
    """

    if '/' in string and "'" in string:
        try:
            # 切分带分数的整数部分与分数部分
            # print("origin: " + string)
            div = string.split("'")  # 报错则说明没有 ' 符号
            if len(div) != 2:  # 大于一个 ' 符号
                raise ValueError
            div1 = div[0]
            # print(f"r1 = {div1}")

            # 切分分子与分母
            div = div[1].split("/")  # 报错则说明没有 / 符号
            if len(div) != 2:  # 大于一个 / 符号
                raise ValueError
            div2 = div[0]
            # print(f"r2 = {div2}")
            div3 = div[1]
            # print(f"r3 = {div3}")
            if "" in [div1, div2, div3]:  # 报错则说明缺失其中整数/分子/分母
                raise ValueError
        except (ValueError, IndexError):
            raise ValueError
        return int(div1) + Fraction(f"{div2}/{div3}")

    return Fraction(string)


def get_arguments():
    """
    cmd参数解析器
    :return:
    """
    parser = argparse.ArgumentParser(description="Usage Example: python main.py -n 3 -r 10",
                                     epilog="若需要使用判题功能，请勿输入-r参数")
    parser.add_argument('-n', type=int, help="生成题目的个数（默认为10）")
    parser.add_argument('-r', type=int, help="题目中的最大数值")
    parser.add_argument('-m', action='store_true', help="启用答题模式（默认关闭）")
    parser.add_argument('-e', type=str, help="题目文件路径")
    parser.add_argument('-a', type=str, help="答案文件路径")
    return parser.parse_args()


if __name__ == '__main__':
    # 获取参数信息
    # n —— 题目数量
    # r —— 数值最大值
    # e, a —— 题目与答案
    args = get_arguments()
    if args.n:
        n = args.n
    else:
        n = 10  # 默认值
    if args.r:
        r = args.r
        m = False
        if args.m:
            m = args.m
        # 答题模式
        answer_questions(r, n, m)
        # q = Question()
        # q.generate_question(10)
        # print(q.string_ver)


    else:
        if args.e and args.a:
            # 检查模式
            EXERCISE_FILE = args.e
            ANSWER_FILE = args.a
            check_answer(EXERCISE_FILE, ANSWER_FILE)
        else:
            # 什么模式都没有进入！
            print("Argument '-r' is needed!")
            os.system("pause")
            exit()

from fractions import Fraction
from question import Question
from utils import fraction_to_mixed, mixed_to_fraction


def answer_questions(r, n, answer_mode=False):
    """
    生成并解答随机的数学题目，将题目和答案分别保存到文件中。
    :param r: 操作数的最大值
    :param n: 题目数量
    :param answer_mode: 是否启用用户答题模式，True 为启用答题模式
    """
    correct_answers = 0  # 用于统计用户正确答题数
    wrong_answers = 0  # 用于统计用户错误答题数

    # 清空已有的题目和答案文件
    with open("file\\Exercise.txt", 'w', encoding="UTF-8"), open("file\\Answer.txt", 'w', encoding="UTF-8"):
        pass  # 占位操作，目的是清空文件内容

    # 打开题目和答案文件，准备写入新题目和答案
    with open("file\\Exercise.txt", 'a', encoding="UTF-8") as fp1, open("file\\Answer.txt", 'a',
                                                                        encoding="UTF-8") as fp2:
        for question_num in range(1, n + 1):  # 生成 n 道题目
            while True:
                try:
                    # 生成一个新的问题对象
                    question = Question()
                    question.generate_question(r)  # 生成题目，最大操作数为 r
                except ValueError:
                    # 如果题目结果为负数，重新生成
                    continue
                break

            # 将生成的题目写入文件中
            fp1.write(f"({question_num}){question.string_ver} = \n")
            # 将答案转换为带分数形式并写入答案文件中
            fp2.write(f"({question_num}){fraction_to_mixed(question.result)}\n")

            # 如果启用了答题模式
            if answer_mode:
                # 提示用户输入答案
                answer = input(f"({question_num}){question.string_ver} = ")
                # 将用户输入的答案转换为 Fraction 类型
                answer = mixed_to_fraction(answer)
                # 判断用户答案是否正确
                if answer == question.result:
                    print("√")  # 如果正确，打印 √
                    correct_answers += 1  # 正确答题数加 1
                else:
                    # 如果错误，显示正确答案并打印 ×
                    print(f"× | The correct answer is: {fraction_to_mixed(question.result)}")
                    wrong_answers += 1  # 错误答题数加 1

    # 如果是答题模式，输出正确和错误题目数
    if answer_mode:
        print(f"正确题目数：{correct_answers}\n错误题目数：{wrong_answers}")
    else:
        # 否则，提示生成已完成
        print("生成已经完成！")


def check_answer(exercise_file, answer_file):
    """
    校对题目和答案文件，检查答案是否正确，并将结果写入文件。
    :param exercise_file: 题目文件路径
    :param answer_file: 答案文件路径
    """
    correct_answers = 0  # 正确答案数量
    wrong_answers = 0  # 错误答案数量
    correct_list = []  # 保存正确题目的编号
    wrong_list = []  # 保存错误题目的编号

    # 打开题目和答案文件，逐行读取
    with open(exercise_file, 'r', encoding="UTF-8") as fp1, open(answer_file, 'r', encoding="UTF-8") as fp2:
        counter = 1  # 题目编号计数器
        exe_line = fp1.readline()  # 读取一行题目
        ans_line = fp2.readline()  # 读取一行答案
        while exe_line and ans_line:
            # 提取出题目中的表达式部分
            exe_line = exe_line[exe_line.index(')') + 1:-3]
            # 提取出答案部分，并将其转换为 Fraction 类型
            ans_line = ans_line[ans_line.index(')') + 1:]
            ans_line = str(mixed_to_fraction(ans_line))
            # 计算题目表达式的正确结果
            result_exe = Fraction(eval(exe_line)).limit_denominator(1024)
            # 计算答案的结果
            result_ans = Fraction(eval(ans_line)).limit_denominator(1024)
            # 比较答案是否正确
            if result_ans == result_exe:
                correct_answers += 1  # 正确答案数加 1
                correct_list.append(counter)  # 将题号加入正确列表
            else:
                wrong_answers += 1  # 错误答案数加 1
                wrong_list.append(counter)  # 将题号加入错误列表
            # 读取下一行题目和答案
            exe_line = fp1.readline()
            ans_line = fp2.readline()
            counter += 1  # 题号加 1

    # 将结果写入成绩文件
    with open("file\\Grade.txt", 'w', encoding="UTF-8") as fp:
        fp.write(f"Correct: {correct_answers} {tuple(correct_list)}\n")  # 写入正确答案信息
        fp.write(f"Wrong: {wrong_answers} {tuple(wrong_list)}\n")  # 写入错误答案信息
    print("输出结果已写入file文件夹中的Grade.txt")

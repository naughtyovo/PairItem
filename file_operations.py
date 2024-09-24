from fractions import Fraction
from question import Question
from utils import fraction_to_mixed, mixed_to_fraction
import sys
import time
import threading
import concurrent.futures


## 多线程模式
def generate_single_question(r, question_num):
    """
    生成一个数学题目并返回题目及答案。
    :param r: 操作数的最大值
    :param question_num: 当前题目的序号
    :return: 题号、题目文本和答案
    """
    while True:
        try:
            # 生成一个新的问题对象
            question = Question()
            question.generate_question(r)  # 生成题目，最大操作数为 r
        except ValueError:
            # 如果题目结果为负数，重新生成
            continue
        break
    question_text = f"{question_num}. {question.string_ver} = \n"
    answer_text = f"{question_num}. {fraction_to_mixed(question.result)}\n"
    return question_num, question_text, answer_text

def answer_questions(r, n, answer_mode=False):
    """
    生成并解答随机的数学题目，将题目和答案分别保存到文件中。
    :param r: 操作数的最大值
    :param n: 题目数量
    :param answer_mode: 是否启用用户答题模式，True 为启用答题模式
    """
    correct_answers = 0  # 用于统计用户正确答题数
    wrong_answers = 0  # 用于统计用户错误答题数
    # 计时
    start_time = time.time()
    # 清空已有的题目和答案文件
    with open("file\\Exercise.txt", 'w', encoding="UTF-8"), open("file\\Answer.txt", 'w', encoding="UTF-8"):
        pass  # 占位操作，目的是清空文件内容

    # 用于存储生成的题目和答案的列表
    question_data = []

    # 使用线程池并行生成题目
    if n > 5000:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1024) as executor:
            futures = [executor.submit(generate_single_question, r, question_num) for question_num in range(1, n + 1)]
            # 查看当前活跃的线程数量
            print(f"当前活跃的线程数: {threading.active_count()}")
            for future in concurrent.futures.as_completed(futures):
                question_data.append(future.result())
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(generate_single_question, r, question_num) for question_num in range(1, n + 1)]
            # 查看当前活跃的线程数量
            print(f"当前活跃的线程数: {threading.active_count()}")
            for future in concurrent.futures.as_completed(futures):
                question_data.append(future.result())

    # 按题号对生成的题目和答案排序
    question_data.sort(key=lambda x: x[0])

    # 将生成的题目和答案写入文件中
    with open("file\\Exercise.txt", 'a', encoding="UTF-8") as fp1, open("file\\Answer.txt", 'a', encoding="UTF-8") as fp2:
        for _, question_text, answer_text in question_data:
            fp1.write(question_text)
            fp2.write(answer_text)

    # 如果启用了答题模式
    if answer_mode:
        for question_num, question_text, answer_text in question_data:
            answer = input(f"({question_num}){question_text.strip()} ")
            # 将用户输入的答案转换为 Fraction 类型
            answer = mixed_to_fraction(answer)
            # 解析正确答案
            correct_answer = mixed_to_fraction(answer_text.split(". ")[1].strip())
            # 判断用户答案是否正确
            if answer == correct_answer:
                print("√")  # 如果正确，打印 √
                correct_answers += 1  # 正确答题数加 1
            else:
                print(f"× | The correct answer is: {fraction_to_mixed(correct_answer)}")
                wrong_answers += 1  # 错误答题数加 1

        print(f"正确题目数：{correct_answers}\n错误题目数：{wrong_answers}")
    else:
        # 否则，提示生成已完成
        print("生成已经完成！")

        # 结束时间
    end_time = time.time()
    # 计算执行时间
    elapsed_time = end_time - start_time
    print(f"耗时: {elapsed_time:.2f} s")


## 单线程模式
# def answer_questions(r, n, answer_mode=False):
#     """
#     生成并解答随机的数学题目，将题目和答案分别保存到文件中。
#     :param r: 操作数的最大值
#     :param n: 题目数量
#     :param answer_mode: 是否启用用户答题模式，True 为启用答题模式
#     """
#     correct_answers = 0  # 用于统计用户正确答题数
#     wrong_answers = 0  # 用于统计用户错误答题数
#     # 计时
#     start_time = time.time()
#     # 清空已有的题目和答案文件
#     with open("file\\Exercise.txt", 'w', encoding="UTF-8"), open("file\\Answer.txt", 'w', encoding="UTF-8"):
#         pass  # 占位操作，目的是清空文件内容
#
#     # 打开题目和答案文件，准备写入新题目和答案
#     with open("file\\Exercise.txt", 'a', encoding="UTF-8") as fp1, open("file\\Answer.txt", 'a',
#                                                                         encoding="UTF-8") as fp2:
#         for question_num in range(1, n + 1):  # 生成 n 道题目
#             print("\r", end="")
#             progress = int((question_num / n) * 50)  # 计算进度条长度（50个字符）
#             percentage = (question_num / n) * 100  # 计算百分比
#             print("Progress: {:.2f}%: ".format(percentage), "▋" * progress + " " * (50 - progress), end="")
#             sys.stdout.flush()
#             while True:
#                 try:
#                     # 生成一个新的问题对象
#                     question = Question()
#                     question.generate_question(r)  # 生成题目，最大操作数为 r
#                 except ValueError:
#                     # 如果题目结果为负数，重新生成
#                     continue
#                 break
#
#             # 将生成的题目写入文件中
#             fp1.write(f"{question_num}. {question.string_ver} = \n")
#             # 将答案转换为带分数形式并写入答案文件中
#             fp2.write(f"{question_num}. {fraction_to_mixed(question.result)}\n")
#
#             # 如果启用了答题模式
#             if answer_mode:
#                 # 提示用户输入答案
#                 answer = input(f"({question_num}){question.string_ver} = ")
#                 # 将用户输入的答案转换为 Fraction 类型
#                 answer = mixed_to_fraction(answer)
#                 # 判断用户答案是否正确
#                 if answer == question.result:
#                     print("√")  # 如果正确，打印 √
#                     correct_answers += 1  # 正确答题数加 1
#                 else:
#                     # 如果错误，显示正确答案并打印 ×
#                     print(f"× | The correct answer is: {fraction_to_mixed(question.result)}")
#                     wrong_answers += 1  # 错误答题数加 1
#
#     # 如果是答题模式，输出正确和错误题目数
#     if answer_mode:
#         print(f"正确题目数：{correct_answers}\n错误题目数：{wrong_answers}")
#     else:
#         # 否则，提示生成已完成
#         print("生成已经完成！")
#
#         # 结束时间
#     end_time = time.time()
#     # 计算执行时间
#     elapsed_time = end_time - start_time
#     print(f"耗时: {elapsed_time:.2f} s")



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

    # 读取题目和答案文件的行数，以便计算总进度
    with open(exercise_file, 'r', encoding="UTF-8") as fp1, open(answer_file, 'r', encoding="UTF-8") as fp2:
        total_lines = sum(1 for _ in fp1)  # 计算题目行数
        fp1.seek(0)  # 重置文件指针到开头
        fp2.seek(0)  # 重置文件指针到开头

        counter = 1  # 题目编号计数器
        exe_line = fp1.readline()  # 读取一行题目
        ans_line = fp2.readline()  # 读取一行答案

        while exe_line and ans_line:
            # 提取出题目中的表达式部分
            exe_line = exe_line[exe_line.index('. ') + 1:-3]
            # 提取出答案部分，并将其转换为 Fraction 类型
            ans_line = ans_line[ans_line.index('. ') + 1:]
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

            # 更新进度条
            print("\r", end="")
            progress = int((counter / total_lines) * 50)  # 进度条长度为20个字符
            percentage = (counter / total_lines) * 100  # 计算百分比
            print("校对进度: {:.2f}%: ".format(percentage), "▋" * progress + " " * (50 - progress), end="")
            sys.stdout.flush()

            # 读取下一行题目和答案
            exe_line = fp1.readline()
            ans_line = fp2.readline()
            counter += 1  # 题号加 1

    # 将结果写入成绩文件
    with open("file\\Grade.txt", 'w', encoding="UTF-8") as fp:
        fp.write(f"Correct: {correct_answers} {tuple(correct_list)}\n")  # 写入正确答案信息
        fp.write(f"Wrong: {wrong_answers} {tuple(wrong_list)}\n")  # 写入错误答案信息
    print("输出结果已写入file文件夹中的Grade.txt")

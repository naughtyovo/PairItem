import unittest
from file_operations import answer_questions,check_answer  # 假设你的函数在这个模块中


class TestAnswerQuestions(unittest.TestCase):
    def test_basic_function(self):
        # 测试生成10个题目
        r = 10  # 操作数的最大值
        n = 10  # 题目数量
        answer_questions(r, n)
        # 这里可以添加检查文件内容的代码来验证是否正确生成了题目

    def test_large_number_of_questions(self):
        # 测试生成大量题目
        r = 100
        n = 5000
        answer_questions(r, n)
        # 验证文件内容或性能（可能需要单独的性能测试工具）

    def test_zero_questions(self):
        # 测试生成0个题目
        r = 10
        n = 0
        answer_questions(r, n)
        # 验证没有生成文件内容

    # 注意：答题模式需要手动测试或模拟输入


class TestCheckAnswer(unittest.TestCase):
    def setUp(self):
        ExerciseTestfile_path = "E:\python project\PairItem\Four_Basic_Operations\\file\ExerciseTest.txt"
        AnswerTestfile_path = "E:\python project\PairItem\Four_Basic_Operations\\file\AnswerTest.txt"
        grade_file_path = "E:\python project\PairItem\Four_Basic_Operations\\file\Grade.txt"

        # 使用'w'模式打开文件，这将清空文件内容（如果文件已存在）
        # 或者创建一个新文件（如果文件不存在）
        with open(grade_file_path, 'w') as grade_file:
            pass
        with open(ExerciseTestfile_path, 'r', encoding='utf-8') as file:
            self.ExerciseTestfile_content = file.readlines()
            pass
        with open(AnswerTestfile_path, 'r', encoding='utf-8') as file:
            self.AnswerTestfile_content = file.readlines()
            pass

    def test_basic_function(self):
        # 假设已经有两个文件：Exercise.txt 和 Answer.txt，包含正确和错误的答案
        exercise_file = self.ExerciseTestfile_content
        answer_file = self.AnswerTestfile_content
        check_answer("E:\python project\PairItem\Four_Basic_Operations\\file\ExerciseTest.txt", "E:\python project\PairItem\Four_Basic_Operations\\file\AnswerTest.txt")
        # 验证Grade.txt文件的内容是否正确

    def test_empty_files(self):
        # 测试空文件
        with open("E:\python project\PairItem\Four_Basic_Operations\\file\Exercise_emptyTest.txt", 'w') as fp:
            pass
        with open("E:\python project\PairItem\Four_Basic_Operations\\file\Answer_emptyTest.txt", 'w') as fp:
            pass
        check_answer("E:\python project\PairItem\Four_Basic_Operations\\file\Exercise_emptyTest.txt", "E:\python project\PairItem\Four_Basic_Operations\\file\Answer_emptyTest.txt")
        # 验证Grade.txt文件的内容（应该显示没有题目）Four_Basic_Operations

    if __name__ == '__main__':
            unittest.main()
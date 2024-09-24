import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from main_2 import get_arguments, run_cmd_mode

class TestMainFunctions(unittest.TestCase):

    @patch('main_2.answer_questions')  # Mock answer_questions
    @patch('main_2.check_answer')  # Mock check_answer
    def test_run_cmd_mode_generate_questions(self, mock_check_answer, mock_answer_questions):
        # 模拟命令行参数
        test_args = ['main.py', '-n', '5', '-r', '10']
        with patch.object(sys, 'argv', test_args):
            run_cmd_mode()
            mock_answer_questions.assert_called_once_with(10, 5, False)

    @patch('main_2.answer_questions')
    @patch('main_2.check_answer')
    def test_run_cmd_mode_check_answers(self, mock_check_answer, mock_answer_questions):
        # 模拟命令行参数
        test_args = ['main.py', '-e', 'questions.txt', '-a', 'answers.txt']
        with patch.object(sys, 'argv', test_args):
            run_cmd_mode()
            mock_check_answer.assert_called_once_with('questions.txt', 'answers.txt')

    @patch('builtins.print')
    @patch('os.system')
    def test_run_cmd_mode_missing_argument(self, mock_os_system, mock_print):
        # 模拟命令行参数缺失
        test_args = ['main.py']
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):  # 期望程序退出
                run_cmd_mode()
            mock_print.assert_called_once_with("Argument '-r' is needed!")  # 确保输出了错误信息
            mock_os_system.assert_called_once_with("pause")  # 确保调用了暂停

    def test_get_arguments(self):
        # 测试命令行参数解析
        test_args = ['main.py', '-n', '5', '-r', '10']
        with patch.object(sys, 'argv', test_args):
            args = get_arguments()
            self.assertEqual(args.n, 5)
            self.assertEqual(args.r, 10)
            self.assertFalse(args.m)  # 默认是 False

    def test_get_arguments_invalid_input(self):
        # 测试命令行参数解析无效输入
        test_args = ['main.py', '-n', 'x', '-r', 'x']

        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):  # argparse 会调用 sys.exit()
                get_arguments()


if __name__ == '__main__':
    unittest.main()
# cmd
import argparse
import os
import sys

from question import Question  # 引入生成数学题目的 Question 类
from file_operations import answer_questions, check_answer  # 引入生成题目和检查答案的功能

def get_arguments():
    """
    解析命令行参数，返回包含参数的命名空间对象。
    参数包括生成题目的数量、最大数值、是否启用答题模式、题目文件路径、答案文件路径等。
    """
    parser = argparse.ArgumentParser(
        description="Usage Example: python main.py -n 3 -r 10",  # 描述程序用途
        epilog="若需要使用判题功能，请勿输入-r参数"  # 在帮助信息末尾显示的额外信息
    )
    # 添加命令行参数
    parser.add_argument('-n', type=int, help="生成题目的个数（默认为10）")
    parser.add_argument('-r', type=int, help="题目中的最大数值")
    parser.add_argument('-m', action='store_true', help="启用答题模式（默认关闭）")
    parser.add_argument('-e', type=str, help="题目文件路径")
    parser.add_argument('-a', type=str, help="答案文件路径")
    return parser.parse_args()  # 返回解析后的命名空间对象

if __name__ == '__main__':
    args = get_arguments()  # 获取命令行参数
    if args.n:  # 如果提供了题目数量参数
        n = args.n
    else:
        n = 10  # 如果未提供题目数量，则默认生成 10 道题目
    if args.r:  # 如果提供了最大数值参数
        r = args.r
        m = args.m if args.m else False  # 判断是否启用了答题模式，默认关闭
        answer_questions(r, n, m)  # 调用生成题目的函数
    elif args.e and args.a:  # 如果提供了题目文件路径和答案文件路径
        check_answer(args.e, args.a)  # 调用检查答案的函数
    else:
        print("Argument '-r' is needed!")  # 如果没有提供必要参数，输出错误信息
        os.system("pause")  # 暂停程序等待用户输入，防止窗口立即关闭
        sys.exit  # 退出程序

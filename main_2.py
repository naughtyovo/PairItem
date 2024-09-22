# cmd or GUI

import argparse
import os
import sys
import tkinter as tk
from tkinter import messagebox

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

def run_cmd_mode():
    """
    运行命令行模式，通过解析参数并生成题目或检查答案。
    """
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
        sys.exit()  # 退出程序

def run_gui_mode():
    """
    运行图形化界面模式，用户可以通过界面输入生成题目或答案。
    """
    def generate_questions():
        """
        生成题目并将其显示在图形界面的文本框中，同时生成对应的答案。
        """
        try:
            n = int(entry_n.get())  # 获取用户输入的题目数量
            r = int(entry_r.get())  # 获取用户输入的最大数值
            answer_mode = var_answer_mode.get()  # 获取用户是否启用答题模式的选择

            # 清空文本框内容
            text_output.delete(1.0, tk.END)
            # 调用生成题目函数，并根据用户选择的模式生成题目或答案
            answer_questions(r, n, answer_mode)

            # 读取生成的题目和答案文件，并显示在文本框中
            with open("file/Exercise.txt", 'r', encoding="UTF-8") as f:
                text_output.insert(tk.END, f.read())  # 将生成的题目写入文本框
            with open("file/Answer.txt", 'r', encoding="UTF-8") as f:
                text_output.insert(tk.END, f"\n\nAnswers:\n{f.read()}")  # 将生成的答案写入文本框

        except ValueError:
            messagebox.showerror("输入错误", "请确保输入的是有效的数字。")  # 如果输入的不是有效数字，则弹出错误消息框

    # 创建主窗口
    root = tk.Tk()
    root.title("四则运算生成器")  # 设置窗口标题
    root.geometry("600x400")  # 设置窗口尺寸

    # 题目数量输入框
    label_n = tk.Label(root, text="题目数量 (n):")
    label_n.pack()
    entry_n = tk.Entry(root)
    entry_n.pack()

    # 最大数值输入框
    label_r = tk.Label(root, text="最大数值 (r):")
    label_r.pack()
    entry_r = tk.Entry(root)
    entry_r.pack()

    # 答题模式选项（复选框）
    var_answer_mode = tk.IntVar()  # 用于存储复选框的值
    check_answer_mode = tk.Checkbutton(root, text="启用答题模式", variable=var_answer_mode)  # 答题模式复选框
    check_answer_mode.pack()

    # 生成题目按钮
    button_generate = tk.Button(root, text="生成题目", command=generate_questions)  # 点击按钮后调用生成题目的函数
    button_generate.pack()

    # 输出区域（用于显示生成的题目和答案）
    text_output = tk.Text(root, height=15, width=70)
    text_output.pack()

    # 启动图形化界面的主循环
    root.mainloop()

if __name__ == '__main__':
    # 判断是否传入命令行参数，如果有参数，则运行命令行模式；否则运行图形化界面
    if len(sys.argv) > 1:
        run_cmd_mode()  # 运行命令行模式
    else:
        run_gui_mode()  # 启动图形化界面



#c测试命令：
# python main_2.py -n 99999 -r 9
# python main_2.py -e C:\Users\ZHENG\PycharmProjects\四则运算\file\Exercise.txt -a C:\Users\ZHENG\PycharmProjects\四则运算\file\Answer.txt

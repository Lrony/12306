# coding:utf-8
# 工具类

from colorama import init, Fore

init()

"""
输出错误信息（红色）
"""
def print_error_info(info):
    print("\n", Fore.RED +  info + Fore.RESET, "\n")

"""
反转list
"""
def list_reverse(list):
    # 反转k，v形成新的字典
    return {v: k for k, v in list.items()}
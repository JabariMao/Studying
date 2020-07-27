import os.path
import sys
import time

# 路径 os.path

# os.makedirs("test")  # 创建目录
# os.rename("test", "try")  # 重命名文件或路径
# os.path.basename()  # 返回文件名

# print(os.path.abspath("try"))  # 返回绝对路径
# os.path.exists()  # 判断路径是否存在
# os.path.getsize()  # 返回文件大小

# os.path.join()  # 把路径和文件名合成目录
# os.path.normpath()  # 根据系统规范路径
# os.path.split()  # 分割文件名和路径

# 内置函数
filter()  # 过滤序列
new_list = filter(lambda x: x % 2 == 1, [1, 2, 3, 4, 5, 6, 7, 8, 9])

iter()

open()
"""
r :只读
rb : 二进制打开
r+ :打开一个文件用于读写
w：只用于写入
"""
f = open()
f.read()
f.write()
f.readline()
f.close()



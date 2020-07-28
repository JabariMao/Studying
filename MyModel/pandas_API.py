import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 创建DataFrame的方式
# 1.字典创建
df1 = pd.DataFrame(data={"第一列": [1, 2, 3],
                         "第二列": [4, 5, 6],
                         "第三列": [7, 8, 9]})

# 2.numpy创建
df2 = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=["第一列", "第二列", "第三列"])

# 3.随机创建
df3 = pd.DataFrame(data=np.random.randn(10, 10), columns=[
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
print(df3)

# DataFrame常用属性
print(df1.columns)  # 列标题列表
print(df1.axes)  # 轴标题列表
print(df1.shape)  # 行数*列数
print(df1.ndim)  # 维数
print(df1.size)  # 返回元素数量
print(df1.values)  # 以numpy形式返回数据中的数据
print(df1.index)  # 返回index
print(df1.dtypes)  # 返回数据类型

# DataFrame常用方法
df1.abs()  # 返回所有数据的绝对值
df1.drop_duplicates()  # 删除重复值
df1.dropna()  # 删除空值
df1.isnull()  # 检测空值
df1.notnull()  # 检测非空值
df1.info()  # 返回数据类型
print(df1.iloc[:3])  # 根据序号定位
print(df1.loc[:"第一列"])
print(df1["第一列"].value_counts())  # 计算某一列每个值出现的次数
df1.select_dtypes(include="float64")  # 返回满足条件的数据类型
print(df1.empty)  # 判断data_frame是否为空
print(df1.insert())


# DataFrame修改列名
df1.rename(columns={"第一列": "第1列", "第二列": "第2列", "第三列": "第3列"}, inplace=True)

df2.rename(columns=lambda x: x.replace(
    "列", "个"), inplace=True)  # 用lambda表达式更改列名

# 将连续值分为离散值 pd.cut()
df3["k"] = pd.cut(x=df3['a'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                  labels=["one", "two", "three", "four", "five"])
df3["k"].hist()
plt.show()

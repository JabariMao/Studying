import pandas as pd
import numpy as np

# 创建DataFrame的方式
# 1.字典创建
df1 = pd.DataFrame(data={"第一列": [1, 2, 3],
                         "第二列": [4, 5, 6],
                         "第三列": [7, 8, 9]})

# 2.numpy创建
df2 = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=["第一列", "第二列", "第三列"])

# DataFrame常用属性
print(df1.columns)  # 列标题列表
print(df1.axes)  # 轴标题列表
print(df1.shape)  # 行数*列数
print(df1.ndim)  # 维数
print(df1.size)  # 返回元素数量
print(df1.values)  # 以numpy形式返回数据中的数据

# DataFrame常用方法
df1.abs()  # 返回所有数据的绝对值
df1.drop_duplicates()  # 删除重复值
df1.dropna()  # 删除空值
df1.isnull()  # 检测空值
df1.notnull()  # 检测非空值
df1.info()
print(df1.iloc[:3])  # 根据序号定位
print(df1.loc[:"第一列"])

# DataFrame修改列名
df1.rename(columns={"第一列": "第1列", "第二列": "第2列", "第三列": "第3列"}, inplace=True)

df2.rename(columns=lambda x: x.replace("列", "个"), inplace=True)  # 用lambda表达式更改列名

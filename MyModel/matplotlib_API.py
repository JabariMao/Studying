import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置绘图风格
plt.style.use('ggplot')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False


# 第一种：面向对象样式

value = np.linspace(0, 2, 100)
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(x=value, # x值
        y=value, # y值
        label='linear', #series的名称
        linestyle="-", # 折线的风格
        color="steelblue", # 折线的颜色
        marker="o", # 点的形状
        markersize=6, # 点的大小
        markeredgecolor="black", # 点的边框的颜色
        markerfacecolor="steelblue" # 点的填充色

        )  # Plot some data on the axes.
ax.set_title("这是第一张图")
# Plot more data on the axes...
ax.plot(x=value, y=value**2, label='quadratic')
ax.plot(x=value, y=value**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.


# 第二种：pyplot 风格
value = np.linspace(0, 2, 100)

# Plot some data on the (implicit) axes.
plt.plot(x=value, y=value, label='linear')
plt.plot(x=value, y=value**2, label='quadratic')  # etc.
plt.plot(x=value, y=value**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()

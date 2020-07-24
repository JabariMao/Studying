import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 第一种：面向对象样式

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [5, 6, 7, 8])
fig.show()


# 第二种：pyplot 风格
x = np.linspace(0, 2, 100)

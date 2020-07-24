# 监督学习
# Linear Model 线性模型
# %%
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# 获取sklearn库中的数据
data_X, data_y = datasets.load_diabetes(return_X_y=True)

# 将数据分为训练集和测试集
train_X = data_X[:-20]
train_y = data_y[:-20]
test_X = data_X[-20:]
test_y = data_y[-20:]

# 开始预测
reg = LinearRegression()
reg.fit(X=train_X, y=train_y)

# 用测试集的X进行预测，返回y
pred_y = reg.predict(test_X)

# 对模型进行检验
print(reg.coef_)  # 返回相关系数

# 最小二乘法
mse = mean_squared_error(test_y, pred_y)
print(mse)

# r2估计
r2 = r2_score(test_y, pred_y)
print(r2)


# 可视化
plt.scatter(x=train_X, y=train_y, color="black")
plt.plot(test_X, pred_y, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()


# %%

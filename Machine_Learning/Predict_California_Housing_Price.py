# %%[markdown]
# **导包**
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from pandas.plotting import scatter_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# %%[markdown]
# **加载数据**
path = r"E:\Git_Workplace\handson-ml2\datasets\housing\housing.csv"
housing = pd.read_csv(path)

# %%[markdown]
# **查看数据基本信息**
# %%
housing.head()
# %%
housing.info()
# %%
housing.isnull().sum()
# %%
housing["ocean_proximity"].value_counts()
# %%[markdown]
# **描述性统计**
housing.describe()
# 每个属性作图
housing.hist(bins=50, figsize=(20, 15))
# %% 设置训练集和测试集(普通随机抽样)
train_data, test_data = train_test_split(housing, test_size=0.2, random_state=42)

# %%[markdown]
# **更进一步考虑抽样方式，普通抽样可能会导致抽样偏差，所以采用分层抽样，考虑每个类别的比例，按照比例对样本进行抽样，这样抽取的测试集可以很好的反应全体样本的真实情况。**
housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0, 1.2, 3.0, 4.5, 6.0, np.inf],
                               labels=[1, 2, 3, 4, 5])
housing["income_cat"].hist()

# 根据收入的不同类别进行分层抽样
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]
strat_test_set["income_cat"].value_counts() / len(strat_test_set)

for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

# %%[markdowm]
# **开始探索数据**
housing = strat_train_set.copy()
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)

# %%
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
             s=housing["population"] / 100, label="population", figsize=(10, 7),
             c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True)
plt.legend()

# %%[markdowm]
# **计算标准相关系数**
corr_matrix = housing.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)

# %%
attributes = ["median_house_value", "median_income",
              "total_rooms", "housing_median_age"]
scatter_matrix(housing[attributes], figsize=[12, 8])

# %%
housing.plot(kind="scatter", x="median_income",
             y="median_house_value", alpha=0.1)

# %%
housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"] / \
                               housing["total_rooms"]
housing["population_per_household"] = housing["population"] / \
                                      housing["households"]
# %%

corr_matrix = housing.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)

# %%
# 准备数据
housing = strat_train_set.drop(columns=["median_house_value"], axis=1)
housing_labels = strat_train_set["median_house_value"].copy()
median = housing["total_bedrooms"].median()
housing["total_bedrooms"].fillna(median, inplace=True)

# %%
# 用scikit-leran处理空值
imputer = SimpleImputer(strategy="median")
housing_num = housing.drop(columns=["ocean_proximity"], axis=1)
imputer.fit(housing_num)
imputer.statistics_
# %%
X = imputer.transform(housing_num)
housing_tr = pd.DataFrame(X, columns=housing_num.columns, index=housing_num.index)

# %%
# 处理分类数据
housing_cat = housing[["ocean_proximity"]]
ordinal_encoder = OrdinalEncoder()
housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)

# %%
ordinal_encoder.categories_

# %%
# one-hot encoding
cat_encoder = OneHotEncoder()
housing_cat_1hot = cat_encoder.fit_transform(housing_cat)
housing_cat_1hot.toarray()

# %%
# 特征缩放
num_pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")),
                         ("std_scaler", StandardScaler())])
housing_num_tr = num_pipeline.fit_transform(housing_num)

# %%
num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]

full_pipeline = ColumnTransformer([("num", num_pipeline, num_attribs),
                                   ("cat", OneHotEncoder(), cat_attribs)
                                   ])
housing_prepared = full_pipeline.fit_transform(housing)

# %%
# 开始预测
lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

# %%
some_data = housing.iloc[:5]
some_labels = housing_labels.iloc[:5]
some_data_prepared = full_pipeline.transform(some_data)
lin_reg.predict(some_data_prepared)

# %%
list(some_labels)

# %%
housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
lin_rmse

# %%

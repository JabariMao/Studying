"""
@产业自动出数
@Author: Jabori
@主要内容说明：
一、数据清洗部分
    1.drop_and_fill():去除重复值和填充空值，数字填充0，字符串填充“无”。
    2.each_prod_total_sales()；每个产品的总销售额。
    3.each_prod_total_amount():每个产品的总销售量。
    4.each_prod_average_price()；每个产品的平均价格。
    5.extract_category():提取某些特殊种类的数据。
    6.extract_prod_g()；从产品详情字段提取产品规格，并添加“prod_g"字段。
    7.prod_each_g_price()：计算产品每斤的平均价格，并添加“prod_each_g_price”字段。
二、计算部分
    1.total_sales_and_total_amount()：计算总销售额和总销售量
    2.shop_rank()：计算店铺排名。
    3.brand_rank():计算品牌排名。
    4.prod_rank():计算单品排名。
    5.weight_range():计算不同规格区间产品的占比。
    6.price_range():计算不同价格区间产品的占比。
    7.province_rank():计算省份排名。
    8.month_average_price()：计算每个月的平均价格变动。
    9.month_average_500_price():计算每个月的平均价格变动，根据每斤价格。
    10.high_frequency_word_in_prod_name():统计商品名称中的高频词。
    11.channel_distribution():渠道分布。未完成。
    12.second_address_rank():计算某个省的市州排名。
    13.the_total_amount_of_shop_in_different_price_range():计算不同价格区间的店铺的个数。
"""

import pandas as pd
import numpy as np
import time
import re
import os
import psycopg2
import jieba


def month_list(types, num):
    month_money_list = {"03": ["month_money_01", "month_money_02", "month_money_03"],
                        "06": ["month_money_01", "month_money_02", "month_money_03", "month_money_04",
                               "month_money_05",
                               "month_money_06"],
                        "09": ["month_money_01", "month_money_02", "month_money_03", "month_money_04",
                               "month_money_05",
                               "month_money_06", "month_money_07", "month_money_08", "month_money_09"],
                        "12": ["month_money_01", "month_money_02", "month_money_03", "month_money_04",
                               "month_money_05",
                               "month_money_06", "month_money_07", "month_money_08", "month_money_09",
                               "month_money_10",
                               "month_money_11", "month_money_12"]}
    month_amount_list = {"03": ["month_amount_01", "month_amount_02", "month_amount_03"],
                         "06": ["month_amount_01", "month_amount_02", "month_amount_03", "month_amount_04",
                                "month_amount_05",
                                "month_amount_06"],
                         "09": ["month_amount_01", "month_amount_02", "month_amount_03", "month_amount_04",
                                "month_amount_05", "month_amount_06", "month_amount_07", "month_amount_08",
                                "month_amount_09"],
                         "12": ["month_amount_01", "month_amount_02", "month_amount_03", "month_amount_04",
                                "month_amount_05", "month_amount_06", "month_amount_07", "month_amount_08",
                                "month_amount_09", "month_amount_10", "month_amount_11", "month_amount_12"]}
    month_commentnum_as_amount = {"03": ["month_commentnum_01", "month_commentnum_02", "month_commentnum_03"],
                                  "06": ["month_commentnum_01", "month_commentnum_02", "month_commentnum_03",
                                         "month_commentnum_04",
                                         "month_commentnum_05",
                                         "month_commentnum_06"],
                                  "09": ["month_commentnum_01", "month_commentnum_02", "month_commentnum_03",
                                         "month_commentnum_04",
                                         "month_commentnum_05", "month_commentnum_06", "month_commentnum_07",
                                         "month_commentnum_08",
                                         "month_commentnum_09"],
                                  "12": ["month_commentnum_01", "month_commentnum_02", "month_commentnum_03",
                                         "month_commentnum_04",
                                         "month_commentnum_05", "month_commentnum_06", "month_commentnum_07",
                                         "month_commentnum_08",
                                         "month_commentnum_09", "month_commentnum_10", "month_commentnum_11",
                                         "month_commentnum_12"]}
    if types == "money":
        return month_money_list[num]
    elif types == "amount":
        return month_amount_list[num]
    elif types == "commentnum":
        return month_commentnum_as_amount[num]


def sql_query(sql_name,
              result_name,
              output_path,
              sql_path=r"C:\Users\maojiangbo\Documents\Navicat\PostgreSQL\servers\pg.sunsharp.cn_5432\warehouse"):
    path = str(sql_path + "/" + sql_name).replace("\\", "/")
    sql_file = open(path, 'r', encoding="utf-8")
    sql_txt = sql_file.readlines()
    sql_file.close()
    sql_content = "".join(sql_txt)
    print(sql_content)
    conn = psycopg2.connect(database="warehouse", user=r"maojiangbo", password=r"sAoGtBmancLr", host=r"pg.sunsharp.cn",
                            port="5432")
    print("数据库连接成功")
    print("=============")
    query = sql_content
    print("正在查询...")
    start = time.time()
    data = pd.read_sql_query(query, conn)
    end = time.time()
    print("查询结束，共耗时：" + str(round(end - start, 3)) + " 秒")
    print("查询成功, 共查询出{0}条数据".format(data.shape[0]))
    result_path = output_path.replace("\\", "/") + "/" + result_name
    data.to_excel(result_path)
    print("数据写入成功: {0}".format(result_path))
    return data


# 数据处理
class DataProcess:
    def __init__(self, root_path, file_name, industry, month_amount_list, month_money_list):
        self.month_amount_list = month_amount_list
        self.month_money_list = month_money_list
        self.root_path = root_path
        self.industry = industry
        self.file_name = file_name
        self.file_path = str(self.root_path + "/" + self.file_name).replace("\\", "/")
        # 读取文件
        print("数据集目录： {0}".format(self.file_path))
        print("------------------------------------")
        if os.path.splitext(self.file_name)[1] == ".csv":
            self.data = pd.read_csv(self.file_path)
            print("{0}  读取成功".format(self.file_name))
            print("------------------------------------")
        elif (os.path.splitext(self.file_name)[1] == ".xlsx") | (os.path.splitext(self.file_name)[1] == ".xls"):
            self.data = pd.read_excel(self.file_path)
            print("{0}  读取成功".format(self.file_name))
            print("------------------------------------")
        # 创建结果目录
        self.result_path = str(self.root_path + "/" + self.industry + "_结果").replace("\\", "/")
        path_exist = os.path.exists(self.result_path)
        if path_exist:
            print("目录已存在，结果目录: {0}".format(self.result_path))
            print("------------------------------------")
        else:
            os.mkdir(self.result_path)
            print("目录不存在，创建结果目录: {0}".format(self.result_path))
            print("------------------------------------")

    # 去除重复值和填充空值
    def drop_and_fill(self):
        """去除重复值和填充空值"""
        # 去除重复值
        start = self.data.shape[0]
        print("原始数据共有： {0} 行".format(start))
        self.data.drop_duplicates(inplace=True)
        end = self.data.shape[0]
        print("去重后数据共有 : {0} 行, 共删除{1}行".format(end, (start - end)))
        self.data.reset_index(drop=True)

        # 填充空值
        for i in range(0, len(self.data.columns)):
            if self.data[self.data.columns[i]].isnull().sum() == 0:
                continue
            else:
                if self.data.iloc[:, i].dtype == "float64":
                    self.data[self.data.columns[i]].fillna(0, inplace=True)
                elif self.data.iloc[:, i].dtype == "object":
                    self.data[self.data.columns[i]].fillna("无", inplace=True)

        print("重复值去除完成。\n空值填充完成。")
        print("------------------------------------")
        return self.data

    def each_prod_total_sales(self):
        """计算每个产品的总销售额"""
        self.data['each_prod_total_sales'] = self.data[self.month_money_list].apply(np.sum, axis=1)
        print("产品共 {0} 个月的销售额之和计算完成。".format(len(self.month_money_list)))
        print("------------------------------------")
        return self.data

    def each_prod_total_amount(self):
        """计算每个产品的总销售量"""
        # 计算每个产品1-5月的销售量之和
        self.data['each_prod_total_amount'] = self.data[self.month_amount_list].apply(np.sum, axis=1)
        print("产品共{0}个月的销售量之和计算完成。".format(len(self.month_amount_list)))
        print("------------------------------------")
        return self.data

    def each_prod_average_price(self):
        """计算每个产品的平均价格"""
        # 计算每个产品的单价
        self.data["each_prod_average_price"] = self.data["each_prod_total_sales"] / self.data["each_prod_total_amount"]
        print("产品平均单价计算完成")
        print("------------------------------------")
        return self.data

    def extract_category(self, match_word, columns="prod_name", stop_word=None, output=False):
        # name_list = self.data[columns]
        # print(name_list)
        if stop_word:
            match_result = self.data[(self.data[columns].str.contains(match_word) == True) &
                                     (self.data[columns].str.contains(stop_word) == False)]
        else:
            match_result = self.data[(self.data[columns].str.contains(match_word) == True)]

        if output:
            self.write_to_excel(data=match_result, name="{0} 提取结果".format(self.result_path))
            return match_result
        else:
            return match_result

    def extract_prod_g(self):
        """提取产品规格"""
        field = self.data["prod_detail"]
        prod_g = []
        for i in range(0, len(field)):
            g = re.search(pattern=r"\{?\"?[\u4e00-\u9fa5]{3}\".\"\d{2,5}[g]{1}\"\}", string=field[i])
            if g:
                result = re.search(pattern=r"\d{1,5}", string=g.group(0))
                prod_g.append(result.group(0))
            else:
                prod_g.append("0")
        self.data['prod_g'] = prod_g
        # self.data = self.data[self.data["prod_g"] != "无"]
        # self.data.reset_index(drop=True, inplace=True)
        # self.data.copy()
        self.data['prod_g'] = self.data["prod_g"].astype("float64")
        print("产品重量提取完成。")
        return self.data

    def prod_each_g_price(self):
        """每个产品每斤的平均价格"""
        g_price = []
        for i in range(0, len(self.data)):
            if self.data["prod_g"][i] == 0:
                g_price.append(0)
            else:
                price = self.data["each_prod_average_price"][i] / self.data["prod_g"][i] * 500
                g_price.append(price)
        self.data["prod_each_g_price"] = g_price
        # field = self.data[self.data["prod_g"] != 0]
        # g_price = (field["each_prod_average_price"] / field["prod_g"]) * 500
        # self.data

    # 计算部分==============================================================

    # 总销量和总销售额
    def total_sales_and_amount(self, output=True):
        """计算总销量和总销售额"""
        total_amount = self.data["each_prod_total_amount"].sum()
        total_sales = self.data["each_prod_total_sales"].sum()
        total_result = pd.DataFrame(data=[total_amount, total_sales], index=["总销量", "总销售额"])
        if output:
            self.write_to_excel(data=total_result, name="{0} 总销量和总销售额".format(self.industry))
            return total_result
        else:
            return total_result

    # 店铺top
    def shop_rank(self, output=True):
        """计算店铺的销售额排名"""
        shop_rank_data = self.data.groupby("shop_name")[["each_prod_total_sales"]].sum()
        shop_rank_result = shop_rank_data.sort_values(by="each_prod_total_sales", ascending=False)
        if output:
            self.write_to_excel(data=shop_rank_result, name="{0} 网商排行榜".format(self.industry))
            return shop_rank_result
        else:
            return shop_rank_result

    #  品牌top
    def brand_rank(self, output=True):
        """计算品牌排名"""
        # 全国品牌top10 并且求出每个品牌的价格区间和规格区间
        # 品牌排名
        rank = self.data.groupby("brand_name")[['each_prod_total_sales']].sum()
        rank.rename(columns={"each_prod_total_sales": "总销售额"}, inplace=True)
        # 价格最小值
        brand_price_min = self.data.groupby("brand_name")[["each_prod_average_price"]].min()
        brand_price_min.rename(columns={"each_prod_average_price": "价格最小值"}, inplace=True)
        # print(domestic_brand_price_min.values)
        # 价格最大值
        brand_price_max = self.data.groupby("brand_name")[["each_prod_average_price"]].max()
        brand_price_max.rename(columns={"each_prod_average_price": "价格最大值"}, inplace=True)
        # 规格最小值
        brand_g_min = self.data.groupby("brand_name")[["prod_g"]].min()
        brand_g_min.rename(columns={"prod_g": "规格最小值"}, inplace=True)
        # 规格最大值
        brand_g_max = self.data.groupby("brand_name")[["prod_g"]].max()
        brand_g_max.rename(columns={"prod_g": "规格最大值"}, inplace=True)
        brand_rank_result = pd.concat([rank, brand_price_min, brand_price_max, brand_g_min, brand_g_max], axis=1)
        brand_rank_result = brand_rank_result.sort_values(by="总销售额", ascending=False)
        brand_rank_result = brand_rank_result.drop("无", axis=0)
        if output:
            self.write_to_excel(data=brand_rank_result, name="{0} 品牌排行榜".format(self.industry))
            return brand_rank_result
        else:
            return brand_rank_result

    # 单品top
    def prod_rank(self, output=True):
        """计算单品的销售额排名以及所属店铺"""
        prod_rank_data = self.data.groupby(["prod_name", "shop_name"])[
            ["each_prod_total_sales", "each_prod_average_price"]].sum()
        prod_rank_result = prod_rank_data.sort_values(by="each_prod_total_sales", ascending=False)
        if output:
            self.write_to_excel(data=prod_rank_result, name="{0} 单品top".format(self.industry))
            return prod_rank_result
        else:
            return prod_rank_result

    # 写入excel
    def write_to_excel(self, data, name):
        data.to_excel(self.result_path + "/" + name + ".xlsx")
        print("结果写入目录: {0}.xlsx".format(self.result_path + "/" + name))

    # 不同<规格>区间的产品总销量
    def weight_range(self, weight_nodes, output=True):
        # 全国不同<规格>区间的产品总销量
        g_range = []
        g_amount = []
        g_number = []
        for i in range(0, len(weight_nodes)):
            if i == 0:
                g_range.append(" X < %s" % weight_nodes[i + 1])
                result = self.data[self.data["prod_g"] < weight_nodes[i + 1]]
                amount = result['each_prod_total_amount'].sum()
                number = result.shape[0]
                g_amount.append(amount)
                g_number.append(number)
            elif i == len(weight_nodes) - 1:
                g_range.append(" X >= %s" % (weight_nodes[i]))
                result = self.data[self.data["prod_g"] >= weight_nodes[i]]
                amount = result['each_prod_total_amount'].sum()
                number = result.shape[0]
                g_amount.append(amount)
                g_number.append(number)
            elif i != 0 & i != len(weight_nodes) - 1:
                g_range.append("%s <= X < %s" % (weight_nodes[i], weight_nodes[i + 1]))
                result = self.data[
                    (self.data["prod_g"] >= weight_nodes[i]) & (self.data["prod_g"] < weight_nodes[i + 1])]
                amount = result['each_prod_total_amount'].sum()
                number = result.shape[0]
                g_amount.append(amount)
                g_number.append(number)
        weight_range_result = pd.DataFrame(data={"weight_range": g_range, "amount": g_amount, "number": g_number})
        if output:
            self.write_to_excel(data=weight_range_result, name="{0} 规格区间 ".format(self.industry))
            return weight_range_result
        else:
            return weight_range_result

    def price_range(self, price_nodes, output=True):
        p_range = []
        p_amount = []
        p_price = []
        p_number = []
        for i in range(0, len(price_nodes)):
            if i == 0:
                p_range.append(" X <= %s" % price_nodes[i + 1])
                match_item = self.data[self.data["each_prod_average_price"] <= price_nodes[i + 1]]
                amount = match_item['each_prod_total_amount'].sum()
                price = match_item['each_prod_total_sales'].sum()
                number = match_item.shape[0]
                p_amount.append(amount)
                p_price.append(price)
                p_number.append(number)
            elif i == len(price_nodes) - 1:
                p_range.append(" X > %s" % (price_nodes[i]))
                match_item = self.data[self.data["each_prod_average_price"] > price_nodes[i]]
                amount = match_item['each_prod_total_amount'].sum()
                price = match_item['each_prod_total_sales'].sum()
                number = match_item.shape[0]
                p_amount.append(amount)
                p_price.append(price)
                p_number.append(number)
            elif i != 0 & i != len(price_nodes) - 1:
                p_range.append("%s < X <= %s" % (price_nodes[i], price_nodes[i + 1]))
                match_item = self.data[
                    (self.data["each_prod_average_price"] > price_nodes[i]) & (
                            self.data["each_prod_average_price"] <= price_nodes[i + 1])]
                amount = match_item['each_prod_total_amount'].sum()
                price = match_item['each_prod_total_sales'].sum()
                number = match_item.shape[0]
                p_amount.append(amount)
                p_price.append(price)
                p_number.append(number)
        # price_range_result = pd.DataFrame(data=p_amount, index=p_range, columns=[["range", "amount", "price"]])
        price_range_result = pd.DataFrame(
            data={"price_range": p_range, "amount": p_amount, "price": p_price, "number": p_number})
        if output:
            self.write_to_excel(data=price_range_result, name="{0} 价格区间 ".format(self.industry))
            return price_range_result
        else:
            return price_range_result

    # 省份排名
    def province_rank(self, output=True):
        province_data = self.data.groupby("first_addr")[["each_prod_total_sales"]].sum()
        province_result = province_data.sort_values(by="each_prod_total_sales", ascending=False)
        if output:
            self.write_to_excel(data=province_result, name="{0} 省份排名".format(self.industry))
            return province_result
        else:
            return province_result

    # 月平均价格
    def month_average_price(self, output=True):
        month_money = self.data[self.month_money_list].apply(np.sum, axis=0)
        month_amount = self.data[self.month_amount_list].apply(np.sum, axis=0)
        month_average_price_list = []
        for i in range(0, len(month_money)):
            result = month_money[i] / month_amount[i]
            month_average_price_list.append(result)
        month_average_price_result = pd.DataFrame(data=month_average_price_list,
                                                  index=range(1, len(month_average_price_list) + 1),
                                                  columns=["average_price"])
        if output:
            self.write_to_excel(data=month_average_price_result, name="{0} 月平均价格变动".format(self.industry))
            return month_average_price_result
        else:
            return month_average_price_result

    # 月平均价格变动（平均元/斤）
    def month_average_500_price(self, output=True):
        data = self.data[self.data["prod_g"] != 0]
        each_month_sales = data[self.month_money_list].apply(np.sum, axis=0)
        # each_month_amount = data[self.month_amount_list].apply(np.sum, axis=0)

        print(each_month_sales)
        # print(each_month_amount)
        total_g = data["prod_g"].sum(axis=0)
        print(total_g)
        month_average_500_price_list = []
        for i in range(0, len(each_month_sales)):
            result = (each_month_sales[i] / total_g) * 500
            month_average_500_price_list.append(result)
        print(month_average_500_price_list)
        month_average_500_price_result = pd.DataFrame(data=month_average_500_price_list,
                                                      index=range(1, len(month_average_500_price_list) + 1),
                                                      columns=["每月每斤平均价格"])
        if output:
            self.write_to_excel(data=month_average_500_price_result,
                                name="{0} 每月每斤平均价格".format(self.industry))
        else:
            return month_average_500_price_result

    # 高频词
    def high_frequency_words_in_prod_name(self):
        word = self.data['prod_name']
        words_list = []
        for i in range(0, len(word)):
            words_list.append(word[i])

        name_content = " ".join(words_list)
        name_split = " ".join(jieba.cut(name_content, cut_all=False))
        count_words = name_split.split()
        counts = {}
        for word in count_words:
            counts[word] = counts.get(word, 0) + 1
        items = list(counts.items())
        items.sort(key=lambda s: s[1], reverse=True)
        for j in range(20):
            m, n = items[j]
            print(m, n)

        # font = r"C:\Windows\Fonts\simhei.ttf"
        #
        # word_cloud = WordCloud(font_path=font,
        #                        contour_width=5,
        #                        contour_color="lightblue",
        #                        width=2000,
        #                        height=1000)
        # word_cloud.generate(name_split)
        # word_cloud.to_file(self.result_path + "/" + "{0}词云.png".format(self.industry))

    # 渠道分布
    def channel_distribution(self, area_name: list):
        pass

    # 销售额top20市州
    def second_address_rank(self, output=True):
        second_addr_rank = self.data.groupby("second_addr")[['each_prod_total_sales']].sum()
        second_addr_rank.sort_values(by="each_prod_total_sales", ascending=False, inplace=True)
        if output:
            self.write_to_excel(data=second_addr_rank, name="{0} 市州销售额榜单".format(self.industry))
        else:
            return second_addr_rank

    # 不同销售额区间的网商数量
    def the_total_amount_of_shop_in_different_price_range(self, sales_nodes: list, output=True):
        shop_sales = self.data.groupby("shop_name")[["each_prod_total_sales"]].sum()

        sales_range = []
        shop_number = []
        for i in range(0, len(sales_nodes)):
            if i == 0:
                sales_range.append(" X <= %s" % sales_nodes[i + 1])
                match_item = shop_sales[shop_sales["each_prod_total_sales"] <= sales_nodes[i + 1]]
                number = match_item.shape[0]
                shop_number.append(number)
            elif i == len(sales_nodes) - 1:
                sales_range.append(" X > %s" % (sales_nodes[i]))
                match_item = shop_sales[shop_sales["each_prod_total_sales"] > sales_nodes[i]]
                number = match_item.shape[0]
                shop_number.append(number)
            elif i != 0 & i != len(sales_nodes) - 1:
                sales_range.append("%s < X <= %s" % (sales_nodes[i], sales_nodes[i + 1]))
                match_item = shop_sales[
                    (shop_sales["each_prod_total_sales"] > sales_nodes[i]) & (
                            shop_sales["each_prod_total_sales"] <= sales_nodes[i + 1])]
                number = match_item.shape[0]
                shop_number.append(number)
        # price_range_result = pd.DataFrame(data=p_amount, index=p_range, columns=[["range", "amount", "price"]])
        price_range_result = pd.DataFrame(
            data={"sales_range": sales_range, "shop_number": shop_number})
        if output:
            self.write_to_excel(data=price_range_result, name="{0} 不同零售额区间网商数量 ".format(self.industry))
        else:
            return price_range_result

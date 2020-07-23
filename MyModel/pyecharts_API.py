# -*- coding: utf-8 -*-

from pyecharts import options as opts  # 配置项
from pyecharts.charts import Bar  # 条形图/柱状图
from pyecharts.faker import Faker  # 数据生成

x, y = Faker.choose(), Faker.values()
a = (Bar(init_opts=opts.InitOpts(height="800px",  # 定义高度
                                 width="1600px",  # 定义宽度
                                 theme=opts.global_options.ThemeType.DARK,  # 设置主题
                                 animation_opts=opts.AnimationOpts(animation_delay=1000,
                                                                   animation_easing="elasticOut"),  # 动画设置,

                                 ))
     .add_xaxis(x)
     .add_yaxis(series_name="商品A",  # 系列名称
                y_axis=y,  # 值
                gap="0%",  # 柱间距离
                color=Faker.rand_color()
                )
     .add_yaxis(series_name="商品B",
                y_axis=Faker.values(),
                is_selected=False,  # 默认取消显示某Series
                gap="0%",
                color=Faker.rand_color()
                )
     .reversal_axis()  # 翻转XY轴

     .set_global_opts(title_opts=opts.TitleOpts(title="自定义", subtitle="自定义副标题"),  # 表格标题设置
                      toolbox_opts=opts.ToolboxOpts(is_show=True),  # 工具箱选项
                      legend_opts=opts.LegendOpts(is_show=True),  # 图例选项
                      )
     .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=50, name="yAxis=50")]),  # 标记线
                      markpoint_opts=opts.MarkPointOpts(
                          data=[opts.MarkPointItem(name="自定义标记点", coord=[x[2], y[2]], value=y[2])]),  # 标记点
                      label_opts=opts.LabelOpts(position="right", is_show=True)  # 标签位置
                      )
     .render()  # 渲染
     )

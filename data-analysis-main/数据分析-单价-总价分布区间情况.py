import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Pie


def draw_pie(xlist, ylist, xlist2, ylist2, name):
    # 确认传递给 draw_pie 的数据格式正确
    print("单价数据:", list(zip(xlist, ylist)))
    print("总价数据:", list(zip(xlist2, ylist2)))

    data_pair = [list(z) for z in zip(xlist, ylist)]
    data_pair2 = [list(z) for z in zip(xlist2, ylist2)]

    c = (
        Pie(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
        .set_global_opts(title_opts=opts.TitleOpts(
            title=name
        ),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        .add(
            '广州二手房单价分布图',
            data_pair=data_pair,
            center=["20%", "40%"],
            radius=[60, 90],
        )
        .add(
            '广州二手房总价分布图',
            data_pair=data_pair2,
            center=["60%", "40%"],
            radius=[60, 90],
        )
        .render('./分析图表/' + name + '.html')
    )
    print(f"图表已经保存为 './分析图表/{name}.html'")


def calulate(filenames):
    ydic = {'20000元以下': 0, '20000-30000元': 0, '30000-40000元': 0, '40000-50000元': 0, '50000-60000元': 0,
            '60000-70000元': 0, '70000-80000元': 0, '80000-90000元': 0, '90000-100000元': 0, '100000元以上': 0}
    ydic2 = {'100万以下': 0, '100-200万': 0, '200-300万': 0, '300-400万': 0, '400-500万': 0, '500-600万': 0,
             '600-700万': 0, '700-800万': 0, '800-900万': 0, '900-1000万': 0, '1000万以上': 0}

    for filename in filenames:
        file_path = os.path.join('./爬取结果', filename)
        # 打印文件路径，帮助调试
        print(f"正在处理文件: {file_path}")

        try:
            data = pd.read_csv(file_path, encoding='gb18030', header=None, skip_blank_lines=True)
            if data.empty:
                print(f"警告: 文件 {filename} 为空，跳过该文件。")
                continue  # 如果文件为空，跳过该文件

            data.columns = ['标题', '小区名', '位置', '标签', '关注人数', '发布时间', '房间类型', '面积', '朝向',
                            '装修', '楼层', '年份', '楼况', '总价', '单价']

            # 统计单价分布
            for i in data['单价']:
                try:
                    price = float(i)  # 将价格转换为浮动类型
                    if price <= 20000:
                        ydic['20000元以下'] += 1
                    elif 20000 < price <= 30000:
                        ydic['20000-30000元'] += 1
                    elif 30000 < price <= 40000:
                        ydic['30000-40000元'] += 1
                    elif 40000 < price <= 50000:
                        ydic['40000-50000元'] += 1
                    elif 50000 < price <= 60000:
                        ydic['50000-60000元'] += 1
                    elif 60000 < price <= 70000:
                        ydic['60000-70000元'] += 1
                    elif 70000 < price <= 80000:
                        ydic['70000-80000元'] += 1
                    elif 80000 < price <= 90000:
                        ydic['80000-90000元'] += 1
                    elif 90000 < price <= 100000:
                        ydic['90000-100000元'] += 1
                    elif price > 100000:
                        ydic['100000元以上'] += 1
                except ValueError:
                    print(f"跳过无效单价数据: {i}")
                    continue  # 跳过无效数据

            # 统计总价分布
            for i in data['总价']:
                try:
                    price = float(i)  # 将总价转换为浮动类型
                    if price <= 1000000:
                        ydic2['100万以下'] += 1
                    elif 1000000 < price <= 2000000:
                        ydic2['100-200万'] += 1
                    elif 2000000 < price <= 3000000:
                        ydic2['200-300万'] += 1
                    elif 3000000 < price <= 4000000:
                        ydic2['300-400万'] += 1
                    elif 4000000 < price <= 5000000:
                        ydic2['400-500万'] += 1
                    elif 5000000 < price <= 6000000:
                        ydic2['500-600万'] += 1
                    elif 6000000 < price <= 7000000:
                        ydic2['600-700万'] += 1
                    elif 7000000 < price <= 8000000:
                        ydic2['700-800万'] += 1
                    elif 8000000 < price <= 9000000:
                        ydic2['800-900万'] += 1
                    elif 9000000 < price <= 10000000:
                        ydic2['900-1000万'] += 1
                    elif price > 10000000:
                        ydic2['1000万以上'] += 1
                except ValueError:
                    print(f"跳过无效总价数据: {i}")
                    continue  # 跳过无效数据

        except pd.errors.EmptyDataError:
            print(f"警告: 文件 {filename} 无法读取，跳过该文件。")
            continue  # 如果文件为空或无法读取，跳过该文件

    # 打印分布结果进行验证
    # print("单价分布:", ydic)
    # print("总价分布:", ydic2)

    # 调用绘图函数，生成饼图
    draw_pie(list(ydic.keys()), list(ydic.values()), list(ydic2.keys()), list(ydic2.values()),
             '广州二手房单价-总计分布图')


if __name__ == '__main__':
    # 获取目录下所有文件
    filenames = os.listdir('./爬取结果')
    calulate(filenames)

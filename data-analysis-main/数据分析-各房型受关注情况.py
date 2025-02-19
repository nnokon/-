import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Pie

regions_dic = {'tianhe': '天河', 'yuexiu': '越秀', 'liwan': '荔湾', 'haizhu': '海珠', 'panyu': '番禺', 'baiyun': '白云',
               'huangpu': '黄埔', 'conghua': '从化', 'zengcheng': '增城', 'huadou': '花都', 'nansha': '南沙',
               'nanhai': '南海', 'shunde': '顺德'}

def draw(data):
    c = (
        Pie(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
            .add(
            "",
            [list(z) for z in zip(data.keys(), data.values())]
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="广州二手房各房型受关注情况图"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical")
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render('分析图表/' + "广州二手房各房型受关注情况图.html")
    )

def read_csv():
    room_type_sum = {}
    room_type_cnt = {}
    room_type_avg = {}

    filenames = os.listdir('./爬取结果/')  # 设定调用文件的相对路径
    for i in filenames:
        if '.csv' in str(i):
            file_path = './爬取结果/' + str(i)

            # Check if file is empty
            if os.path.getsize(file_path) == 0:
                print(f"Skipping empty file: {file_path}")
                continue  # Skip empty files

            try:
                data = pd.read_csv(file_path, encoding='gb18030')
                data.columns = ['标题', '小区名', '位置', '标签', '关注人数', '发布时间', '房间类型', '面积', '朝向',
                                '装修', '楼层', '年份', '楼况', '总价', '单价']
            except pd.errors.EmptyDataError:
                print(f"Skipping file with no data: {file_path}")
                continue  # Skip files that can't be read

            for row in range(1, len(data)):
                # Skip rows with invalid data
                if pd.isnull(data['房间类型'].iloc[row]) or pd.isnull(data['关注人数'].iloc[row]) or data['关注人数'].iloc[row] <= 0:
                    continue  # Skip invalid rows

                if data['房间类型'].iloc[row] in room_type_sum:
                    room_type_sum[data['房间类型'].iloc[row]] += data['关注人数'].iloc[row]
                    room_type_cnt[data['房间类型'].iloc[row]] += 1
                else:
                    room_type_sum[data['房间类型'].iloc[row]] = 0
                    room_type_cnt[data['房间类型'].iloc[row]] = 0
                    room_type_sum[data['房间类型'].iloc[row]] += data['关注人数'].iloc[row]
                    room_type_cnt[data['房间类型'].iloc[row]] += 1

    for key in room_type_sum.keys():
        room_type_avg[key] = round(room_type_sum[key] / room_type_cnt[key], 2)
    d_order = sorted(room_type_avg.items(), key=lambda x: x[1], reverse=True)
    draw(dict(d_order))

if __name__ == '__main__':
    read_csv()

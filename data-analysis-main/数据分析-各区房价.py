import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Pie

# 字典用于映射区域名称（你可以根据需要自定义）
regions_dic = {'tianhe': '天河', 'yuexiu': '越秀', 'liwan': '荔湾', 'haizhu': '海珠', 'panyu': '番禺', 'baiyun': '白云',
               'huangpu': '黄埔', 'conghua': '从化', 'zengcheng': '增城', 'huadou': '花都', 'nansha': '南沙',
               'nanhai': '南海', 'shunde': '顺德'}

def draw(room_type_count):
    # 绘制饼图显示每种房型的数量
    c = (
        Pie(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
            .add(
            "",
            [list(z) for z in zip(room_type_count.keys(), room_type_count.values())],
            radius=["30%", "75%"]
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="广州二手房各房型统计"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical")
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render('分析图表/' + "广州二手房各房型统计图.html")
    )

def read_csv():
    room_type_count = {}

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

            # 清洗数据：去掉房间类型为空或者关注人数为0或负值的数据
            data = data.dropna(subset=['房间类型', '关注人数'])  # 去掉房间类型和关注人数为空的行
            data = data[data['关注人数'] > 0]  # 过滤掉关注人数为0或负值的数据

            # 检查房间类型字段是否有额外的空格
            data['房间类型'] = data['房间类型'].str.strip()

            for row in range(len(data)):
                room_type = data['房间类型'].iloc[row]

                # Skip rows with invalid room type (empty or erroneous values)
                if not room_type:
                    continue  # Skip invalid room type rows

                # 提取几室几厅信息，例如 "3室2厅"
                room_type_str = ''.join(filter(str.isdigit, room_type))  # 提取房间类型中的数字部分

                if room_type_str in room_type_count:
                    room_type_count[room_type_str] += 1
                else:
                    room_type_count[room_type_str] = 1

    draw(room_type_count)

if __name__ == '__main__':
    read_csv()

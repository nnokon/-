import os
from pyecharts import options as opts
import pandas as pd
import requests
import urllib.parse
import time
from pyecharts.charts import Geo
from pyecharts.globals import GeoType


def formatdata(filenames):
    info_table = pd.DataFrame(columns=['位置', '次数'])
    row = 0
    for filename in filenames:
        try:
            file_path = os.path.join('./爬取结果/', filename)
            print(f"Processing file: {file_path}")
            data = pd.read_csv(file_path, encoding='gb18030')
            data.columns = ['标题', '小区名', '位置', '标签', '关注人数', '发布时间', '房间类型', '面积', '朝向',
                            '装修', '楼层', '楼况', '年份', '总价', '单价']
            frequency = data['小区名'].value_counts()
            for name, count in frequency.items():
                info_table.loc[row] = [name, count]
                row += 1
            print(f"{filename} finished")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    info_table.to_csv('./临时数据文件/频数统计.csv', index=False, encoding='gb18030')
    print('频数统计完成！')

def Bmap(filename):
    g = Geo(init_opts=opts.InitOpts(
        width='1800px',
        height='900px',
    )).add_schema(maptype="广州")

    stationid_list = []
    Longitude_list = []
    Latitude_list = []
    point_list = []
    file = pd.read_csv(filename, encoding='gb18030')
    for i in range(0, len(file)):
        stationid_list.append(file['位置'].iloc[i])
        point_list.append(file['次数'].iloc[i])
        Longitude_list.append(file['经度'].iloc[i])
        Latitude_list.append(file['纬度'].iloc[i])

    # 给所有点附上标签 'StationID'
    for i in range(0, len(stationid_list)):
        g.add_coordinate(stationid_list[i], Longitude_list[i], Latitude_list[i])

    # 给每个点赋值
    for i in range(0, len(file)):
        data_pair = []
        data_pair.append((stationid_list[i], int(point_list[i])))
        if int(point_list[i]) <= 3:
            g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=3)
        else:
            g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=int(point_list[i]))

    # 画图
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    g.set_global_opts(title_opts=opts.TitleOpts(title="全地点热力图展示"))

    # 保存结果到 html
    result = g.render('./分析图表/二手房频数地理热力图.html')
    print('地理热力图生成完毕！')

# 获取地址的经纬度
Bmap('./临时数据文件/经纬度转换.csv')
# 获取地址的经纬度
def gain_location(address):
    # 对地址进行 URL 编码
    encoded_address = urllib.parse.quote(address)

    # 你的 API Key
    api_key = ""

    # 构建请求 URL
    api_url = f"https://restapi.amap.com/v3/geocode/geo?address={encoded_address}&city=广州市&key={api_key}"

    try:
        # 发送请求
        response = requests.get(api_url)
        response.raise_for_status()  # 确保请求成功

        # 获取响应的 JSON 数据
        json_data = response.json()

        # 解析 JSON 数据
        if json_data.get('status') == '1':  # 如果请求成功
            # 获取 geocodes 数组中的第一个位置数据
            if 'geocodes' in json_data and len(json_data['geocodes']) > 0:
                location = json_data['geocodes'][0]['location']  # 获取经纬度信息
                lng, lat = location.split(',')  # 将经纬度分开
                # 打印成功的地址和经纬度
                print(f"成功获取经纬度：{address} -> 经度: {lng}, 纬度: {lat}")
                return {'lng': float(lng), 'lat': float(lat)}  # 返回经纬度作为字典
            else:
                print(f"No geocodes found for address: {address}")
                return None
        else:
            print(f"Error: {json_data.get('info', 'Unknown error')} for address: {address}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {address}: {e}")
        return None

# 读取 CSV 文件
input_file = './临时数据文件/频数统计.csv'
df = pd.read_csv(input_file, encoding='gb18030')

# 存储经纬度数据
location_data = []

# 遍历地址列表，获取经纬度
for index, row in df.iterrows():
    address = row['位置']
    location = gain_location(address)
    if location:
        location_data.append({'位置': address, '次数': row['次数'], '经度': location['lng'], '纬度': location['lat']})
    else:
        location_data.append({'位置': address, '次数': row['次数'], '经度': None, '纬度': None})

    # 添加延迟，每次请求后等待 1 秒钟（可以调整这个时间）
    time.sleep(1)  # 每次请求间隔 1 秒

# 将结果保存到新的 CSV 文件
output_file = './临时数据文件/经纬度转换.csv'
location_df = pd.DataFrame(location_data)

# 保存为 CSV 文件
location_df.to_csv(output_file, encoding='gb18030', index=False)

print("经纬度转换已完成，结果已保存到 './临时数据文件/经纬度转换.csv'")

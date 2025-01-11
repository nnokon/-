import requests
import json
import csv

# 高德地铁数据服务 URL
url = "https://map.amap.com/service/subway?_1734271715630&srhdata=4401_drw_guangzhou.json"

# 输出文件路径
output_file = "guangzhou_subway.csv"

# 请求 JSON 数据
response = requests.get(url)
data = response.json()

# 提取地铁线路和站点信息
stations = []
for line in data.get("l", []):  # 遍历所有线路
    line_name = line.get("ln", "未知线路")  # 获取线路名称
    for station in line.get("st", []):  # 遍历每条线路的站点
        station_name = station.get("n", "未知站点")  # 获取站点名称
        coordinates = station.get("sl", "0,0").split(",")  # 提取经纬度
        latitude, longitude = coordinates[1], coordinates[0]
        stations.append([line_name, station_name, latitude, longitude])

# 保存为 CSV 文件
with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # 写入表头
    writer.writerow(["线路名称", "站点名称", "纬度", "经度"])
    # 写入数据
    writer.writerows(stations)

print(f"广州地铁数据已保存到 {output_file}")
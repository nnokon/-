import requests
import json
import csv

# �ߵµ������ݷ��� URL
url = "https://map.amap.com/service/subway?_1734271715630&srhdata=4401_drw_guangzhou.json"

# ����ļ�·��
output_file = "guangzhou_subway.csv"

# ���� JSON ����
response = requests.get(url)
data = response.json()

# ��ȡ������·��վ����Ϣ
stations = []
for line in data.get("l", []):  # ����������·
    line_name = line.get("ln", "δ֪��·")  # ��ȡ��·����
    for station in line.get("st", []):  # ����ÿ����·��վ��
        station_name = station.get("n", "δ֪վ��")  # ��ȡվ������
        coordinates = station.get("sl", "0,0").split(",")  # ��ȡ��γ��
        latitude, longitude = coordinates[1], coordinates[0]
        stations.append([line_name, station_name, latitude, longitude])

# ����Ϊ CSV �ļ�
with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # д���ͷ
    writer.writerow(["��·����", "վ������", "γ��", "����"])
    # д������
    writer.writerows(stations)

print(f"���ݵ��������ѱ��浽 {output_file}")
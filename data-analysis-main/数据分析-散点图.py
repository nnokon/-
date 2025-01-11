import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import matplotlib.cm as cm

# 中文字体支持
rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
rcParams['axes.unicode_minus'] = False

# 读取地铁线路数据
subway_df = pd.read_csv('guangzhou_subway.csv')

# 读取经纬度转换数据（包含散点图数据）
location_df = pd.read_csv('./临时数据文件/经纬度转换.csv',encoding='gb18030')

# 设置图形大小
plt.figure(figsize=(12, 10))

# 获取地铁线路列表
line_ids = subway_df['线路名称'].unique()

# 动态颜色映射（给每条线路分配不同的颜色）
colors = cm.rainbow(np.linspace(0, 1, len(line_ids)))

# 绘制每条地铁线路
for idx, line_id in enumerate(line_ids):
    line_data = subway_df[subway_df['线路名称'] == line_id]

    # 绘制地铁线路
    plt.plot(line_data['经度'], line_data['纬度'],
             marker='o', linestyle='-', linewidth=2, markersize=6,
             markerfacecolor=colors[idx], markeredgewidth=2,  # 填充节点颜色
             label=f'{line_id}', color=colors[idx])

# 绘制散点图（地铁站以外的位置数据）
plt.scatter(location_df['经度'], location_df['纬度'],
            c=location_df['次数'], cmap='viridis', s=location_df['次数'] * 10,  # 点的大小与次数成比例
            edgecolor='black', alpha=0.7, label='Location Points')

# 设置标题和坐标轴
plt.title("Guangzhou Subway Map with Location Scatter and Lines", fontsize=16)
plt.xlabel("Longitude", fontsize=12)
plt.ylabel("Latitude", fontsize=12)

# 设置图例
plt.legend(title="Subway Lines", bbox_to_anchor=(1.05, 1), loc='upper left')

# 网格与显示
plt.grid(True)

# 保存图片
plt.savefig("guangzhou_subway_map_with_scatter_and_lines.png", dpi=300, bbox_inches='tight')  # 保存图片
plt.show()

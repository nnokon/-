import pandas as pd
import re
import matplotlib.pyplot as plt

# 读取Excel文件
file_path = '广州地铁客运量-昨日客流1.xlsx'  # 修改为你文件的路径
df = pd.read_excel(file_path)


# 定义一个提取客运量的函数
def extract_traffic(text_raw):
    # 提取客运量，格式一致 (如：线网总客流量为835万人次)
    traffic_match = re.search(r"线网总客流量为([\d\.]+)万人次", text_raw)
    traffic = traffic_match.group(1) if traffic_match else None
    # 将客运量转换为浮动数值并保留两位小数
    return round(float(traffic), 2) if traffic else None


# 定义一个提取日期并拆分的函数
def extract_date_parts(created_at):
    # 提取日期，格式一致 (如：Mon Dec 23 09:01:01 +0800 2024)
    date_match = re.match(r"([A-Za-z]{3} [A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2} \+0800 \d{4})", created_at)
    date_str = date_match.group(1) if date_match else None

    # 将日期字符串转换为 datetime 类型
    date = pd.to_datetime(date_str, errors='coerce')  # 转换为 datetime 格式

    # 提取年、月、日
    if date:
        year = date.year
        month = date.month
        day = date.day
        return year, month, day
    else:
        return None, None, None


# 应用函数提取日期和客运量
df[['year', 'month', 'day']] = df['created_at'].apply(lambda x: pd.Series(extract_date_parts(x)))
df['traffic'] = df['text_raw'].apply(extract_traffic)

# 创建日期列（用作X轴）
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# 创建新的DataFrame，保留需要的列
final_df = df[['date', 'traffic']]

# 可视化：柱状图
plt.figure(figsize=(10, 6))
plt.bar(final_df['date'], final_df['traffic'], color='skyblue')

# 设置标题和标签
plt.title('线网客运量随时间变化的柱状图')
plt.xlabel('日期')
plt.ylabel('线网客运量（万人次）')

# 格式化日期显示
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# 显示网格
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 显示图表
plt.tight_layout()  # 自动调整布局以避免标签被截断
plt.show()

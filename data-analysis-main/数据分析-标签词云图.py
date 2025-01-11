import pandas as pd
import os
from wordcloud import WordCloud


def draw_wordcloud(filenames):
    # 租房标签词云图
    labels_dic = {}

    # 遍历所有文件
    for filename in filenames:
        try:
            # 读取 CSV 文件
            data = pd.read_csv(os.path.join('./爬取结果', filename), encoding='gb18030', header=None,
                               skip_blank_lines=True)
            # 设置列名
            data.columns = ['标题', '小区名', '位置', '标签', '关注人数', '发布时间', '房间类型', '面积', '朝向',
                            '装修', '楼层', '年份', '楼况', '总价', '单价']

            # 遍历 '标签' 列
            for i in data['标签']:
                try:
                    # 如果标签为空或无效，跳过
                    if pd.isnull(i) or i == '':
                        continue

                    # 将标签分割为多个单词（按空格）
                    elements = i.split(' ')

                    # 统计每个标签出现的次数
                    for element in elements:
                        if element != '':
                            if element in labels_dic:
                                labels_dic[element] += 1
                            else:
                                labels_dic[element] = 1
                except Exception as e:
                    # 捕获任何标签解析错误并跳过
                    print(f"跳过无效标签数据: {i}，错误: {e}")
                    continue
        except Exception as e:
            print(f"无法处理文件 {filename}，错误: {e}")
            continue

    # 生成词云
    wc = WordCloud(font_path='simkai.ttf', max_words=100, width=1920, height=1080, margin=5)
    wc.generate_from_frequencies(labels_dic)

    # 保存词云图像
    wc.to_file('./分析图表/广州二手房标签词云图.png')


if __name__ == '__main__':
    filenames = os.listdir('./爬取结果')
    draw_wordcloud(filenames)

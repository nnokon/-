import pandas as pd
import re
import parsel
from bs4 import BeautifulSoup


def remove_html_tags(html_content):

    # 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 使用 get_text() 方法提取纯文本
    text = soup.get_text(separator=" ").strip()  # 使用空格作为分隔符，去除多余空白

    return text
def getIntoPage(region, text):
    data_all = []
    selector = parsel.Selector(text)
    item_all = selector.css(".sellListContent > li").getall()
    print(len(item_all))
    for item in item_all:
        selector2 = parsel.Selector(item)
        name = selector2.css(".title a::text").get()
        link = selector2.css(".title a::attr(href)").get()
        position, position2 = selector2.css(".positionInfo a::text").getall()
        labels = remove_html_tags(selector2.css(".tag").get())
        followers = remove_html_tags(selector2.css(".followInfo").get())
        total_price = remove_html_tags(selector2.css(".totalPrice span::text").get())
        price = selector2.css(".unitPrice::attr(data-price)").get()
        # print(name, link, position, position2, total_price, price, labels, followers)

        # alist = []
        alist_temp = dict()

        # 处理房屋名称和链接
        # alist.append(name if name else '')
        alist_temp["标题"] = name
        # alist_temp["链接"] = link
        # alist.append(link if link else '')

        # 处理小区和位置
        alist_temp["小区名"] = position
        alist_temp["位置"] = position2

        # 处理标签
        if labels:
            label_list = labels.split('|')
            alist_temp["标签"] = ' | '.join([label.strip() for label in label_list])

        # 处理关注人数和发布时间
        if followers:
            follower_data = followers.split('/')
            alist_temp["关注人数"] =  follower_data[0].replace('人关注', '').strip() if len(follower_data) > 0 else ''
            alist_temp["发布时间"] =  follower_data[1].replace('天以前发布', '').strip() if len(follower_data) > 1 else ''

        # 处理房间信息（例如 3室2厅 | 93.7平米 | 北 | 简装 | 中楼层）
        house_info = remove_html_tags(selector2.css(".houseInfo").get())
        if house_info:
            house_info = house_info.replace(' ', '')
            house_info_list = re.split(r'\|', house_info)  # 以"|"拆分信息
            print(house_info_list)

            if len(house_info_list) >= 7:
                alist_temp["房间类型"] = house_info_list[0]
                alist_temp["面积"] = house_info_list[1]
                alist_temp["朝向"] = house_info_list[2]
                alist_temp["装修"] = house_info_list[3]
                alist_temp["楼层"] = house_info_list[4]
                alist_temp["年份"] = house_info_list[5]
                alist_temp["楼况"] = house_info_list[6]
            else:
                alist_temp["房间类型"] = house_info_list[0]
                alist_temp["面积"] = house_info_list[1]
                alist_temp["朝向"] = house_info_list[2]
                alist_temp["装修"] = house_info_list[3]
                alist_temp["楼层"] = house_info_list[4]
                alist_temp["楼况"] = house_info_list[5]
                alist_temp["年份"] = ""

        # 处理价格信息
        if total_price:
            alist_temp["总价"] = float(total_price) * 10000

        if price:
            alist_temp["单价"] = price.replace('单价', '').replace('元/平米', '').strip()
        # print(alist)
        # 如果列表中的数据已满，则保存到 DataFrame
        data_all.append(alist_temp)
    # print(data_all)
    # print(len(data_all))
    info_table = pd.DataFrame(data=data_all)
    print(info_table.head())
    return info_table

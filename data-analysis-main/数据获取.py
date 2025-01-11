# -*- coding: utf-8 -*-
import os.path

import dd as ds
import asyncio
import aiohttp
import itertools
import datetime
import sys

# 修改 sys.stdout 的编码为 utf-8
sys.stdout.reconfigure(encoding='gb18030')
start = datetime.datetime.now()


async def parse(item, text):
    # 正则匹配提取数据
    try:
        print(item[0])
        datas = ds.getIntoPage(item[0], text)
        print(datas)
        if os.path.exists(f'爬取结果/{item[0]}.csv'):
            datas.to_csv(f'爬取结果/{item[0]}.csv', mode='a+', index=False, header=False, encoding='gb18030')
        else:
            datas.to_csv(f'爬取结果/{item[0]}.csv', index=False, encoding='gb18030')
    except Exception as e:
        print(f"错误：{e}")


class Spider:
    # 初始化
    def __init__(self):
        self.semaphore = asyncio.Semaphore(1)
        self.judge = True
        self.headers = {
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'gz.lianjia.com',
            "Cookie": "",
            'User-Agent': ''
                          ''
        }

    async def scrape(self, url):
        async with self.semaphore:  # 使用信号量来限制并发
            async with aiohttp.ClientSession(headers=self.headers) as session:
                response = await session.get(url)  # 发起请求
                await asyncio.sleep(3)  # 模拟请求延时
                # print("返回的", url)
                result = await response.text(encoding='utf-8')
                return result

    async def scrape_index(self, item):
        url = f'https://gz.lianjia.com/ershoufang/{item[0]}/pg{item[1]}/'
        print('url--->',url)
        text = await self.scrape(url)
        # exit()
        await parse(item, text)
        print(f'完成  {item[0]} 第{item[1]}页')
        await asyncio.sleep(1)

    async def main(self):
        regions = ['baiyun', 'yuexiu', 'liwan', 'haizhu', 'panyu', 'huangpu', 'conghua', 'zengcheng',
                   'huadou', 'nansha','nanhai','shunde','tianhe']
        # page = [str(i) for i in range(1, 101)]
        page = [str(i) for i in range(1, 10)]

        items = list(itertools.product(regions, page))  # 生成区域和页面的组合

        # 创建任务列表
        scrape_index_tasks = [self.scrape_index(item) for item in items]

        # 并行执行所有任务
        await asyncio.gather(*scrape_index_tasks)


if __name__ == '__main__':
    spider = Spider()
    # 使用 asyncio.run 来启动异步主程序
    asyncio.run(spider.main())

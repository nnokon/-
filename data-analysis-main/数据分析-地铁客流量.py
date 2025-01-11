import requests
import pandas as pd

content_list = []

for page in range(1, 200):
    headers = {
        "Cookie": "XSRF-TOKEN=FMF7ONohqsfrxBXYQ2Tvv4Km; Hm_lvt_d7c7037093938390bc160fc28becc542=1734931181; HMACCOUNT=0C3322E8D7BFA303; SCF=AssdxVRnRkvFec2o51kf-B0E2PewhLt47nQ6DwzxgR4zdLiHgDQ4rOUuWYdWqeP8-Y6_OTvK7zohh9F6u5FVLMA.; SUB=_2A25KbIf-DeRhGeBN4lIU8yvNzzmIHXVpA4U2rDV8PUNbmtANLRThkW9NRA_eoZDUzaWCUUYgVChMGdG5H4Gdxpbu; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhM0DpUnu9Rms22SmaB2yDT5NHD95Qce0.7SKefeKBfWs4Dqcj_i--4iKnEi-20i--fi-8Fi-24i--Ri-i8i-20i--Ri-i8i-20i--RiKysiKnN; ALF=02_1737524398; _s_tentry=passport.weibo.com; Apache=9266026418147.91.1734932406134; SINAGLOBAL=9266026418147.91.1734932406134; ULV=1734932406183:1:1:1:9266026418147.91.1734932406134:; WBPSESS=gXwRbe1s6wiI2_K83yK3aQb7SoCT91HRMb5RvS4pCJVJmDhuSfj4fm1vDyYXVhoKn414LIVwXQPkefO4FH9gqFOkBtTvKGm58BF6On6wqPNrr24NWNtr70Odq7k9dEgPYwmqA9nHiK0M6e74F3WkVQ==; Hm_lpvt_d7c7037093938390bc160fc28becc542=1734932499",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }
    data = {
        "page": page,
        "uid": "2612249974",
        "q": "悠悠报客流：昨日回顾",

    }

    url = f"https://weibo.com/ajax/statuses/searchProfile?"

    content_json = requests.get(url=url, headers=headers, params=data).json()
    print("第", page, "页，本页", len(content_json['data']['list']), "条数据", content_json['data']['list'])

    # df = pd.DataFrame(content_json['data'])
    if len(content_json['data']['list']) > 0:
        df = pd.json_normalize(content_json['data']['list'], errors='ignore')
        df = df.loc[:, ['created_at', 'text_raw']]
        content_list.append(df)
    else:
        break

# concat合并Pandas数据
df = pd.concat(content_list)
df.to_excel(f"广州地铁客运量-昨日客流1.xlsx", index=False)
print("保存完成！")

# 查看 DataFrame 的行数和列数。
rows = df.shape
print("请求得到的表格行数与列数：", rows)

import requests
from bs4 import BeautifulSoup
import jieba
from jieba.analyse import extract_tags
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# 欲爬取的網址、送請求、解析
url = "https://www.ptt.cc/bbs/Japan_Travel/M.1672289125.A.1DC.html" 
web = requests.get(url)
soup = BeautifulSoup(web.text,"lxml")

# 爬取回復，清理後放置於空字串
push_tag = soup.find_all("span",class_="f3 push-content")
p = []
for row in push_tag:
    s= row.get_text().replace(": ","")
    p.append(s)
    # print(s)

# 設定分析所需的斷字字典
jieba.set_dictionary("dict.txt.big.txt")

# 添加空格(jieba才可以進行分析) 
c = " ".join(p)
# 提取關鍵字(設定80個關鍵字)，並放進新的字典
kw = extract_tags(c,topK=80, withWeight=True, allowPOS=(),withFlag=True)
d = {}
for j in range(len(kw)):
    d[kw[j][0]]=kw[j][1]

# 製作文字雲
wd=WordCloud(width=1280, # 圖寬
             height=720, # 圖高
             background_color="#000000", # 圖底色
             colormap="Dark2", # 字體顏色
             font_path=r"C:\Windows\Fonts\msjhbd.ttc" # 字型
             ).fit_words(d)
# 用plt顯示
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.figure(dpi=100)
plt.imshow(wd)
plt.title("[問題] 北海道跟團還是自助")
plt.axis("off")
plt.show()

# 另存csv檔
df =  pd.DataFrame(p)
# print(df)
df.to_csv("crawl_travel.csv",encoding="utf-8",index=False)
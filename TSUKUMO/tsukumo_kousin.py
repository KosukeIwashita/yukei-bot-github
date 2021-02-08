import os
import requests
import pandas as pd

from bs4 import BeautifulSoup
from pathlib import Path
from linebot import LineBotApi
from linebot.models import TextSendMessage

textFile = Path("rtx3070.text")
line_bot_api = LineBotApi(os.environ["line_channel_token"])


url = "https://shop.tsukumo.co.jp/search/c20:2018:2018200:201820088000400/?keyword=3070"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

get_class = soup.find(class_="search-box__product-list search-default__product-list mb20__common")
get_text = get_class.find_all(class_="search-box__product")

text_only = [x.text for x in get_text]
text_only = [x.replace("\n", "") for x in text_only]
text_only = [x.replace("\xa0", "") for x in text_only]
text_only = str(text_only)

old = open(textFile, encoding="UTF-8")
old_text = old.read()

if(text_only == old_text):
    line_bot_api.broadcast(TextSendMessage(text='更新はありまｓん'))

else:
    f = open(textFile, "w", encoding="UTF-8")
    f.writelines(text_only)
    f.close
    line_bot_api.broadcast(TextSendMessage(text='3070更新された'))
    line_bot_api.broadcast(TextSendMessage(text=url))

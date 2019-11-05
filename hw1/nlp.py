# -*- coding: utf-8 -*-
# @Date    : 2019-09-25
# @Author  : 17341046 Guoziyu (893050234@qq.com)
import jieba
import requests
import lxml
from bs4 import BeautifulSoup
import re


url = 'http://www.xinhuanet.com/politics/leaders/2019-09/21/c_1125023359.htm'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.content, 'html.parser')
text = soup.find_all(text=True)

#print(set([t.parent.name for t in text]))

# 将网页文字写入txt文件
with open('web.txt', 'w', encoding='utf-8')as f_write:
    for i in text:
        if i.parent.name == 'p'or i.parent.name == 'title':
            f_write.write(i.strip(' '))

f_read = open('web.txt', 'r', encoding='utf-8')
words = f_read.read()


jieba.add_word('史竞男')  # 加入默认词汇

# 分词并写入结果txt文件
paragraph = jieba.cut(words, cut_all=False)
with open('text.txt', 'w', encoding='utf-8')as f_write:
    f_write.write('Default Mode:')
    for i in paragraph:
        if i == ' ' or i == '\n':
            f_write.write(i)
        else:
            f_write.write(i+'|')

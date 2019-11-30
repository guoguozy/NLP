from bs4 import BeautifulSoup
import urllib.request
import re
import os
import requests


def get_page_link():
    '''
    Function：使用request库获取链接
    Return：新闻链接的list
    '''
    page = 1
    pagelinks = []
    while page <= 180:  # 设置爬取网页数量
        init_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=372&lid=2431&k=&num=50&page=' + str(
            page)  # + '&r=0.09727658885083823&callback=jQuery1112008872655482486436_1571649390171&_=1571649390176'
        request = urllib.request.Request(init_url)
        response = urllib.request.urlopen(request)
        data = response.read()
        data = data.decode('gbk')  # 设置解码方式
        reg_str = r'"url":"(.*?)"'
        pattern = re.compile(reg_str, re.DOTALL)
        items = re.findall(pattern, data)
        for item in items:
            pagelinks.append(item)
        page += 1
    return pagelinks


def del_same_link(pagelinks):
    '''
    Function：去除重复链接
    Return：包含不重复链接的list
    '''
    unrepect_url = []
    for l in pagelinks:
        if l not in unrepect_url:
            unrepect_url.append(l)
    return unrepect_url


def writelist(list):
    '''
    Function：记录可用不重复链接
    Return：None
    '''
    f = open("D:\\code\\py\\NLP\\hw2\\list.txt", "w")
    for row in list:
        f.write(row+'\n')
    f.close()


def get_news_content(list, n, num):
    '''
    Function：获取链接的新闻内容，并写入txt文件
    Return：True or False
    '''
    print(n)
    # print(list[n])
    url = str(list[n].replace('\\', ''))
    # try:
    req = requests.get(url)
    req.encoding = 'utf-8'
    textreq = BeautifulSoup(req.text, features='lxml')
    # print(textreq.prettify())
    article = textreq.find('div', class_="article", id="artibody")
    if not article:
        print("error\n")
        return False
    else:
        body = article.get_text()
        index = body.find('(function')
        if index > 0:
            body = body[:index]
        if len(body) > 300 and '{' not in body:
            body = body.strip()
            fp = open('E:\\code\\py\\NLP\\hw2\\data\\' +
                      str(num+1) + '.txt', 'w', encoding='utf-8')
            fp.write(body)
            fp.close()
        else:
            return False
        return True


if __name__ == '__main__':

    pagelinks = get_page_link()
    urllist = del_same_link(pagelinks)
    writelist(urllist)
    num = 0
    for i, link in enumerate(urllist):
        if(num < 1000):
            if(get_news_content(urllist, i, num)):
                num += 1
        else:
            break

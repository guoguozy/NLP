# coding=utf-8
# jieba 分词
import jieba
f_read = open('joke.txt', 'r', encoding='utf-8')
words = f_read.read()
paragraph = jieba.cut(words, cut_all=False)
with open('joke_text.txt', 'w', encoding='utf-8')as f_write:
    for i in paragraph:
        f_write.write(i+'|')
# thulac 分词
import thulac
thu1 = thulac.thulac()  # 默认模式
text = thu1.cut("欢迎武汉市长江大桥莅临指导", text=True)
print(text)
text = thu1.cut("广州市长隆马戏欢迎您", text=True)
print(text)
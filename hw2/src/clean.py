import jieba
import string
import re
zhon_punctuation = ['，', ' ', '“', '”', '。', '\u3000', '\n', '\xa0', '（', '）', '、', '；', '：', '《', '》', '—', '！', '？',
                    '―', '…', '＜', '’', '·', '｜', '【', '】', '／', '‘', '％', '–', '＋', '～', '〔', '〕', '「', '」', '－', '＂', '①', '②', '③']
en_punctuation = ['/', '丨', ',', '.', '(', ')', '+', '-', '[', ']', '&', '@', '..', '...', '....', '.....', '......', '.......',
                  '|', '~', ':', ';', '#', '=', '_', '>', '*', '"', '?', '!', "'", '\\', '$', '%', '<', '=', '^', '`', '{', '}']

def get_stwlist():
    stwlist = [x.strip()
               for x in open('hw2/stopwords/哈工大停用词表.txt', encoding='utf-8').readlines()]
    # stwlist += [x.strip() for x in open('hw2/stopwords/百度停用词表.txt',encoding='utf-8').readlines()]
    stwlist += [x.strip() for x in open('hw2/stopwords/中文停用词表.txt',
                                        encoding='utf-8').readlines()]
    stwlist += [x.strip() for x in open('hw2/stopwords/四川大学机器智能实验室停用词库.txt',
                                        encoding='utf-8').readlines()]
    return stwlist

def remove_punctuation(line):
    # 只保留中文、大小写字母和阿拉伯数字
    # 去掉标点符号
    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    return re.sub(reg, '', line)


def remove_number_english(word):
    # 去除阿拉伯数字和英文
    reg = "[a-zA-Z0-9]"
    return re.sub(reg, '', word)


def clear_and_write_words(start, end):
    jieba.add_word('云计算')
    jieba.add_word('区块链')
    for file in range(start, end):
        fread = open('hw2/data/' + str(file+1)+'.txt', 'r',encoding='utf-8')
        fwrite = open('hw2/word/' + str(file+1)+'.txt', 'w',encoding='utf-8')
        for line in fread.readlines():
            line = re.split(r'[！？…。；]', line)
            fwrite = open('hw2/word/' + str(file+1)+'.txt', 'a',encoding='utf-8')
            for sentences in line:
                word_list = list(jieba.cut(sentences.replace(' ', '')))
                i = 0
                while i < len(word_list):
                    if remove_punctuation(word_list[i]) == ''or word_list[i] in en_punctuation or word_list[i] in zhon_punctuation:
                        del word_list[i]
                    else:
                        i = i+1
                if word_list:
                    fwrite.write(' '.join(word_list)+'\n')


def create_words_table(start, end):
    All_words = {}
    stwlist = get_stwlist()
    for file in range(start, end):
        fread = open('hw2/word/' + str(file+1)+'.txt', 'r',encoding='utf-8')
        for line in fread.readlines():
            if line:
                line = line.rstrip('\n')
                line = re.split(r'\s', line)
                for i in line:
                    if i not in stwlist and remove_punctuation(remove_number_english(i)) != '' and remove_punctuation(remove_number_english(i)) not in zhon_punctuation+en_punctuation and len(i) > 1:
                        if i in All_words:
                            All_words[i] = All_words[i]+1
                        else:
                            All_words[i] = 1
    fsum = open('hw2/words_table_5.txt', 'w',encoding='utf-8')
    number = 1
    words_list = sorted(All_words.items(), key=lambda d: d[1], reverse=False)
    for item in words_list:
        fsum.write(str(number)+' '+str(item[0])+' '+str(item[1])+'\n')
        number = number+1


def match():
    # 查看有多少个answer存在词表中
    All_words = {}
    fread = open('hw2/words_table_5.txt',encoding='utf-8')
    for i in fread.readlines():
        i = i.split()
        All_words[i[1]] = i[2]
    num = 0
    fread2 = open('hw2/answer.txt',encoding='utf-8')
    for i in fread2.readlines():
        i = i.rstrip('\n')
        if i in All_words.keys():
            num += 1
    print(num)

def clean_word(start,end):
    # 将分好词的1000个txt去掉停止词
    stwlist=get_stwlist()
    for file in range(start,end):
        fread = open('hw2/word/' + str(file+1)+'.txt', 'r',encoding='utf-8')
        fwrite = open('hw2/word_cleaned/' + str(file+1)+'.txt', 'w',encoding='utf-8')
        for line in fread.readlines():
            line=line[:len(line)-1].split(' ')
            i=0
            while i <len(line):
                if line[i] in stwlist:
                    del line[i]
                else:
                    i+=1
            if line:
                fwrite.write(' '.join(line))
                fwrite.write('\n')

if __name__ == '__main__':
    # clear_and_write_words(0, 1000)
    # create_words_table(0, 1000)
    # match()
    clean_word(0,1000)
import jieba
import clean


def n_gram(n):
    fread = open('hw2/questions.txt', 'r')
    match_word = {}
    question = {}
    number = 1
    stwlist = clean.get_stwlist()
    # 读question.txt，记录前n-1个词及问题
    for sentences in fread.readlines():
        word_list = list(jieba.cut(sentences))
        # 去掉标点和空格
        for i in range(0, len(word_list)):
            word_list[i] = clean.remove_punctuation(word_list[i])
        word_list = [x for x in word_list if x != '']
        # 去掉停止词
        num_word = 0
        while num_word < len(word_list):
            if word_list[num_word] in stwlist:
                del word_list[num_word]
            else:
                num_word += 1

        if n == 2:
            match_word[word_list[word_list.index('MASK')-1]+' '] = {}
            question[number] = word_list[word_list.index('MASK')-1]+' '
        elif n == 3:
            match_word[word_list[word_list.index(
                'MASK')-2]+' '+word_list[word_list.index('MASK')-1]+' '] = {}
            question[number] = word_list[word_list.index(
                'MASK')-2]+' '+word_list[word_list.index('MASK')-1]+' '
        number += 1
    for front_n_word in match_word.keys():
        for i in range(0, 1000):
            # fread = open('hw2/word/'+str(i+1)+'.txt', 'r')
            fread = open('hw2/word_cleaned/'+str(i+1)+'.txt', 'r')
            for lines in fread.readlines():
                lines = lines.rstrip('\n')
                if front_n_word in lines:
                    answer_word = lines[lines.index(
                        front_n_word)+len(front_n_word):].split(' ')[0]
                    if answer_word in match_word[front_n_word]:
                        match_word[front_n_word][answer_word] += 1
                    else:
                        match_word[front_n_word][answer_word] = 1
        match_word[front_n_word] = sorted(
            match_word[front_n_word].items(), key=lambda d: d[1], reverse=True)
    fwrite = open('hw2/prediction_3.txt', 'w')
    for i in range(1, 101):
        num = 0
        for item in match_word[question[i]]:
            num += 1
            if num == 6:
                break
            fwrite.write(str(item[0])+' ')
        fwrite.write('\n')


def accurate():
    bingo = 0
    f1 = open('hw2/answer.txt',encoding='utf-8')
    #f2 = open('predict.txt',encoding='utf-8')
    #f2 = open('hw2/prediction_2.txt',encoding='utf-8')
    f2 = open('hw2/prediction_3.txt',encoding='utf-8')
    answer_list = []
    pre_list = []
    for i in f1.readlines():
        i = i.rstrip('\n')
        answer_list.append(i)
    for i in f2.readlines():
        i = i.rstrip('\n')
        pre_list.append(i)
    for i in range(0, 100):
        if answer_list[i] == pre_list[i].split(' ')[0]:
        # if answer_list[i] in pre_list[i].split(' '):
            print(i,answer_list[i])
            bingo += 1
    print(bingo/100)


if __name__ == "__main__":
    # n_gram(3)
    accurate()

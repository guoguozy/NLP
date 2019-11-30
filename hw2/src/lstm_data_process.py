import jieba
import clean


def create_new_table():
    All_words = {}
    word_num = 1

    # 将1000个txt的词加入词表
    for file in range(0, 1000):
        fread = open('hw2/word_cleaned/'+str(file+1)+'.txt', encoding='utf-8')
        for line in fread.readlines():
            line = line[:len(line)-1].split(' ')
            for i in line:
                if i not in All_words.keys():
                    All_words[i] = word_num
                    word_num += 1

    # 将qusetion中的词加入词表
    fread = open('hw2/questions.txt', encoding='utf-8')
    for sentences in fread.readlines():
        word_list = list(jieba.cut(sentences))
        # 去掉标点和空格
        for i in range(0, len(word_list)):
            word_list[i] = clean.remove_punctuation(word_list[i])
        word_list = [x for x in word_list if x != '']
        # 去掉停止词
        for i in range(0, len(word_list)):
            if word_list[i] in clean.get_stwlist():
                word_list[i] = ''
        word_list = [x for x in word_list if x != '']
        for i in word_list:
            if i == 'MASK':
                All_words[i] = -1
            if i not in All_words.keys():
                All_words[i] = word_num
                word_num += 1

    # 将answer中词加入词表
    fread = open('hw2/answer.txt', encoding='utf-8')
    for line in fread.readlines():
        if str(line.rstrip('\n')) not in All_words.keys():
            All_words[str(line.rstrip('\n'))] = word_num
            word_num += 1

    fwrite = open('hw2/All_words_dict.txt', 'w', encoding='utf-8')
    fwrite.write(str(All_words))


def get_all_words_dict():
    f = open('hw2/All_words_dict.txt', 'r', encoding='utf-8')
    return dict(eval(f.read()))


def transfer_word_to_num():
    All_words = get_all_words_dict()
    for file in range(0, 1000):
        fread = open('hw2/word_cleaned/'+str(file+1)+'.txt', encoding='utf-8')
        fwrite = open('hw2/word_train/'+str(file+1) +
                      '.txt', 'w', encoding='utf-8')
        for line in fread.readlines():
            line = line[:len(line)-1].split(' ')
            temp = []
            for i in line:
                temp.append(All_words[i])
            if len(temp) >= 5:
                fwrite.write(str(temp)+'\n')

    fread = open('hw2/questions.txt', encoding='utf-8')
    fwrite = open('hw2/questions_num.txt', 'w', encoding='utf-8')
    for sentences in fread.readlines():
        word_list = list(jieba.cut(sentences))
        # 去掉标点和空格
        for i in range(0, len(word_list)):
            word_list[i] = clean.remove_punctuation(word_list[i])
        word_list = [x for x in word_list if x != '']
        # 去掉停止词
        for i in range(0, len(word_list)):
            if word_list[i] in clean.get_stwlist():
                word_list[i] = ''
        word_list = [x for x in word_list if x != '']
        temp = []
        for i in word_list:
            temp.append(All_words[i])
        fwrite.write(str(temp)+'\n')

    fread = open('hw2/answer.txt', encoding='utf-8')
    fwrite = open('hw2/answer_num.txt', 'w', encoding='utf-8')
    fwrite.write('\n'.join([str(All_words[str(line.rstrip('\n'))])
                            for line in fread.readlines()]))


if __name__ == "__main__":
    # create_new_table()
    transfer_word_to_num()

import tensorflow as tf
import keras
import os
import numpy as np
import datetime
import time
import lstm_data_process
time_steps = 10


def load_train():
    pre_path = 'hw2/word_train/'
    txt_list = os.listdir(pre_path)
    txt_list = txt_list[0:1000]
    train_x = []
    train_y = []
    result1 = []
    result2 = []
    for txt in txt_list:
        with open(pre_path+txt, 'r', encoding='utf-8')as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = eval(line)
                seg_x, seg_y = seq_seg(line)
                result1.extend(seg_x[0])
                result2.extend(seg_x[1])
                train_y.extend(seg_y)
    train_x = [result1, result2]
    return train_x, train_y


def seq_seg(seq):
    global time_steps
    seg_x = []
    seg_y = []
    size = time_steps//2
    result1 = []
    result2 = []
    for i in range(1, len(seq)):
        iter_x1 = []
        iter_x2 = []
        iter_y = seq[i]
        if i >= size:
            iter_x1 = seq[i-size:i]
        else:
            iter_x1 = [0 for _ in range(size-i)]+seq[0:i]
        if i+size < len(seq):
            iter_x2 = seq[i+1:i+size+1]
        else:
            iter_x2 = seq[i+1:len(seq)]+[0 for _ in range(size-len(seq)+i+1)]
        result1.append(iter_x1)
        result2.append(iter_x2)
        seg_y.append(iter_y)
    seg_x = [result1, result2]
    return seg_x, seg_y


def load_test(length):
    # test_x, test_y = lt.load_test(3)
    test_x = []
    test_y = []
    dic = {}
    with open('hw2/questions_num.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        test_x = [eval(s.strip()) for s in lines]
    with open('hw2/answer_num.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        test_y = [eval(s.strip()) for s in lines]
    with open('hw2/All_words_dict.txt', 'r', encoding='utf-8')as f:
        dic = eval(f.read())
    result1 = []
    result2 = []
    for seq in test_x:
        index = seq.index(-1)
        left = []
        right = []
        if index >= length:
            left = seq[index-length:index]
        else:
            left = [0 for _ in range(length-index)]+seq[0:index]
        if index+length < len(seq):
            right = seq[index+1:index+length+1]
        else:
            right = seq[index+1:]+[0 for _ in range(length-len(seq)+index+1)]

        result1.append(left)
        result2.append(right)
    test_x = [result1, result2]
    return test_x, test_y, dic


def create_model(dic_len, axis=64):
    global time_steps
    Input1 = tf.keras.layers.Input(shape=(time_steps//2), dtype='float32')
    Input2 = tf.keras.layers.Input(shape=(time_steps//2), dtype='float32')
    encode = tf.keras.layers.Embedding(
        dic_len, axis, input_length=time_steps//2, trainable=True)
    v1 = encode(Input1)
    v2 = encode(Input2)

    l1 = tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(128, return_sequences=True))(v1)
    l2 = tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(128, return_sequences=True))(v2)

    l = tf.keras.layers.Concatenate(axis=1)([l1, l2])
    l = tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(128, return_sequences=False))(l)
    l = tf.keras.layers.Dropout(0.5)(l)

    d = tf.keras.layers.Dense(512, activation='relu')(l)
    d = tf.keras.layers.BatchNormalization()(d)
    output = tf.keras.layers.Dense(dic_len, activation='softmax')(d)

    model = tf.keras.Model(inputs=[Input1, Input2], outputs=output)

    return model

# def get_dic():
#     dic={}
#     with open('one_hot.txt','r',encoding='utf-8')as f:
#         dic=eval(f.read())
#     return dic


def get_dic():
    int_to_str = {}
    all_words = lstm_data_process.get_all_words_dict()
    for key, value in all_words.items():
        int_to_str[value] = key
    return int_to_str


def test(network, test_x):
    dic = get_dic()
    out = network([test_x[0], test_x[1]])
    out = tf.argmax(out, axis=1)
    out = out.numpy().astype('int32')

    result1 = []
    for i in range(len(out)):
        if dic.get(out[i]):
            result1.append(dic[out[i]])

    print(str(result1))
    with open('hw2/answer.txt', 'r', encoding='utf-8')as f:
        labels = f.readlines()
        labels = [line.strip() for line in labels]
    print(labels)
    with open('predict.txt', 'w', encoding='utf-8') as f:
        for i in range(len(result1)):
            f.write(result1[i]+','+labels[i]+'\n')


def main():
    # dic_len=len(dic)+1
    test_x, test_y, dic = load_test(time_steps//2)
    train_x, train_y = load_train()
    size = len(dic)
    # test_x=list(map(lambda x:eval(x),test_x))

    train_x = np.array(train_x).astype('float32')
    train_y = np.array(train_y).astype('int32')
    test_x = np.array(test_x).astype('float32')
    test_y = np.array(test_y).astype('int32')

    network = create_model(size+1, 64)
    # 设置优化器，损失函数，评估函数
    # callback,可视化，真的方便
    s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    s = '.\\logs\\LV1'
    # print(s)
    callback = [tf.keras.callbacks.TensorBoard(
        log_dir=s,
        write_graph=True,
        write_images=True
    )]
    network.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy', metrics=['acc'])
    # network=tf.keras.models.load_model('lastmodel_V1.h5')
    # network.load_weights('lastmodel_weights_V20.h5')
    print(network.summary())

    
    # 训练
    try:
        network.fit([train_x[0], train_x[1]], train_y, batch_size=128, callbacks=callback,
                    epochs=10, verbose=1, shuffle=True, validation_data=([test_x[0], test_x[1]], test_y))
    except Exception as e:
        print(e)
    network.save_weights('lastmodel_weights.h5')
    # network.save('lastmodel_V1.h5')
    # 测试
    test(network, test_x)


if __name__ == "__main__":
    main()

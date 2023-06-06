import pickle


def get_vocab(corpus1, corpus2):
    word_vocab = set()
    for i in range(0, len(corpus1)):
        for j in range(0, len(corpus1[i][1][0])):
            word_vocab.add(corpus1[i][1][0][j])
        for j in range(0, len(corpus1[i][1][1])):
            word_vocab.add(corpus1[i][1][1][j])
        for j in range(0, len(corpus1[i][2][0])):  # len(corpus2[i][2])
            word_vocab.add(corpus1[i][2][0][j])  # 注意之前是 word_vocab.add(corpus2[i][2][j])
        for j in range(0, len(corpus1[i][3])):
            word_vocab.add(corpus1[i][3][j])

    for i in range(0, len(corpus2)):
        for j in range(0, len(corpus2[i][1][0])):
            word_vocab.add(corpus2[i][1][0][j])
        for j in range(0, len(corpus2[i][1][1])):
            word_vocab.add(corpus2[i][1][1][j])
        for j in range(0, len(corpus2[i][2][0])):  # len(corpus2[i][2])
            word_vocab.add(corpus2[i][2][0][j])  # 注意之前是 word_vocab.add(corpus2[i][2][j])
        for j in range(0, len(corpus2[i][3])):
            word_vocab.add(corpus2[i][3][j])
    print(len(word_vocab))
    return word_vocab


def load_pickle(filename):
    return pickle.load(open(filename, 'rb'), encoding='iso-8859-1')


# 构建初步词典
def vocab_processing(filepath1, filepath2, save_path):
    with open(filepath1, 'r') as f:
        total_data1 = eval(f.read())
        f.close()

    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())
        f.close()

    vocab_set = get_vocab(total_data1, total_data2)
    f = open(save_path, "w")
    f.write(str(vocab_set))
    f.close()


def final_vocab_processing(filepath1, filepath2, save_path):
    word_set = set()
    with open(filepath1, 'r') as f:
        total_data1 = set(eval(f.read()))
        f.close()
    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())
        f.close()
    total_data1 = list(total_data1)
    vocab_set = get_vocab(total_data1, total_data2)
    for i in vocab_set:
        if i in total_data1:
            continue
        else:
            word_set.add(i)
    print(len(total_data1))
    print(len(word_set))
    f = open(save_path, "w")
    f.write(str(word_set))
    f.close()


if __name__ == "__main__":
    # ====================获取staqc的词语集合===============
    python_hnn = 'xxxxx'
    python_staqc = 'xxxxx'
    python_word_dict = 'xxxxx'

    sql_hnn = 'xxxxx'
    sql_staqc = 'xxxxx'
    sql_word_dict = 'xxxxx'

    # ====================获取最后大语料的词语集合的词语集合===============
    new_sql_staqc = 'xxxxx'
    new_sql_large = 'xxxxx'
    large_word_dict_sql = 'xxxxx'
    final_vocab_processing(sql_word_dict, new_sql_large, large_word_dict_sql)

    new_python_staqc = 'xxxxx'
    new_python_large = 'xxxxx'
    large_word_dict_python = 'xxxxx'
    final_vocab_processing(python_word_dict, new_python_large, large_word_dict_python)

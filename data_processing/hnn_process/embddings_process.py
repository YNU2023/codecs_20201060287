import pickle

import numpy as np
from gensim.models import KeyedVectors


class WordVectorUtils:
    def __init__(self, vec_path):
        self.vec_path = vec_path

    def load_word_vectors(self):
        return KeyedVectors.load_word2vec_format(self.vec_path, binary=False)

    def save_word_vectors(self, model, output_path):
        model.init_sims(replace=True)
        model.save(output_path)


class DictionaryBuilder:
    def __init__(self, word_vec_path):
        self.word_vec_path = word_vec_path

    def build_dictionary(self, type_vec_path, type_word_path, final_vec_path, final_word_path):
        model = KeyedVectors.load(type_vec_path, mmap='r')

        with open(type_word_path, 'r') as f:
            total_word = eval(f.read())

        word_dict = ['PAD', 'SOS', 'EOS', 'UNK']
        fail_word = []
        rng = np.random.RandomState(None)
        pad_embedding = np.zeros(shape=(1, 300)).squeeze()
        unk_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
        sos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
        eos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
        word_vectors = [pad_embedding, sos_embedding, eos_embedding, unk_embedding]

        for word in total_word:
            try:
                word_vectors.append(model.wv[word])
                word_dict.append(word)
            except:
                fail_word.append(word)

        word_vectors = np.array(word_vectors)
        word_dict = dict(map(reversed, enumerate(word_dict)))

        with open(final_vec_path, 'wb') as file:
            pickle.dump(word_vectors, file)

        with open(final_word_path, 'wb') as file:
            pickle.dump(word_dict, file)

        print("完成")


class DataSerialization:
    def __init__(self, word_dict_path):
        self.word_dict_path = word_dict_path

    def get_index(self, word_type, text, word_dict):
        location = []

        if word_type == 'code':
            location.append(1)
            len_c = len(text)
            if len_c + 1 < 350:
                if len_c == 1 and text[0] == '-1000':
                    location.append(2)
                else:
                    for i in range(0, len_c):
                        if word_dict.get(text[i]) != None:
                            index = word_dict.get(text[i])
                            location.append(index)
                        else:
                            index = word_dict.get('UNK')
                            location.append(index)

                    location.append(2)
            else:
                for i in range(0, 348):
                    if word_dict.get(text[i]) != None:
                        index = word_dict.get(text[i])
                        location.append(index)
                    else:
                        index = word_dict.get('UNK')
                        location.append(index)
                location.append(2)
        else:
            if len(text) == 0:
                location.append(0)
            elif text[0] == '-10000':
                location.append(0)
            else:
                for i in range(0, len(text)):
                    if word_dict.get(text[i]) != None:
                        index = word_dict.get(text[i])
                        location.append(index)
                    else:
                        index = word_dict.get('UNK')
                        location.append(index)

        return location

    def serialize_data(self, type_path, final_type_path, word_dict_path):
        with open(word_dict_path, 'rb') as file:
            word_dict = pickle.load(file)

        with open(type_path, 'r') as f:
            type_data = eval(f.read())

        final_data = []

        for data in type_data:
            text = data[0]
            label = data[1]
            index = self.get_index('text', text, word_dict)
            final_data.append((index, label))

        with open(final_type_path, 'wb') as file:
            pickle.dump(final_data, file)

        print("完成")


# 使用示例
vec_path = "xxxxx"
type_vec_path = "xxxxx"
type_word_path = "xxxxx"
final_vec_path = "xxxxx"
final_word_path = "xxxxx"
word_dict_path = "xxxxx"
type_path = "xxxxx"
final_type_path = "xxxxx"

word_vector_utils = WordVectorUtils(vec_path)
word_vectors = word_vector_utils.load_word_vectors()

dictionary_builder = DictionaryBuilder(word_vec_path)
dictionary_builder.build_dictionary(type_vec_path, type_word_path, final_vec_path, final_word_path)

data_serialization = DataSerialization(word_dict_path)
data_serialization.serialize_data(type_path, final_type_path, word_dict_path)

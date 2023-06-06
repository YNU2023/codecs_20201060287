import pickle
import sys
from multiprocessing import Pool as ThreadPool

sys.path.append("..")

# 解析结构
from python_structured import *
from sqlang_structured import *

# 定义并行分词类
class ParallelTokenizer:
    def __init__(self, lang_type, split_num, source_path, save_path):
        self.lang_type = lang_type
        self.split_num = split_num
        self.source_path = source_path
        self.save_path = save_path

    # python解析
    def multipro_python_query(self, data_list):
        result = [python_query_parse(line) for line in data_list]
        return result

    def multipro_python_code(self, data_list):
        result = [python_code_parse(line) for line in data_list]
        return result

    def multipro_python_context(self, data_list):
        result = []
        for line in data_list:
            if line == '-10000':
                result.append(['-10000'])
            else:
                result.append(python_context_parse(line))
        return result

    # sql解析
    def multipro_sqlang_query(self, data_list):
        result = [sqlang_query_parse(line) for line in data_list]
        return result

    def multipro_sqlang_code(self, data_list):
        result = [sqlang_code_parse(line) for line in data_list]
        return result

    def multipro_sqlang_context(self, data_list):
        result = []
        for line in data_list:
            if line == '-10000':
                result.append(['-10000'])
            else:
                result.append(sqlang_context_parse(line))
        return result

    def parse_python(self, python_list):
        acont1_data = [i[1][0][0] for i in python_list]
        acont1_split_list = [acont1_data[i:i + self.split_num] for i in range(0, len(acont1_data), self.split_num)]
        pool = ThreadPool(10)
        acont1_list = pool.map(self.multipro_python_context, acont1_split_list)
        pool.close()
        pool.join()
        acont1_cut = []
        for p in acont1_list:
            acont1_cut += p
        print('acont1条数：%d' % len(acont1_cut))

        acont2_data = [i[1][1][0] for i in python_list]
        acont2_split_list = [acont2_data[i:i + self.split_num] for i in range(0, len(acont2_data), self.split_num)]
        pool = ThreadPool(10)
        acont2_list = pool.map(self.multipro_python_context, acont2_split_list)
        pool.close()
        pool.join()
        acont2_cut = []
        for p in acont2_list:
            acont2_cut += p
        print('acont2条数：%d' % len(acont2_cut))

        query_data = [i[3][0] for i in python_list]
        query_split_list = [query_data[i:i + self.split_num] for i in range(0, len(query_data), self.split_num)]
        pool = ThreadPool(10)
        query_list = pool.map(self.multipro_python_query, query_split_list)
        pool.close()
        pool.join()
        query_cut = []
        for p in query_list:
            query_cut += p
        print('query条数：%d' % len(query_cut))

        code_data = [i[2][0][0] for i in python_list]
        code_split_list = [code_data[i:i + self.split_num] for i in range(0, len(code_data), self.split_num)]
        pool = ThreadPool(10)
        code_list = pool.map(self.multipro_python_code, code_split_list)
        pool.close()
        pool.join()
        code_cut = []
        for p in code_list:
            code_cut += p
        print('code条数：%d' % len(code_cut))

        qids = [i[0] for i in python_list]
        print(qids[0])
        print(len(qids))

        return acont1_cut, acont2_cut, query_cut, code_cut, qids

    def parse_sqlang(self, sqlang_list):
        acont1_data = [i[1][0][0] for i in sqlang_list]
        acont1_split_list = [acont1_data[i:i + self.split_num] for i in range(0, len(acont1_data), self.split_num)]
        pool = ThreadPool(10)
        acont1_list = pool.map(self.multipro_sqlang_context, acont1_split_list)
        pool.close()
        pool.join()
        acont1_cut = []
        for p in acont1_list:
            acont1_cut += p
        print('acont1条数：%d' % len(acont1_cut))

        acont2_data = [i[1][1][0] for i in sqlang_list]
        acont2_split_list = [acont2_data[i:i + self.split_num] for i in range(0, len(acont2_data), self.split_num)]
        pool = ThreadPool(10)
        acont2_list = pool.map(self.multipro_sqlang_context, acont2_split_list)
        pool.close()
        pool.join()
        acont2_cut = []
        for p in acont2_list:
            acont2_cut += p
        print('acont2条数：%d' % len(acont2_cut))

        query_data = [i[3][0] for i in sqlang_list]
        query_split_list = [query_data[i:i + self.split_num] for i in range(0, len(query_data), self.split_num)]
        pool = ThreadPool(10)
        query_list = pool.map(self.multipro_sqlang_query, query_split_list)
        pool.close()
        pool.join()
        query_cut = []
        for p in query_list:
            query_cut += p
        print('query条数：%d' % len(query_cut))

        code_data = [i[2][0][0] for i in sqlang_list]
        code_split_list = [code_data[i:i + self.split_num] for i in range(0, len(code_data), self.split_num)]
        pool = ThreadPool(10)
        code_list = pool.map(self.multipro_sqlang_code, code_split_list)
        pool.close()
        pool.join()
        code_cut = []
        for p in code_list:
            code_cut += p
        print('code条数：%d' % len(code_cut))
        qids = [i[0] for i in sqlang_list]

        return acont1_cut, acont2_cut, query_cut, code_cut, qids

    def process_data(self):
        total_data = []
        with open(self.source_path, "rb") as f:
            corpus_lis = pickle.load(f)  # pickle

        if self.lang_type == 'python':
            parse_acont1, parse_acont2, parse_query, parse_code, parse_qids = self.parse_python(corpus_lis)

        elif self.lang_type == 'sqlang':
            parse_acont1, parse_acont2, parse_query, parse_code, parse_qids = self.parse_sqlang(corpus_lis)

        for acont1, acont2, query, code, qid in zip(parse_acont1, parse_acont2, parse_query, parse_code, parse_qids):
            total_data.append((qid, [acont1, acont2], [[code], [code]], [query]))

        with open(self.save_path, 'wb') as f:
            pickle.dump(total_data, f)

        return total_data


if __name__ == '__main__':
    lang_type = 'python'
    split_num = 500
    source_path = 'xxxxx'
    save_path = 'xxxxx'

    tokenizer = ParallelTokenizer(lang_type, split_num, source_path, save_path)
    tokenizer.process_data()

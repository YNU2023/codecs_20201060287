# 软件工程实习

## 项目说明

该项目为云南大学 2023Spring 软件工程课程提供的demo代码，用于学习软件的组织结构。

由于仅需结构性调整，不要求代码的调试和运行，在此删去了数据集，调整后的项目结构如下：
```
├── data_preprocessing  
│   └── hnn_processing  
│        └── embaddings_process.py  
│        └── getStru2Vec.py
│        └── process_single_corpus.py
│        └── python_structured.py
│        └── sqlang_structured.py
│        └── word_dirt.py
└── ANN_Staqc_new 
```
这里主要修改的是`data_preprocessing`文件夹下的`hnn_processing`,没有对ANN_Staqc_new文件夹下的模型进行优化。

源文件是代码组织方式较为杂乱随性，在此使用了面向对象的方式进行了重构，使得代码更加清晰易懂。

## 文件说明

### `embddings_process.py` 文件说明

该文件提供了用于处理词向量、构建字典和序列化数据的功能。以下是对该文件中的各个类和方法的说明：

#### `WordVectorUtils` 类

该类提供了加载和保存词向量模型的功能。

##### 方法：

- `__init__(self, vec_path)`: 构造方法，接受词向量文件的路径作为参数。
- `load_word_vectors(self)`: 加载词向量模型，返回 `KeyedVectors` 对象。
- `save_word_vectors(self, model, output_path)`: 保存词向量模型到指定路径。

#### `DictionaryBuilder` 类

该类提供了构建字典的功能。

##### 方法：

- `__init__(self, word_vec_path)`: 构造方法，接受词向量文件路径作为参数。
- `build_dictionary(self, type_vec_path, type_word_path, final_vec_path, final_word_path)`: 构建字典的方法，接受用于构建字典的文件路径，并将最终的字典和词向量保存到指定路径。

#### `DataSerialization` 类

该类提供了数据序列化的功能。

##### 方法：

- `__init__(self, word_dict_path)`: 构造方法，接受字典文件路径作为参数。
- `get_index(self, word_type, text, word_dict)`: 根据给定的文本和字典，获取文本对应的索引序列。
- `serialize_data(self, type_path, final_type_path, word_dict_path)`: 序列化数据的方法，根据给定的类型文件和字典，将文本转换为索引序列，并将最终的序列化数据保存到指定路径。

请将代码和文件路径替换为实际的值，并根据需要进行调整。

请确保在运行代码之前，已经安装了所需的依赖项（如 gensim 库），并提供正确的文件路径和数据文件。运行后，将会输出 "完成" 表示相应的操作已经完成。

2. `getStru2Vec.py`
3. `process_single_corpus.py`
4. `python_structured.py`
5. `sqlang_structured.py`
6. `word_dirt.py`
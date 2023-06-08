# 软件工程实习 实验
20201060287 李昂

## 目录

- [一、项目说明](#一项目说明)
- [二、文件说明](#二文件说明)
  - [2.1 getSru2Vec.py文件](#getsru2vecpy文件)
  - [2.2 embddings_process.py文件](#embddings_processpy文件)
  - [2.3 process_single_corpus.py文件](#process_single_corpuspy文件)
  - [2.4 python_structured.py文件](#python_structuredpy文件)
  - [2.5 sqlang_structured.py文件](#sqlang_structuredpy文件)
  - [2.6 word_dict.py文件](#word_dictpy文件)
- [三、后记](#三后记)

## 一、项目说明

该项目为云南大学 2023Spring 软件工程课程提供的demo代码，用于学习软件架构。

由于仅要求调整代码结构而不要求代码运行，为了加快`Git`推送速度，在此删去了数据集，调整后的项目结构如下：
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
**源文件的代码组织方式较为杂乱随性，此仓库存储的是经过本人重构后的代码。**

此仓库通过删改注释、删除重复代码段、使用面向对象的方式将特定的功能封装成类等方法，增加代码的可读性和易用性。

本仓库主要修改`data_preprocessing`文件夹下的`hnn_processing`目录,并没有对ANN_Staqc_new文件夹下的具体模型进行优化。

## 二、文件说明

### getSru2Vec.py文件

#### 1. 概述
该文件实现了一个并行分词类 `ParallelTokenizer`，用于解析结构化数据。它依赖于模块 `python_structured` 和 `sqlang_structured`，用于解析不同类型的数据。该类支持 Python 和 SQLang 两种语言的解析。

#### 2. 导入依赖库
该文件导入了以下依赖库：
- `pickle`：用于读取和写入 pickle 文件
- `sys`：提供对 Python 解释器的访问和控制
- `multiprocessing.Pool`：用于实现并行任务的线程池

#### 3. 导入自定义模块
该文件导入了两个自定义模块：
- `python_structured`：Python 结构化数据解析模块
- `sqlang_structured`：SQLang 结构化数据解析模块

#### 4. 并行分词类 `ParallelTokenizer`
该类用于并行解析结构化数据。它具有以下属性和方法：

##### 属性
- `lang_type`：解析的语言类型，可以是 'python' 或 'sqlang'
- `split_num`：每次并行解析的数据量
- `source_path`：源数据路径
- `save_path`：解析后数据保存路径

##### 方法
- `__init__(self, lang_type, split_num, source_path, save_path)`：初始化方法，设置类属性的初始值
- `multipro_python_query(self, data_list)`：Python 查询解析方法
- `multipro_python_code(self, data_list)`：Python 代码解析方法
- `multipro_python_context(self, data_list)`：Python 上下文解析方法
- `multipro_sqlang_query(self, data_list)`：SQLang 查询解析方法
- `multipro_sqlang_code(self, data_list)`：SQLang 代码解析方法
- `multipro_sqlang_context(self, data_list)`：SQLang 上下文解析方法
- `parse_python(self, python_list)`：解析 Python 数据的方法
- `parse_sqlang(self, sqlang_list)`：解析 SQLang 数据的方法
- `process_data(self)`：数据处理方法，实现数据解析和保存

#### 5. 示例运行
文件末尾的示例代码演示了如何使用 `ParallelTokenizer` 类进行数据解析。通过设置相关参数，选择解析的语言类型、并行解析的数据量，以及源数据和保存路径。然后调用 `process_data` 方法开始解析和保存数据。

请根据实际需求修改示例代码中的参数，并确保导入的自定义模块和相关文件存在。

---

### embddings_process.py文件

#### 1. 概述
该文件包含了几个类和相关方法，用于处理词向量和数据序列化的任务。

#### 2. 导入依赖库
该文件导入了以下依赖库：
- `pickle`：用于读取和写入 pickle 文件
- `numpy`：用于处理数组和矩阵的库
- `gensim.models.KeyedVectors`：用于加载和保存词向量模型

#### 3. 类和方法说明

##### 3.1. 类 `WordVectorUtils`
该类提供了加载和保存词向量模型的功能。

###### 属性
- `vec_path`：词向量文件的路径

###### 方法
- `__init__(self, vec_path)`：初始化方法，设置词向量文件的路径
- `load_word_vectors(self)`：加载词向量模型的方法，返回加载的词向量模型对象
- `save_word_vectors(self, model, output_path)`：保存词向量模型的方法，将词向量模型对象保存到指定路径

##### 3.2. 类 `DictionaryBuilder`
该类用于构建字典，将词语映射为索引。

###### 属性
- `word_vec_path`：词向量文件的路径

###### 方法
- `__init__(self, word_vec_path)`：初始化方法，设置词向量文件的路径
- `build_dictionary(self, type_vec_path, type_word_path, final_vec_path, final_word_path)`：构建字典的方法，接收类型向量文件路径、类型词语文件路径、最终向量文件路径和最终词语文件路径作为参数，将构建的字典和向量保存到指定路径

##### 3.3. 类 `DataSerialization`
该类用于数据序列化，将文本转换为索引序列。

###### 属性
- `word_dict_path`：字典文件的路径

###### 方法
- `__init__(self, word_dict_path)`：初始化方法，设置字典文件的路径
- `get_index(self, word_type, text, word_dict)`：获取索引序列的方法，接收词语类型、文本内容和字典作为参数，返回对应的索引序列
- `serialize_data(self, type_path, final_type_path, word_dict_path)`：数据序列化方法，接收类型文件路径、最终类型文件路径和字典文件路径作为参数，将数据序列化后保存到指定路径

#### 4. 示例运行
文件末尾的示例代码演示了如何使用上述类进行词向量加载、字典构建和数据序列化的操作。请根据实际需求修改示例代码中的参数，确保相关文件存在，并按照需要的功能调用相应的方法。

---

### process_single_corpus.py文件

#### 1. 概述
该文件包含了一个名为 `DataProcessor` 的类，用于处理数据。它包括了一些静态方法来处理数据，如解析、分割和保存数据。

#### 2. 导入依赖库
该文件导入了以下依赖库：
- `pickle`：用于读取和写入 pickle 文件
- `Counter`：用于计数数据中元素的频率

#### 3. 类 `DataProcessor`
该类用于处理数据，具有以下属性和方法：

##### 属性
- `__init__(self)`：初始化方法

##### 方法
- `data_staqc_prpcessing(filepath, save_single_path, save_mutiple_path)`：将数据按照单候选和多候选进行分割和保存
- `data_large_prpcessing(filepath, save_single_path, save_mutiple_path)`：将大规模数据按照单候选和多候选进行分割和保存
- `single_unlable2lable(path1, path2)`：将单候选数据转换为带标签的数据

#### 4. 示例运行
文件末尾的示例代码演示了如何使用 `DataProcessor` 类来处理数据。首先设置相关参数，包括文件路径和保存路径。然后调用对应的方法进行数据处理和保存。请根据实际需求修改示例代码中的参数，并确保相关文件存在。

注意：示例代码中的文件路径（'xxxxx'）需要根据实际情况进行修改。

---

### python_structured.py文件

#### 1. 概述
该文件实现了两个类：`PythonParser` 和 `PythonRefactor`。`PythonParser` 类用于解析 Python 代码，修复代码中的变量命名问题。`PythonRefactor` 类使用 `PythonParser` 类进行代码重构，添加变量名的注释。

#### 2. 导入依赖库
该文件导入了以下依赖库：
- `re`：用于正则表达式匹配和替换
- `token` 和 `tokenize`：用于解析 Python 代码中的 token
- `io.StringIO`：用于在内存中操作字符串作为文件
- `inflection`：用于进行单词的单复数转换
- `nltk`：自然语言处理工具包，用于词性标注、分词和词形还原

#### 3. 类 `PythonParser`
该类用于解析 Python 代码，修复代码中的变量命名问题。它具有以下属性和方法：

##### 属性
- `code`：待解析的 Python 代码
- `varnames`：代码中的变量名集合
- `tokenized_code`：代码中的 token 列表
- `bool_failed_var`：表示变量修复是否失败的布尔值
- `bool_failed_token`：表示 token 解析是否失败的布尔值
- `wnler`：WordNetLemmatizer 对象，用于词形还原
- `pattern_var_equal`：匹配变量赋值语句的正则表达式模式
- `pattern_var_for`：匹配变量迭代语句的正则表达式模式
- `pattern_case1_in`：匹配交互式输入语句（Case 1）中的输入标识
- `pattern_case1_out`：匹配交互式输入语句（Case 1）中的输出标识
- `pattern_case1_cont`：匹配交互式输入语句（Case 1）中的续行标识
- `pattern_case2_in`：匹配交互式输入语句（Case 2）中的输入标识
- `pattern_case2_cont`：匹配交互式输入语句（Case 2）中的续行标识
- `patterns`：用于匹配不同情况的正则表达式模式列表

##### 方法
- `__init__(self, code)`：初始化方法，设置类属性的初始值
- `repair_program_io(self, code)`：修复代码中的 I/O 错误
- `repair_program_token(self, code_list)`：修复代码中的 token 错误
- `tokenize_python_code(self, code)`：解析 Python 代码，生成 token 列表
- `get_repaired_code(self, code)`：修复代码中的变量命名问题
- `repair_variable_assignment(self, code, name)`：修复变量赋值语句中的变量命名
- `repair_variable_iteration(self, code, name)`：修复变量迭代语

句中的变量命名
- `repair_variable_usage(self, code, name)`：修复变量使用语句中的变量命名
- `repair_program(self)`：修复整个程序

#### 4. 类 `PythonRefactor`
该类使用 `PythonParser` 类进行代码重构，添加变量名的注释。它具有以下属性和方法：

##### 属性
- `code`：待重构的 Python 代码
- `parser`：PythonParser 对象，用于解析和修复代码

##### 方法
- `__init__(self, code)`：初始化方法，设置类属性的初始值
- `add_comments(self, code)`：向代码中添加注释
- `refactor(self)`：重构代码

#### 5. 示例用法
该文件末尾提供了一个示例用法，演示了如何使用 `PythonRefactor` 类对代码进行重构，并打印出重构后的代码。

---

### sqlang_structured.py文件

#### 1. 概述
这段代码是一个SQL解析器，用于解析和标记SQL查询语句中的各种标记类型。使将SQL查询语句作为输入，并对其进行标记化和分类，包括函数、关键字、表、提供了方法来获取标记类型和标识符列表。

#### 2. 导入依赖库
该文件导入了以下依赖库：
- `re`：用于正则表达式操作
- `inflection`：用于词形转换
- `sqlparse`：用于解析 SQL 语句
- `nltk`：用于自然语言处理任务

#### 3. 类 `SqlangParser`
该类用于解析 SQLang 语言的 SQL 代码。它具有以下属性和方法：

##### 属性
- `sql`：要解析的 SQL 语句
- `idMap`：标识符映射字典，用于映射表名和列名的标识符
- `idMapInv`：反向标识符映射字典，用于反向映射标识符和原始名称
- `idCount`：标识符计数，用于生成唯一的标识符名称
- `regex`：是否使用正则表达式进行分词
- `parseTreeSentinel`：解析树标志，用于标记解析树的根节点
- `tableStack`：表堆栈，用于跟踪嵌套的表引用
- `parse`：解析树列表，用于保存解析后的树形结构
- `tokens`：解析后的标记列表

##### 方法
- `__init__(self, sql, regex=False, rename=True)`：初始化方法，接受要解析的 SQL 语句、是否使用正则表达式进行分词和是否重命名标识符作为参数
- `sanitizeSql(self, sql)`：清理 SQL 语句的辅助方法，去除多余的空格和添加缺失的分号
- `removeWhitespaces(self, p)`：移除解析树中的空白符
- `identifyLiterals(self, p)`：识别解析树中的文本字面量
- `identifySubQueries(self, p)`：识别解析树中的子查询
- `identifyFunctions(self, p)`：识别解析树中的函数
- `identifyTables(self, p)`：识别解析树中的表名
- `parseStrings(self, p)`：解析树中的字符串字面量
- `renameIdentifiers(self, p)`：重命名解析树中的标识符
- `getTokens(self, parseTree)`：从解析树中提取标记
- `lemmatize(self, word)`：对单词进行词形还原

- `generateTokens(self)`：生成标记列表
- `tokenize(self)`：执行分词，返回标记列表
- `get_token_types(self)`：获取标记的类型列表
- `get_identifiers(self)`：获取解析后的标识符列表

#### 4. 使用示例
代码末尾的使用示例中，创建了一个 `SqlangParser` 的实例，并使用给定的 SQL 语句进行初始化。然后，分别获取了标记的类型列表和解析后的标识符列表，并将它们打印出来。

---

### word_dict.py文件

#### 1. 概述
该文件包含了一些用于处理词汇表的函数。主要功能是从给定的语料中构建词汇表，并对词汇表进行处理和保存。

#### 2. 导入依赖库
该文件导入了以下依赖库：
- `pickle`：用于读取和写入 pickle 文件

#### 3. 函数说明

##### 3.1 `get_vocab(corpus1, corpus2)`
该函数用于从两个语料中获取词汇表。它遍历语料中的元素，并将每个元素中的单词添加到词汇表中。函数的参数为两个语料列表 `corpus1` 和 `corpus2`，返回值为词汇表 `word_vocab`。注意，在函数的实现中，语料中的元素结构是通过索引进行访问的。

##### 3.2 `load_pickle(filename)`
该函数用于从 pickle 文件中加载数据。它接收一个文件名 `filename`，并返回加载的数据。函数使用 pickle 模块的 `load` 函数来读取 pickle 文件。

##### 3.3 `vocab_processing(filepath1, filepath2, save_path)`
该函数用于构建初步词汇表。它从指定的文件路径 `filepath1` 和 `filepath2` 中读取语料数据，然后调用 `get_vocab` 函数获取词汇表，并将词汇表保存到指定的文件路径 `save_path` 中。

##### 3.4 `final_vocab_processing(filepath1, filepath2, save_path)`
该函数用于最终的词汇表处理。它从指定的文件路径 `filepath1` 和 `filepath2` 中读取语料数据，并读取之前构建的词汇表数据。然后调用 `get_vocab` 函数获取最终的词汇表，并将词汇表中不在初步词汇表中的单词保存到指定的文件路径 `save_path` 中。

#### 4. 示例运行
文件末尾的示例代码展示了如何运行上述函数来处理词汇表。首先，定义了一些文件路径变量。然后，分别调用 `final_vocab_processing` 函数来处理 SQL 和 Python 的词汇表。请根据实际需求修改示例代码中的文件路径。

注意：在示例代码中的文件路径部分，将 `xxxxx` 替换为实际的文件路径。

请确保相关文件存在，并在运行代码之前满足所需的文件和数据准备工作。

## 三、后记

**警告：**

**虽然本着不修改代码具体内容仅改动项目结构的思想，但由于不了解该科研任务的具体要求、不清晰相应模块的具体调用方式等因素，仍不可避免的改动了少量代码，可能对实验产生影响，导致代码报错。**

**若运行出现问题，请在`Issues`中提交您的问题或通过邮箱`20201060287@mail.ynu.edu.cn`联系**

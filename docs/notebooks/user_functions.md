# Most harmless user function of Python



```python
from typing import List
import pandas as pd
def merge_df_list(df_left: pd.DataFrame, dfs_right: List[pd.DataFrame], keys: List[str], methods: List[str]) -> pd.DataFrame:
    """
    功能：横向合并多个df
    参数：
    df_left: 最左边的df
    df_list：需要合并的df列表(除最左边的以外)
    keys：合并df所需要的key列表，需要与df_list一一对应, 列表元素为一个二元元组，元组元素为str列表
    methods: 合并df所需要的方法列表，需要与df_list一一对应

    返回值：合并后的df
    """
    # 将最左边的数据帧赋值给df_merged
    df_merged = df_left
    # 使用zip函数同时迭代df_right，keys和methods列表
    for df, key, method in zip(dfs_right, keys, methods):
        # 使用指定的键和方法合并当前数据帧与df_merged
        df_merged = df_merged.merge(df, left_on=key[0], right_on=key[1], how=method)
    # 返回合并后的数据帧
    return df_merged

# 示例代码：
if __name__ == "__main__":
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 6]})
    df2 = pd.DataFrame({"B": [1, 2, 9], "C": [10, 11, 12]})
    df3 = pd.DataFrame({"C": [10, 3, 15], "D": [16, 17, 18]})


    df_left = df1
    df_right = [df2, df3]
    keys = [("B","B"),("C","C")]
    methods = ['inner','outer']

    merged_df = merge_df_list(df_left,df_right, keys,methods)
    print(f"df1: \n {df1} \n")
    print(f"df1: \n {df2} \n")
    print(f"df1: \n {df3} \n")
    print(f"merged df: \n {merged_df} \n")

```

    df1: 
        A  B
    0  1  1
    1  2  2
    2  3  6 
    
    df1: 
        B   C
    0  1  10
    1  2  11
    2  9  12 
    
    df1: 
         C   D
    0  10  16
    1   3  17
    2  15  18 
    
    merged df: 
          A    B   C     D
    0  1.0  1.0  10  16.0
    1  2.0  2.0  11   NaN
    2  NaN  NaN   3  17.0
    3  NaN  NaN  15  18.0 
    


### 批量扫描文件夹并获取文件路径



```python
import re
import os
from typing import List, Generator

def scan_file_path(
    folder: str, 
    extensions: List[str], 
    exclude: str="^$", 
    recursive: bool=False) -> Generator[str, None, None]:
    """生成器函数，用于生成符合指定条件的文件路径。

    Args:
        folder (str): 要扫描的文件夹。
        extensions (List[str]): 要匹配的文件扩展名列表。
        exclude (str, optional): 要排除的通配符模式。默认为 "^$", 代表完全不排除。
        recursive (bool, optional): 是否递归到子目录。默认为 False。

    Yields:
        str: 文件路径。
    """
    # 验证输入文件夹
    if not os.path.isdir(folder):
        raise ValueError("'{}' 不是存在的文件夹".format(folder))
    # 使用 os.scandir 遍历文件夹中的条目
    with os.scandir(folder) as it:
        for entry in it:
            # 检查条目是否为文件，并且其名称是否与扩展名和排除模式匹配
            if (entry.is_file() 
                and entry.name.endswith(tuple(extensions)) 
                and not re.search(exclude, entry.path)):
                # 输出文件路径
                yield entry.path
            # 检查条目是否为目录，并且是否启用递归扫描
            elif entry.is_dir() and recursive:
                # 递归到子目录
                yield from scan_file_path(entry.path, extensions, exclude, recursive)



# 示例代码
if __name__ == "__main__":
  extensions = ['.csv','.dta']
  folder = "." 
  exclude = r".csv$"
  paths1 = scan_file_path(folder,extensions,recursive=True)
  paths2 = scan_file_path(folder,extensions,recursive=True,exclude=exclude)

  for path in paths1:
    print(f"未排除csv文件的路径如下: \n {path} \n")

  for path in paths2:
    print(f"排除csv文件的路径如下: \n {path} \n")
```

    未排除csv文件的路径如下: 
     ./assets/auto.dta 
    
    未排除csv文件的路径如下: 
     ./assets/auto.csv 
    
    排除csv文件的路径如下: 
     ./assets/auto.dta 
    



```python
from typing import Dict, Any
def dict_to_df(_dict: Dict[Any, Any], key_name: str, value_name: str) -> pd.DataFrame:
    """
    字典转换为一个dataframe, 字典键对应第一列，字典值第二列。

    参数：
    _dict (Dict[Any, Any]): 字典。
    key_name (str): 字典的keys对应的列名。
    value_name (str): 字典的values对应的列名。
    
    返回值：
    df(pd.DataFrame): 一个两列dataframe，第一列对应字典的keys，第二列对应字典的values。
    """
    df = (pd.DataFrame.from_dict(_dict, orient='index', columns=[value_name])
        .rename_axis(key_name))
  
    return df

if __name__ == "__main__":
    # 定义测试字典
    test_dict = {'a': 1, 'b': 2, 'c': 3}

    # 调用 dict_to_df 函数
    df = dict_to_df(test_dict, 'key', 'value')

    # 打印输出结果，查看是否符合预期
    print(f"{test_dict} \n")
    print(f"{df} \n")

```

    {'a': 1, 'b': 2, 'c': 3} 
    
         value
    key       
    a        1
    b        2
    c        3 
    



```python
import pandas as pd
from typing import Generator, List

def stata_to_chunks(
    file_path: str, 
    chunksize: int=1000, 
    keep_data: str = 'all', 
    convert_categoricals:bool=False,
    preserve_dtypes:bool=False,
    convert_missing:bool=True,
    usecols:List[str]|None=None) -> Generator:
    """
    读取 Stata 文件并返回数据和标签。
    
    参数:
    file_path (str): Stata 文件的路径。
    chunksize (int): 读取stata文件的数据块的大小。
    keep_data (str): 保留数据的类型, 'all'为数据和标签，'only_label'仅标签，'only_data'仅数据，默认为'all'。
    convert_categoricals (bool): 是否转换原始值为值标签对应值，默认值为False。注意，有些文件转换会报错。
    convert_missing (bool): 是否以stata缺失值类型存储，默认值为True。
    usecols (List[str]|None): 保留的列，默认值None保留所有列。

    
    返回值:
    Generator: 返回一个(DataFrame)生成器。
    """
    
    # 创建 StataReader 并设置参数。
    reader = pd.read_stata(
        file_path, 
        chunksize=chunksize, 
        convert_categoricals=convert_categoricals,
        preserve_dtypes=preserve_dtypes,
        convert_missing=convert_missing,
        columns=usecols)
    # 如果保留标签信息
    if keep_data in ['all','only_label']:
        # 获取Stata文件的变量标签dataframe
        variable_labels = dict_to_df(
            reader.variable_labels(),
            key_name='_column_name',
            value_name='_column_label').reset_index()
        # 获取Stata文件的值标签dataframe
        value_labels = dict_to_df(
            reader.value_labels(),
            key_name='_value_label_name',
            value_name='_value_label').reset_index()
        # Outer横向合并生成标签dataframe
        label = pd.merge(
            variable_labels,
            value_labels,
            left_on='_column_name',
            right_on='_value_label_name',
            how='outer',
            copy=False)

        if keep_data == "only_label":
            # 仅返回label信息
            yield label
            
        else: 
            # 返回包含标签和数据的信息
            for df in reader:
                labels = pd.concat([label,df],axis=1,join='outer')
                yield labels
    elif keep_data == "only_data":
        # 仅返回数据数据dataframe块
        yield from reader
    
    else:
        # 返回错误
        raise ValueError(f"paramter 'keep_data' in function 'stata_to_chunks()' got an unexpected value '{keep_data}'")


# 函数调用示例：
if __name__ == "__main__":
    # 生成两个示例的df chunks生成器
    data1 = stata_to_chunks("http://www.principlesofeconometrics.com/stata/cps.dta",chunksize=2500)
    data2 = stata_to_chunks("http://www.principlesofeconometrics.com/stata/cps.dta",chunksize=2500,keep_data="only_label")
    data3 = stata_to_chunks("http://www.principlesofeconometrics.com/stata/cps.dta",chunksize=2500,keep_data="only_data")
   
    # # 遍历生成器
    for index, df in enumerate(data1):
        print(f"生成器data1中的df块{index+1}:\n {df}")
        print(df.dtypes, "\n")
    for index, df in enumerate(data2):
        print(f"生成器data2中的df块{index+1}:\n {df}")
    for index, df in enumerate(data3):
        print(f"生成器data3中的df块{index+1}:\n {df}")
```

    生成器data1中的df块1:
          _column_name       _column_label _value_label_name _value_label  wage  \
    0            wage   earnings per hour               NaN          NaN  1.05   
    1            educ  years of education               NaN          NaN  1.05   
    2             age        age in years               NaN          NaN  1.23   
    3           exper          experience               NaN          NaN  1.28   
    4          female        =1 if female               NaN          NaN  1.34   
    ...           ...                 ...               ...          ...   ...   
    2495          NaN                 NaN               NaN          NaN  8.84   
    2496          NaN                 NaN               NaN          NaN  8.84   
    2497          NaN                 NaN               NaN          NaN  8.84   
    2498          NaN                 NaN               NaN          NaN  8.84   
    2499          NaN                 NaN               NaN          NaN  8.84   
    
          educ   age  exper  female  black  white  married  union  northeast  \
    0     12.0  37.0   19.0     0.0    0.0    1.0      0.0    1.0        0.0   
    1     13.0  42.0   23.0     0.0    0.0    1.0      0.0    0.0        1.0   
    2      8.0  54.0   40.0     0.0    0.0    1.0      0.0    0.0        0.0   
    3     10.0  59.0   43.0     1.0    0.0    1.0      1.0    1.0        1.0   
    4     18.0  28.0    4.0     1.0    0.0    1.0      0.0    0.0        0.0   
    ...    ...   ...    ...     ...    ...    ...      ...    ...        ...   
    2495  14.0  43.0   23.0     0.0    0.0    1.0      0.0    0.0        0.0   
    2496  13.0  24.0    5.0     1.0    0.0    1.0      0.0    0.0        0.0   
    2497  12.0  57.0   39.0     0.0    1.0    0.0      1.0    0.0        0.0   
    2498  14.0  24.0    4.0     0.0    1.0    0.0      0.0    0.0        0.0   
    2499  13.0  21.0    2.0     1.0    0.0    1.0      0.0    0.0        1.0   
    
          midwest  south  west  fulltime  metro  
    0         0.0    0.0   1.0       1.0    1.0  
    1         0.0    0.0   0.0       1.0    1.0  
    2         0.0    0.0   1.0       1.0    1.0  
    3         0.0    0.0   0.0       0.0    1.0  
    4         0.0    0.0   1.0       1.0    0.0  
    ...       ...    ...   ...       ...    ...  
    2495      0.0    0.0   1.0       0.0    0.0  
    2496      0.0    1.0   0.0       1.0    1.0  
    2497      1.0    0.0   0.0       1.0    1.0  
    2498      0.0    1.0   0.0       1.0    1.0  
    2499      0.0    0.0   0.0       1.0    1.0  
    
    [2500 rows x 19 columns]
    _column_name          object
    _column_label         object
    _value_label_name     object
    _value_label          object
    wage                 float64
    educ                 float64
    age                  float64
    exper                float64
    female               float64
    black                float64
    white                float64
    married              float64
    union                float64
    northeast            float64
    midwest              float64
    south                float64
    west                 float64
    fulltime             float64
    metro                float64
    dtype: object 
    
    生成器data1中的df块2:
          _column_name       _column_label _value_label_name _value_label  \
    0            wage   earnings per hour               NaN          NaN   
    1            educ  years of education               NaN          NaN   
    2             age        age in years               NaN          NaN   
    3           exper          experience               NaN          NaN   
    4          female        =1 if female               NaN          NaN   
    ...           ...                 ...               ...          ...   
    4728          NaN                 NaN               NaN          NaN   
    4729          NaN                 NaN               NaN          NaN   
    4730          NaN                 NaN               NaN          NaN   
    4731          NaN                 NaN               NaN          NaN   
    4732          NaN                 NaN               NaN          NaN   
    
               wage  educ   age  exper  female  black  white  married  union  \
    0           NaN   NaN   NaN    NaN     NaN    NaN    NaN      NaN    NaN   
    1           NaN   NaN   NaN    NaN     NaN    NaN    NaN      NaN    NaN   
    2           NaN   NaN   NaN    NaN     NaN    NaN    NaN      NaN    NaN   
    3           NaN   NaN   NaN    NaN     NaN    NaN    NaN      NaN    NaN   
    4           NaN   NaN   NaN    NaN     NaN    NaN    NaN      NaN    NaN   
    ...         ...   ...   ...    ...     ...    ...    ...      ...    ...   
    4728  47.220001  18.0  59.0   35.0     0.0    0.0    1.0      1.0    1.0   
    4729  56.480000   9.0  63.0   48.0     0.0    0.0    1.0      1.0    0.0   
    4730  60.189999  16.0  55.0   33.0     0.0    0.0    1.0      1.0    1.0   
    4731  74.320000  18.0  41.0   17.0     0.0    0.0    1.0      1.0    0.0   
    4732  78.709999  18.0  63.0   39.0     1.0    0.0    1.0      0.0    0.0   
    
          northeast  midwest  south  west  fulltime  metro  
    0           NaN      NaN    NaN   NaN       NaN    NaN  
    1           NaN      NaN    NaN   NaN       NaN    NaN  
    2           NaN      NaN    NaN   NaN       NaN    NaN  
    3           NaN      NaN    NaN   NaN       NaN    NaN  
    4           NaN      NaN    NaN   NaN       NaN    NaN  
    ...         ...      ...    ...   ...       ...    ...  
    4728        1.0      0.0    0.0   0.0       0.0    1.0  
    4729        0.0      1.0    0.0   0.0       0.0    1.0  
    4730        0.0      0.0    0.0   1.0       0.0    1.0  
    4731        1.0      0.0    0.0   0.0       0.0    1.0  
    4732        0.0      0.0    1.0   0.0       0.0    1.0  
    
    [2248 rows x 19 columns]
    _column_name          object
    _column_label         object
    _value_label_name     object
    _value_label          object
    wage                 float64
    educ                 float64
    age                  float64
    exper                float64
    female               float64
    black                float64
    white                float64
    married              float64
    union                float64
    northeast            float64
    midwest              float64
    south                float64
    west                 float64
    fulltime             float64
    metro                float64
    dtype: object 
    
    生成器data2中的df块1:
        _column_name                     _column_label _value_label_name  \
    0          wage                 earnings per hour               NaN   
    1          educ                years of education               NaN   
    2           age                      age in years               NaN   
    3         exper                        experience               NaN   
    4        female                      =1 if female               NaN   
    5         black                       =1 if black               NaN   
    6         white                       =1 if white               NaN   
    7       married                     =1 if married               NaN   
    8         union                =1 if union member               NaN   
    9     northeast                   =1 if northeast               NaN   
    10      midwest                     =1 if midwest               NaN   
    11        south                       =1 if south               NaN   
    12         west                        =1 if west               NaN   
    13     fulltime            =1 if full time worker               NaN   
    14        metro  =1 if lives in metropolitan area               NaN   
    
       _value_label  
    0           NaN  
    1           NaN  
    2           NaN  
    3           NaN  
    4           NaN  
    5           NaN  
    6           NaN  
    7           NaN  
    8           NaN  
    9           NaN  
    10          NaN  
    11          NaN  
    12          NaN  
    13          NaN  
    14          NaN  
    生成器data3中的df块1:
           wage  educ   age  exper  female  black  white  married  union  \
    0     1.05  12.0  37.0   19.0     0.0    0.0    1.0      0.0    1.0   
    1     1.05  13.0  42.0   23.0     0.0    0.0    1.0      0.0    0.0   
    2     1.23   8.0  54.0   40.0     0.0    0.0    1.0      0.0    0.0   
    3     1.28  10.0  59.0   43.0     1.0    0.0    1.0      1.0    1.0   
    4     1.34  18.0  28.0    4.0     1.0    0.0    1.0      0.0    0.0   
    ...    ...   ...   ...    ...     ...    ...    ...      ...    ...   
    2495  8.84  14.0  43.0   23.0     0.0    0.0    1.0      0.0    0.0   
    2496  8.84  13.0  24.0    5.0     1.0    0.0    1.0      0.0    0.0   
    2497  8.84  12.0  57.0   39.0     0.0    1.0    0.0      1.0    0.0   
    2498  8.84  14.0  24.0    4.0     0.0    1.0    0.0      0.0    0.0   
    2499  8.84  13.0  21.0    2.0     1.0    0.0    1.0      0.0    0.0   
    
          northeast  midwest  south  west  fulltime  metro  
    0           0.0      0.0    0.0   1.0       1.0    1.0  
    1           1.0      0.0    0.0   0.0       1.0    1.0  
    2           0.0      0.0    0.0   1.0       1.0    1.0  
    3           1.0      0.0    0.0   0.0       0.0    1.0  
    4           0.0      0.0    0.0   1.0       1.0    0.0  
    ...         ...      ...    ...   ...       ...    ...  
    2495        0.0      0.0    0.0   1.0       0.0    0.0  
    2496        0.0      0.0    1.0   0.0       1.0    1.0  
    2497        0.0      1.0    0.0   0.0       1.0    1.0  
    2498        0.0      0.0    1.0   0.0       1.0    1.0  
    2499        1.0      0.0    0.0   0.0       1.0    1.0  
    
    [2500 rows x 15 columns]
    生成器data3中的df块2:
                wage  educ   age  exper  female  black  white  married  union  \
    2500   8.840000  16.0  48.0   26.0     1.0    0.0    1.0      0.0    1.0   
    2501   8.840000  13.0  33.0   14.0     1.0    0.0    1.0      1.0    1.0   
    2502   8.840000  12.0  40.0   22.0     1.0    0.0    1.0      1.0    0.0   
    2503   8.840000  12.0  38.0   20.0     0.0    0.0    1.0      1.0    0.0   
    2504   8.840000  12.0  61.0   43.0     1.0    0.0    1.0      0.0    1.0   
    ...         ...   ...   ...    ...     ...    ...    ...      ...    ...   
    4728  47.220001  18.0  59.0   35.0     0.0    0.0    1.0      1.0    1.0   
    4729  56.480000   9.0  63.0   48.0     0.0    0.0    1.0      1.0    0.0   
    4730  60.189999  16.0  55.0   33.0     0.0    0.0    1.0      1.0    1.0   
    4731  74.320000  18.0  41.0   17.0     0.0    0.0    1.0      1.0    0.0   
    4732  78.709999  18.0  63.0   39.0     1.0    0.0    1.0      0.0    0.0   
    
          northeast  midwest  south  west  fulltime  metro  
    2500        1.0      0.0    0.0   0.0       1.0    1.0  
    2501        0.0      0.0    0.0   1.0       1.0    1.0  
    2502        0.0      0.0    1.0   0.0       1.0    1.0  
    2503        1.0      0.0    0.0   0.0       1.0    1.0  
    2504        1.0      0.0    0.0   0.0       1.0    0.0  
    ...         ...      ...    ...   ...       ...    ...  
    4728        1.0      0.0    0.0   0.0       0.0    1.0  
    4729        0.0      1.0    0.0   0.0       0.0    1.0  
    4730        0.0      0.0    0.0   1.0       0.0    1.0  
    4731        1.0      0.0    0.0   0.0       0.0    1.0  
    4732        0.0      0.0    1.0   0.0       0.0    1.0  
    
    [2233 rows x 15 columns]



```python
import sqlite3

def get_table_names(db_file: str) -> List[str]:
    """获取给定数据库中的表名列表。

    Args:
        db_file: 数据库文件的路径。

    Returns:
        数据库中的表名列表。
    """
    # 获取数据库中的所有表名
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [table[0] for table in cursor]

    # 如果给定的表名在列表中，则返回 True，否则返回 False
    return table_names

# 示例调用
print(get_table_names('my_database.db'))  # 输出：True 或 False


```

    ['table1_1', 'table2_1', 'table3_1', 'table1', 'table2', 'table3']



```python
import sqlite3
from typing import Tuple

def name_new_table(table_name: str, db_file: str, if_table_exists: str = 'replace') ->str | None:
    """
    输入与SQLite数据库表名不同的表名。

    参数：
    - table_name (str): 要重命名的表的当前名称。
    - db_file (str): SQLite数据库的文件路径。
    - if_table_exists (str): 当表名存在的处理方法, 可以为replace(删除原有表); 
        可以为rename(用户重新命名新表); 可以append(将数据纵向合并到原表)，默认值'replace'。

    返回值：
    - str | None: 包含原表名和新表名的元组。
    """
    # 当输入的表名已存在时，要求用户重新输入
    while is_table(table_name, db_file):
        new_table_name = input("表名已存在，请输入新的表名：")
        if new_table_name not in table_names:
            break

    return new_table_name

    else:
        return table_name

# 函数调用示例：
if __name__ == "__main__":
    table_name, new_table_name = input_unique_name('table1',"/home/kyrie/Documents/web/econrz/docs/notebooks/my_database.db")
    print(table_name,'\n')
    print(new_table_name, '\n')

```

    table1 
    
    hh 
    


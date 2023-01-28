from typing import List, Dict, Tuple, Iterable, Type, Union, Generator, Iterable
import pandas as pd
import os
from pathlib import Path
from collections import defaultdict
import itertools

def convert_dtypes(
    chunks: 'Iterable[pd.DataFrame]', 
    dtype: 'Union[Type, Dict[str, Type]]') -> 'Generator[pd.DataFrame, None, None]':
    """
    将df可迭代对象中的列转换为给定的数据类型。
    
    参数:
    ----------
    chunks : Type[pd.DataFrame], 一个包含数据框的可迭代对象。
    dtype : Union[Type, Dict[str, Type]]
        要转换的数据类型。如果提供了单个类型，则将所有列转换为该类
    """
    # 转换列数据类型的辅助函数
    def convert_column(chunk: 'pd.DataFrame', col: 'str', col_type: 'Type'):
        if col in chunk.columns:
            chunk[col] = chunk[col].astype(col_type)
        else:
            print(f"Column '{col}' not found in chunk, skipping conversion.")
    # 根据dtype参数类型转换列数据类型
    for chunk in chunks:
        if isinstance(dtype, dict):
            for col, col_type in dtype.items():
                convert_column(chunk, col, col_type)
        elif isinstance(dtype, Type):
            for col in chunk.columns:
                convert_column(chunk, col, dtype)
        else:
            raise Exception('dtype参数值类型错误：仅支持字典Dict[str, Type]或单个类型Type。')
        yield chunk



def read_dta(
    filepath: str,
    usecols: Union[List[str], None] = None,
    dtype: Union[Dict[str,Type], Type , None] = None,
    chunksize: Union[int, None] = None,
    )-> Union[pd.DataFrame , Iterable[pd.DataFrame]]:
    """读取dta文件为df
    
    参数：
    - filepath: str, stata文件路径。
    - usecols: List[str], 导入的列。
    - dtype: Dict[str, str] | str | None, 指定列的数据类型, 默认为None不指定。
    - chunksize: int | None, 数据帧大小，返回这个指定大小的数据帧的TextFileReader对象， 默认为None返回数据框。
    
    返回:
    Union[pd.DataFrame , Iterable[pd.DataFrame]], 返回为数据框或数据框迭代对象。
    """
    stata_reader = pd.read_stata(
        filepath, 
        columns=usecols, 
        convert_categoricals = False, 
        chunksize=chunksize)
    # 如果未指定chunksize, 当dtype参数指定时
    if (chunksize is None) and (dtype is not None):
        stata_reader = stata_reader.astype(dtype, inplace=True)
        return stata_reader
    # 如果指定chunksize, 当dtype参数指定时
    elif (chunksize is not None) and (dtype is not None) :
        return convert_dtypes(stata_reader, dtype)
    else:
        return stata_reader
   
    
def read_data(
    file_path: str,
    usecols: Union[List[str], None] = None,
    dtype: Union[Dict[str, Type], Type, None] = None,
    chunksize: Union[int,None] = None
)->Union[pd.DataFrame,Iterable[pd.DataFrame]]:
    """根据文件路径后缀读取文件为数据框或者数据帧。

    参数:
        file_path (str): 文件路径。
        usecols (Union[List[str], None], optional): 指定导入的列， 默认为None。
        dtype (Union[Dict[str, Type], Type, None], optional): 指定列的数据类型，默认为None。
        chunksize (int, optional): 返回数据帧的数量, 默认为None返回一个数据框。

    返回:
        Union[pd.DataFrame,Iterable[pd.DataFrame]]: 返回一个数据框或指定数量的数据帧。
    """
    # 设定支持的数据读取函数
    readers = {
        '.csv': pd.read_csv,
        '.xls': pd.read_excel,
        '.xlsx': pd.read_excel,
        '.dta': read_dta
    }
    
    # 根据文件路径后缀提取读取函数
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in readers.keys():
        raise ValueError("Unsupported file type.")
    else:
        reader = readers[ext](
            file_path,
            usecols=usecols,
            dtype=dtype,
            chunksize=chunksize)
        return reader   

def read_to_dfs(
    file_paths: Iterable[str],
    columns: Union[Dict[str,List[str]],None]=None,
    dtypes: Union[Dict[str,Dict[str,Type]],None]=None,
    chunksize: Union[int,None]=None   
)->Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]:
    """读取文件路径迭代器为元组迭代器，元组第一个元素为文件名，第二个元素为数据框或者数据帧。
    
    参数：
        file_paths (Iterable[str]): 文件路径可迭代对象。
        columns (Union[Dict[str,List[str]],None]): 选取的列，字典的键为文件名（不带后缀），默认为None。
        dtypes (Union[Dict[str,Dict[str,Type]],None]): 指定的列的数据类型，字典的键为文件名（不带后缀），默认为None。
        chunksize (Union[int,None]): 指定文件的chunksize，默认为None。如果不是None，将返回数据帧对象。
        
    返回：
        Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]: 元组迭代器，元组第一个元素为文件名，第二个元素为数据框或者数据帧。
        
    """ 
    for path in file_paths:
        # 获取文件名
        filename = Path(path).stem
        # 根据文件名提取参数
        usecols = columns.get(filename) if columns is not None else columns
        dtype = dtypes.get(filename) if dtypes is not None else dtypes
        # 读取数据
        data = read_data(path,usecols=usecols,dtype=dtype,chunksize=chunksize)
        # 创建生成器
        yield filename, data


def rename_dfs(
    df_tuples: Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]],
    column_mappings: Dict[str,Dict[str,str]],
)-> Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]:
    """重命名df元组迭代对象中的列

    参数:
        df_tuples (Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]): 需重命名的df元组，元组元素为df名和df。
        column_mappings (Dict[str,Dict[str,str]]): 列名嵌套字典，字典的键为df名，值为包含键为旧列名，值为新列名的字典。

    Returns:
        Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]: 元组迭代器，元组第一个元素为文件名，第二个元素为数据框或者数据帧。
    """
    # 遍历df_tuples中的元素
    for df_name, df_obj in df_tuples:
        # 提取对应df的列名映射
        column_mapping = column_mappings.get(df_name)
        # 当列名映射值不为None
        if column_mapping:
            # 当df_tuple中的df对象元素是单个df
            if isinstance(df_obj, pd.DataFrame):
                # 生成重命名列后的df_tuple
                yield df_name, df_obj.rename(columns=column_mapping, errors='raise')
            # 当df_tuple中的df对象是df迭代器
            elif isinstance(df_obj, Iterable) :
                # 生成重命名列后的df_tuple生成器
                yield df_name, (df.rename(columns=column_mapping, errors='raise') for df in df_obj)
        # 当列名映射值为None
        else:
            # 生成本身
            yield df_name, df_obj

def reshape_to_long_dfs(
    df_tuples: Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]],
    stubnames: Dict[str,Union[List[str],str]],
    ij_names : Dict[str, Tuple[Union[List[str],str],str]],
    seps: Dict[str,str]=defaultdict(lambda: '_')
)-> Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]:
    """批量转换df为宽格式

    参数:
        df_tuples (Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]): df元组(df_name, df)生成器。
        stubnames (Dict[str,Union[List[str],str]]): 转换后的宽格式列名。
        ij_names (Dict[str, Tuple[Union[List[str],str],str]]): 转换后的id变量和order变量。
        seps (Dict[str,str]): stubname和order变量的分割符。默认为下划线'_'

    Returns:
        Iterable[Tuple[str,Union[Iterable[pd.DataFrame],pd.DataFrame]]]: 返回df元组生成器。
    """
    for df_name, df_obj in df_tuples:
        # 获取对应df的参数
        stubname = stubnames.get(df_name)
        ij_name = ij_names.get(df_name)
        sep = seps.get(df_name)
        # 如果没有设定长转宽参数，则生成本身
        if all(val is None for val in (stubname, ij_name)):
            yield df_name, df_obj
        # 如果设定完整参数，则进行长转宽操作
        elif all(val is not None for val in (stubname, ij_name)):
            if isinstance(df_obj, pd.DataFrame):
                wide_df = pd.wide_to_long(
                    df_obj, 
                    stubnames=stubname, 
                    i=ij_name[0], 
                    j=ij_name[1],
                    sep=sep)
                yield df_name, wide_df
            elif isinstance(df_obj, Iterable):
                wide_dfs = (pd.wide_to_long(
                    df_obj, 
                    stubnames=stubname, 
                    i=ij_name[0], 
                    j=ij_name[1],
                    sep=sep))
                yield df_name, wide_dfs
        else:
            raise ValueError(f"{df_name}的宽转长参数设置不完整。")
                


    
        
        
        
        
        
    

                    

                
                
            
        
        
    


    
    
    

 
   
    

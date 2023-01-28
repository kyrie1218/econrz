import pandas as pd
from typing import List, Dict, Type, Union, Iterable
import os

def read_data(
    file_path: str,
    usecols: Union[List[str], None] = None,
    dtype: Union[Dict[str, Type], Type, None] = None,
    chunksize: int = None
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
        '.dta': import_stata
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
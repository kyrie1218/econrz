import os
import pandas as pd
from collections import defaultdict
from typing import List, Dict, Type, Tuple, Iterable, Union, Generator


def scan_data_dir(
    data_dir: str,
    file_types: List[str]= ['.csv'],
    exclude_files: List[str]= [],
    recursive: bool = False
)->Generator[str, None, None]:
    """扫描文件夹下的数据文件路径

      参数:
        - data_dir: str, 需扫描的文件夹。
        - file_types: List[str], 数据文件的类型, 可选，默认['.csv']。
        - exclude_files: List[str], 需排除的带后缀数据文件名，可选，默认[]。
        - recursive: bool, 是否遍历子文件夹, 可选，默认False。
      
      返回：
        Generator[str, None, None]: 返回字符串生成器，其元素为文件路径。
      
    """
    for f in os.scandir(data_dir):
        if f.is_file() and f.name.endswith(tuple(file_types)) and (
            f.name not in exclude_files):
            yield f.path
        elif f.is_dir() and recursive:
            yield from scan_file_paths(f.path,file_types,exclude_files,recursive)



def extract_file_names(
    file_paths: Iterable[str],
    identify_extension: bool = False,
    replace_dot: str = '_', 
)-> Generator[Tuple[str,str],None, None]:
    """批量提取文件路径中的文件名

    参数:
        file_paths: Iterable[str], 文件路径的可迭代对象。
        identify_extension: bool, 是否文件名中区分扩展名(末尾以下划线隔开)，可选，默认False。
        replace_dot: str, 替换扩展名中的点字符，可选，默认为下划线。

    返回:
        Generator[Tuple[str,str],None, None]: 二元元组生成器，包括文件名和文件路径。
    """
    for file_path in file_paths:
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        if identify_extension:
            file_name = file_name + file_extension.replace('.',replace_dot)
        yield file_name, file_path
        

def read_data(
    data: Iterable[Tuple[str,str]],
    usecols: Dict[str, List[str]]= defaultdict(),
    dtypes: Union[Type, Dict[str, Union[Dict[str, Type], Type]]] = defaultdict(),
    chunksize: Union[int, None] = None
)->Generator[Tuple[str,pd.DataFrame], None, None]:
    """根据文件类型批量读取数据文件为数据框

    参数:
        data: Iterable[Tuple[str,str]], 包含数据文件名及其路径的元组可迭代对象。
        usecols: Union[Dict[str, List[str]], None], 指定数据框的列, 字典键为数据文件名, 可选, 默认为None。
        dtypes: Union[Dict[str, Dict[str, Type]],Type, None], 指定数据框的数据类型, 可选, 默认为None。
        chunksize: Union[int, None], 指定数据框分块大小，可选, 默认为None。

    返回:
        Generator[Tuple[str,pd.DataFrame], None, None]: 包含数据框名和数据框的元组生成器。
    """
    # 设定支持的数据读取函数
    reader = {
        '.csv': pd.read_csv,
        '.xls': pd.read_excel,
        '.xlsx': pd.read_excel
    }

        
    for file_name, file_path in data:
        # 提取数据文件的后缀
        ext = os.path.splitext(file_path)[1]
    
        if ext not in reader.keys():
            raise ValueError("Unsupported file type.")
        elif ext in reader.keys() and isinstance(dtypes, Type):
            df = reader[ext](
                file_path,
                usecols=usecols.get(file_name),
                dtype=dtypes,
                chunksize=chunksize)
            yield file_name, df
            
        elif ext in reader.keys() and isinstance(dtypes, dict):
            df = reader[ext](
                file_path,
                usecols=usecols.get(file_name),
                dtype=dtypes.get(file_name),
                chunksize=chunksize)
            yield file_name, df

# def reshape_dfs():
    





# 测试代码
if __name__ == "__main__":
    # 生成一个包含数据文件名及其路径的元组可迭代对象
    my_dir = "/mnt/Data/data/CFPS/data/raw/csv/data" # 修改为你自己的文件夹路径
    my_paths = scan_data_dir(my_dir)
    my_data = extract_file_names(my_paths)
    my_dfs = read_data(my_data,dtypes=str)
    # 读取数据
    for df_name, df in my_dfs:
        print(df_name)
        print(df.head(3))



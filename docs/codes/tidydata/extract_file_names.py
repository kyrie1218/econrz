from typing import Iterable, List, Tuple, Union, Generator
import os

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
        

# 测试代码
if __name__ == "__main__":
    my_paths = [
        '/mnt/Data/data/CFPS/data/raw/csv/data/child2011.csv',
        '/mnt/Data/data/CFPS/data/raw/csv/data/family2011.dta']
    my_names = extract_file_names(my_paths,identify_extension=False)
    my_names_ext = extract_file_names(my_paths,identify_extension=True)
    
    for name, path in my_names:
        print(f"{name} {path}")
    
    for name, path in my_names_ext:
        print(f"{name} {path}")
from typing import List, Generator
import os

def scan_file_paths(
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



# 测试代码
if __name__ == "__main__":
    my_dir = "/mnt/Data/data/CFPS/data/raw/csv" # 修改为你自己的文件夹路径
    my_paths = scan_file_paths(my_dir,recursive=True)
    
    for  path in my_paths:
        print(path)
    
    

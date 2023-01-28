import re
import os
import sqlite3
import functools
import pandas as pd
import numpy as np
from pandas.io.stata import StataReader, StataWriter
from typing import Tuple, List, Generator, Dict, Any, Union, Iterator



class LightDataCleaner(object):
    """
    数据清洗类
    """
    
    def __init__(self):
        """初始化参数和方法
        """

    def scan_csv_path(
        self,
        folder: str,
        extensions: List[str] = ['.csv'],
        exclude: str = "^$",
        recursive: bool = False) -> Generator:
        """生成器函数，用于生成符合指定条件的文件路径。

        Args:
            folder (str): 要扫描的文件夹。
            extensions (List[str]): 要匹配的文件扩展名列表, 默认仅扫描.csv文件。
            exclude (str, optional): 要排除的通配符模式。默认为 "^$"(完全不排除)。
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
                    yield from self.scan_csv_path(entry.path, extensions, exclude, recursive)
    
    def import_csv_to_sqlite(
        self,
        csv_paths_generator: Generator,
        db_file: str = 'data.db',
        csv_chunksize: int = 10000,
        sql_chunksize: int = 5000) -> None:
        """将 CSV 文件导入到 SQLite 数据库。

        参数：
            csv_paths_generator: 生成器，包含 CSV 文件的路径。
            db_file: str，数据库文件的路径。

        返回值：
            None
        """
        # 删除存在的db_file
        self._delete_if_exists(db_file)
        # 连接数据库
        with sqlite3.connect(db_file) as conn:
            # 遍历生成器中的路径
            for csv_path in csv_paths_generator:
                # 获取 CSV 文件的表名
                table_name = self._extract_filename_and_extension(csv_path)[0]
                # 使用 Pandas 读取 CSV 文件
                df_chunks = pd.read_csv(csv_path, chunksize=csv_chunksize, dtype='str')
                for chunk in df_chunks:
                    # 将数据帧写入数据库
                    chunk.to_sql(table_name, conn, chunksize=sql_chunksize, if_exists='append')
            # 提交更改
            conn.commit()
            
            
            
    # 以下是辅助函数
    def _delete_if_exists(
        self,
        filename: str) -> None:
        """如果文件存在，则删除文件。否则，忽略。

        参数:
            filename: str 要删除的文件名
        
        返回值：
        None
        """
        # 检查文件是否存在
        if os.path.exists(filename):
            # 删除文件
            os.remove(filename)    

    def _extract_filename_and_extension(
        self,
        filepath: str) -> Tuple[str, str]:
        """抽取文件路径的纯文件名和后缀。

        参数:
        filepath : str 文件路径。

        返回值:
        Tuple [str, str] 纯文件名和后缀。
        """
        # 获取文件名和后缀
        filename, file_extension = os.path.splitext(filepath)

        # 获取纯文件名（不含后缀）
        pure_filename = os.path.basename(filename)

        return pure_filename, file_extension
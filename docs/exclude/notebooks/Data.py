import re
import os
import sqlite3
import functools
import pandas as pd
import numpy as np
from pandas.io.stata import StataReader, StataWriter

from typing import Tuple, List, Generator, Dict, Any, Union, Iterator


class DataCleaner(object):
    """
    数据清洗器
    """

    def __init__(self):
        """初始化方法

        参数：
        dir: 文件夹所在路径

        返回: None
        """

    def scan_file_path(self,
                       folder: str,
                       extensions: List[str] = ['.csv', '.dta', '.xlsx'],
                       exclude: str = "^$",
                       recursive: bool = False) -> Generator[str, None, None]:
        """生成器函数，用于生成符合指定条件的文件路径。

        Args:
            folder (str): 要扫描的文件夹。
            extensions (List[str]): 要匹配的文件扩展名列表。
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
                    yield from self.scan_file_path(entry.path, extensions, exclude, recursive)

    def read_data(self,
                  file_paths: Generator,
                  chunksize: int = 10000):
        """读取数据

        参数:
            file_paths: Generator 文件路径生成器
            chunksize: int, optional 块大小，默认为 10000

        Yields:
            tuple (文件名, df_chunks)
        """

        for file_path in file_paths:
            # 获取文件名和扩展名
            file_name, file_ext = self._extract_filename_and_extension(
                file_path)

            # 使用字典中的函数来读取文件
            read_func = self._get_read_func(file_ext)
            if read_func is None:
                raise ValueError(f'Unsupported file extension: {file_ext}')
            df_chunks = read_func(file_path, chunksize=chunksize, dtype='str')

            # 遍历 df 块并返回文件名和 df 块
            for df in df_chunks:
                yield file_name, df

    def write_to_sqlite(self,
                        dfs_generator: Generator,
                        db_file: str) -> None:
        """将数据写入 SQLite 数据库。

        参数：
            dfs_generator: 生成器，包含要写入数据库的表名和数据帧。
            db_file: str，数据库文件的路径。

        返回值：
            None
        """
        self._delete_if_exists(db_file)
        # 连接数据库
        with sqlite3.connect(db_file) as conn:
            # 遍历生成器中的内容
            for table_name, df in dfs_generator:
                # 将数据帧写入数据库，追加到现有表中
                df.to_sql(table_name, conn,chunksize=5000, if_exists='append')
            # 提交更改
            conn.commit()

    @functools.lru_cache()
    def _get_read_func(self,
                       file_ext: str):
        """获取文件读取函数

        参数：
            file_ext: str 文件扩展名

        返回值：
            function: 读取文件的函数
        """
        read_funcs = {
            '.csv': pd.read_csv,
            '.dta': self._read_stata,
            '.xlsx': pd.read_excel,
        }

        return read_funcs.get(file_ext)

    def _extract_filename_and_extension(self,
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

    def _read_stata(self,
                    file_path: str,
                    chunksize: int = 10000,
                    keep_data: str = 'all',
                    convert_categoricals: bool = False,
                    preserve_dtypes: bool = False,
                    convert_missing: bool = True,
                    usecols: Union[List[str], None] = None,
                    dtype: Union[List[str], str, None] = None) -> Generator | pd.DataFrame:
        """
        读取 Stata 文件并返回数据和标签。

        参数:
            file_path (str): Stata 文件的路径。
            chunksize (int): 读取stata文件的数据块的大小。
            keep_data (str): 保留数据的类型, 'all'为数据和标签，'only_label'仅标签，
                            'only_data'仅数据，默认为'all'。
            convert_categoricals (bool): 是否转换原始值为值标签对应值，默认值为False。
                            注意，有些文件转换会报错。
            convert_missing (bool): 是否以stata缺失值类型存储，默认值为True。
            usecols (List[str]|None): 保留的列，默认值None保留所有列。
            dtype (List[str]||None): 制定列的数据类型，默认为None。

        返回值:
            Generator: 返回一个(DataFrame)生成器。
        """

        # 创建 StataReader 并设置参数。
        reader = StataReader(
            file_path,
            chunksize=chunksize,
            convert_categoricals=convert_categoricals,
            preserve_dtypes=preserve_dtypes,
            convert_missing=convert_missing,
            columns=usecols)
        # 如果保留标签信息
        if keep_data in ['all', 'only_label']:
            # 获取Stata文件的变量标签dataframe
            variable_labels = self._dict_to_df(
                reader.variable_labels(),
                key_name='_column_name',
                value_name='_column_label').reset_index()
            # 获取Stata文件的值标签dataframe
            value_labels = self._dict_to_df(
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
                copy=False).astype(str)

            if keep_data == "only_label":
                # 仅返回label信息
                return label

            else:
                # 返回包含标签和数据的信息
                for df in reader:
                    labels = pd.concat([label, df], axis=1, join='outer').fillna('')
                    if dtype:
                        yield labels.astype(dtype)
                    else:
                        yield labels
        elif keep_data == "only_data":
            # 仅返回数据数据dataframe块
            for df in reader:
                if dtype:
                    yield df.astype(dtype)
                else:
                    yield df

        else:
            # 返回错误
            raise ValueError(
                f"paramter 'keep_data' got an unexpected value '{keep_data}'")

    def _dict_to_df(self,
                    _dict: Dict[Any, Any],
                    key_name: str,
                    value_name: str) -> pd.DataFrame:
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

    def _get_table_names(self,
                         db_file: str) -> List[str]:
        """获取给定数据库中的表名列表。

        Args:
            db_file: 数据库文件的路径。

        Returns:
            数据库中的表名列表。
        """
        # 获取数据库中的所有表名
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            table_names = [table[0] for table in cursor]

        # 如果给定的表名在列表中，则返回 True，否则返回 False
        return table_names

    def _get_unique_name(self,
                         name: str,
                         name_list: List[str]) -> str:
        """获取唯一的名字。

        如果给定的名字已经在列表中，则提示用户输入新的名字，直到输入的名字在列表中不存在为止。返回不存在于列表中的名字。

        参数:
            name: str 需要检查的名字。
            name_list: List[str] 名字列表。

        返回:
            str: 不存在于列表中的名字。
        """
        new_name = name
        while new_name in name_list:
            new_name = input("请输入一个新的名字: ")
        return new_name

    def _delete_table(self,
                      table_name: str, db_file: str):
        """
        在指定数据库文件中删除指定的表。

        参数:
            table_name: 需要删除的表的名称。
            db_file: 数据库文件的路径。
            
        返回值：
            None
        """
        with sqlite3.connect(db_file) as conn:
            c = conn.cursor()
            c.execute(f"DROP TABLE {table_name}")

    def _name_table(self,
                    name: str,
                    db_file: str,
                    delete_existing_table: bool = False) -> str | None:
        """
        为 SQLite 数据库表命名。如与原表名冲突，则选择要么重命名要么删除原表。

        参数：
        - name (str): 用户定义的名称。
        - db_file (str): SQLite 数据库的文件路径。
        - delete_existing_table (bool): 当表存在时，False（默认）为用户输入新名，True 为删除原表。

        返回值：
        - str | None: 表名或 None。
        """
        # 获取 SQLite 数据库中的全部表名
        table_names = self._get_table_names(db_file)

        # 当命名与已有表名冲突时
        if name in table_names:
            # 删除原表或输入新名字
            return self._delete_table(name, db_file) if delete_existing_table \
                else self._get_unique_name(name, table_names)
        else:
            # 返回原名
            return name



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



    def import_csv_to_sqlite(
        self,
        csv_paths_generator: Generator,
        db_file: str = 'data.db',
        chunksize: int = 5000) -> None:
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
                # 使用 Pandas 读取 CSV 文件
                df = pd.read_csv(csv_path, dtype='str')
                # 获取 CSV 文件的表名
                table_name = self._extract_filename_and_extension(csv_path)[0]
                # 将数据帧写入数据库
                df.to_sql(table_name, conn, chunksize=chunksize, if_exists='append')
            # 提交更改
            conn.commit()

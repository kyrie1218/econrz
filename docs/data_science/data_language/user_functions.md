# Most harmless user function of Python

## 批量横向合并df

```python exec="1" source="tabbed-left"
from typing import List, Union
import pandas as pd
def merge_df(df_left: pd.DataFrame, dfs_right: List[pd.DataFrame], keys: List[str], methods: List[str]) -> pd.DataFrame:
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
df1 = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 6]})
df2 = pd.DataFrame({"B": [1, 2, 9], "C": [10, 11, 12]})
df3 = pd.DataFrame({"C": [10, 3, 15], "D": [16, 17, 18]})


df_left = df1
df_right = [df2, df3]
keys = [("B","B"),("C","C")]
methods = ['inner','outer']

dfs = merge_df(df_left,df_right, keys,methods)

print(f"df1: \n {df1} \n")
print(f"df1: \n {df2} \n")
print(f"df1: \n {df3} \n")
print(f"merged df: \n {dfs} \n")

```

System information:

```python exec="true"
import platform
from textwrap import dedent

print(
    # we must dedent, otherwise Markdown
    # will render it as a code block!
    dedent(
        f"""
        - machine: `{platform.machine()}`
        - version: `{platform.version()}`
        - platform: `{platform.platform()}`
        - system: `{platform.system()}`
        """
    )
)
```

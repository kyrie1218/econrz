# Code cheet

## 根据文件名后缀调用不同的导入方法
```python
# 按照数据文件名的后缀，调用不同的读取方法
import pandas as pd 
def import_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename)
    elif filename.endswith('.dta'):
        return pd.read_stata(filename)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    else:
        raise ValueError('Unsupported file type: 合法的文件类型仅包括csv, dta, xlsx')

path = "/home/kyrie/Documents/project-data_science/cfps_vars.csv"
import_data(path)
```

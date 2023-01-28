# TidyData

???+ abstract
    `TidyData` is a Python class to tidying up raw data for economic research. And it includes the following functions:

    - `scan_file_path` generates a generator of file paths by scanning a directory. 


## Scan_file_path
???+ info 
    `scan_file_paths` inputs a path of directory including raw data. 
=== "Source Codes"
    ```python title="scan_file_paths.py"
    --8<-- "docs/codes/tidydata/scan_file_paths.py"
    ```
=== "Output"
    ```bash
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famecon2010_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/comm2014_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famconf2014_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/adult2010_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/child2011_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/child2012_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famroster2011_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famconf2018_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famconf2010_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/child2010_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famecon2012_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/crossyearid2018_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famconf2016_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famecon2014_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/adult2014_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famconf2012_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/adult2016_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famecon2016_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/childproxy2018_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/child2014_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/comm2010_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/adult2012_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/adult2011_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/person2018_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/famecon2018_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/family2011_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/column_info/child2016_info.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/child2012.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/child2010.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/person2018.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famconf2010.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famconf2012.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famroster2011.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/childproxy2018.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famconf2018.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/adult2010.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/comm2010.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famecon2012.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famecon2018.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/child2014.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famconf2014.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/crossyearid2018.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famconf2016.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/adult2012.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/child2016.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famecon2016.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famecon2014.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/adult2016.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/adult2011.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/comm2014.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/famecon2010.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/adult2014.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/family2011.csv
    /mnt/Data/data/CFPS/data/raw/csv/data/child2011.csv
    ```

## Extract_file_name
???+ info
    `extract_file_names` extracts file names without extensions from a iterable object of file paths.

=== "Source Codes"
    ```python title="extract_file_names.py"
    --8<-- "docs/codes/tidydata/extract_file_names.py"
    ```
=== "Output"
    ```bash
    child2011 /mnt/Data/data/CFPS/data/raw/csv/data/child2011.csv
    family2011 /mnt/Data/data/CFPS/data/raw/csv/data/family2011.dta
    child2011_csv /mnt/Data/data/CFPS/data/raw/csv/data/child2011.csv
    family2011_dta /mnt/Data/data/CFPS/data/raw/csv/data/family2011.dta
    ```







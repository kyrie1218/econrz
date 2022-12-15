# Good Function for Python
## Built-in function
### enumerate()
`enumerate(iterable, start=0)` is a built-in function of Python, which is used to iterate over a list, tuple, or other iterable object and return a tuple containing the index of the element and the element itself. It takes two optional arguments: `iterable`, which is the iterable object to be enumerated, and `start`, which is the index at which to start enumerating the elements. Here is an example of how to use it:

```python exec="1" source="tabbed-left"
# enumerate over a list
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

```

??? "function of `f` in `print()`"
    In Python, the f before the string in a `print()` statement indicates that the string is a formatted string literal. This means that you can include placeholders within the string, surrounded by curly braces `({})`, and then specify the values to be inserted into the placeholders at runtime using the `format()` method. 

```python exec="1" source="tabbed-left"
# enumerate over a tuple, starting at index 1
vegetables = ("carrot", "broccoli", "lettuce")

for i, vegetable in enumerate(vegetables, start=1):
    print(f"{i}: {vegetable}")

```
Also, you can also use the `enumerate()` function to iterate over the elements of a dictionary, by using the `dict.items()` method[^1] to return a list of tuples containing the key-value pairs of the dictionary. For example:

```python exec="1" source="tabbed-left"
# enumerate over a dictionary
prices = {"apple": 1.25, "banana": 0.75, "cherry": 2.50}

for i, (fruit, price) in enumerate(prices.items()):
    print(f"{i}: {fruit} - {price}")

```

As you can see, the `enumerate()` function is a useful tool for iterating over a list or other iterable object and keeping track of the index of each element, and it can be used in a variety of situations where you need to access both the index and the element itself.

## Built-in module: os
### os.scandir()
[`os.scandir()`](https://docs.python.org/zh-cn/3.9/library/os.html) is a function in the `os` module in Python that can be used to get an *iterator containing the entries in a given directory*. It returns an iterator of `os.DirEntry` objects representing each entry in the directory. This function was introduced in Python 3.5 and is intended to replace the older `os.listdir()` function. It is more efficient because it allows the user to access directory entries one at a time, rather than returning a list of all entries in the directory at once.

Here is an example of how `os.scandir()` might be used:

```python exec="1" source="tabbed-left"
import os

# Get an iterator containing the entries in the current directory
with os.scandir(".") as entries:
    for entry in entries:
        # Print the name of each entry
        print(entry.name)
```  
In this code, the `os.scandir()` function is used to get an iterator containing the entries in the current directory. The with statement ensures that the iterator is properly closed and cleaned up when the with block ends. The for loop then iterates over the entries in the directory, allowing the user to perform some action on each entry.

??? note "why uses `with` statement?"
    When using the `os.scandir()` function, it is recommended to use a with statement to ensure that the iterator returned by the function is properly closed and cleaned up. This is because `os.scandir()` opens a directory handle, which is a limited resource, and failing to close the iterator can result in resource leaks.



`os.DirEntry` objects, which are returned by the `os.scandir()` function, have several useful attributes that can provide information about the directory entries they represent. Some of the most commonly used attributes are:

- `name`: The name of the directory entry.
- `path`: The full path to the directory entry.
- `is_dir()`: Returns **True** if the entry is a directory, and **False** otherwise.
- `is_file()`: Returns **True** if the entry is a regular file, and **False** otherwise.
- `is_symlink()`: Returns **True** if the entry is a symbolic link, and **False** otherwise.
- `stat()`: Returns information about the entry, such as its size, permissions, and last modification time.

Here is an example of how these attributes might be used:

```python exec="1" source="tabbed-left"
import os

# Get an iterator containing the entries in the current directory
with os.scandir(".") as entries:
    for entry in entries:
        # Print the name, path, and type of each entry
        print(f"{entry.name} ({entry.path}) - {'directory' if entry.is_dir() else 'file'}")

```
This code will print the name, path, and type (directory or file) of each entry in the current directory. Other attributes of os.DirEntry objects can be accessed in a similar way.


## Built-in module: collections
The `collections` module is a built-in module in Python that provides specialized container datatypes. These datatypes provide alternative ways to store and organize data, and are designed to be more efficient and easier to use than standard Python datatypes.
For more information and examples of how to use the collections module, you can refer to the official Python documentation at https://docs.python.org/3/library/collections.html. Here are some commonly used methods:

### defalutdict()
`collections.defaultdict()` is a function that is part of the `collections` module in Python. It creates a new `defaultdict` object, which is a subclass of the built-in dict class. This means that a `defaultdict` works like a regular dictionary, but it has a default value for keys that don't exist in the dictionary. This default value is specified when the defaultdict is created, and it can be any value, such as an empty list, a zero, or a default factory function. Here is an example of how you might use `collections.defaultdict(list)` to create a dictionary with a default value of an empty list:


```python exec="1" source="tabbed-left"
from collections import defaultdict

# Create a defaultdict with a default value of an empty list
my_dict = defaultdict(list)

# Try to access a key that doesn't exist in the dictionary
print(my_dict["non-existent-key"])  # Output: []

# Add an item to the list at the "non-existent-key"
my_dict["non-existent-key"].append("item1")

# The key now exists in the dictionary and has a value of ["item1"]
print(my_dict["non-existent-key"])  # Output: ["item1"]


```

This example shows how using `defaultdict(list)` allows you to easily add items to a list in a dictionary, even if the key doesn't exist yet in the dictionary. Without using `defaultdict`, you would have to first check if the key exists in the dictionary and then create the key with an empty list as its value before you could add items to the list.

## Popular module: pandas
### pd.merge
`pd.merge` is a function in the Pandas library in Python used for merging dataframes. It can be used to combine data from multiple dataframes based on common columns or keys. This function is similar to SQL's JOIN statement, and can be used to perform various types of inner, outer, and cross joins on dataframes. 

To use the pd.merge function, you need to provide at least two dataframes and specify which columns you want to use to merge the dataframes. For example, you might have a dataframe containing customer data and another dataframe containing purchase data, and you want to combine the data based on the customer's ID. In this case, you would specify the ID column as the key for the merge.

Here is an example of how you might use the pd.merg function to perform an inner join on two dataframes:

```python exec="1" source="tabbed-left"
import pandas as pd

# Create the dataframes
customer_df = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})
purchase_df = pd.DataFrame({'ID': [1, 2, 3], 'Item': ['Book', 'Table', 'Chair']})

# Perform the merge
merged_df = pd.merge(customer_df, purchase_df, on='ID')

# View the resulting dataframe
merged_df

```
As you can see, the pd.merge function has combined the data from the two dataframes based on the common ID column, resulting in a new dataframe that contains the ID, Name, and Item columns.

[^1]: In Python, you also can iterate over a dictionary directly without using the `items()` method. When you do this, the for loop will automatically iterate over the keys of the dictionary. However, we do not recommend this way due to code readablity and easier understanding.


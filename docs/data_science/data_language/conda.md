

# Conda 



![conda](https://raw.githubusercontent.com/kyrie1218/picgo/main/img/202212092055594.png)

[Conda](https://docs.conda.io/en/latest/) is a powerful package and environment management tool designed for [Python](https://www.python.org/). This means it can help users, including economic researchers, organize not only third-party packages like pandas, but also virtual environments with multiple Python compilers. This section will introduce some frequently used commands, covering works:



- Conda information and configuration.

- Package installation, upgrade, and removal;
- Virtual environment creation, activation, change, and removal.



## Conda information and configuration
!!! tip "Basic syntax for conda commands"
    Conda commands have an easy syntax like below.



    ```bash
    conda [DO] [STH] --[OPT]
    ```

    This syntax means if you want conda to do sth with some ways, you must enter commands beginning with `conda`, and with a (maybe optional) specific action like `install` to something like package `pandas`. Also, optional methods like `--help` may be used. 


With basic syntax of conda commands. we turn to specific commands to view information and configuration about Conda.

- `conda --version` displays the version number of conda.

```console exec="1" source="console"
$ conda --version
```

- `conda info --e` checks python virtual environments in Conda. and `conda info` gives more details, e.g. path for configuration file.

``` console exec="1" source="console"
$ conda info --e
```

``` console exec="1" source="console"
$ conda info 
```

- `conda list` lists all installed packages in the current environment.

``` console exec="1" source="console"
$ conda list
```


## Virtual environment management
Conda could create a new virtual environment with a specific version of Python, activate this environment, and remove it.

- `conda create --name python310 python=3.10` creates a new environment named "python310" using Python 3.10 as its compiler.

```bash  
$ conda create --name python310 python=3.10
```

- `conda activate python310` will activate your python virtual environment.

```bash  
$ conda activate python310
```

When you change to a new python environment, you should deactivate current environment using
- `conda deactivate` deactivate conda.

```bash  
$ conda deactivate
```

If you  want to remove this environment, you can use `conda env remove --name python310` in the terminal:

```bash
$ conda env remove --name python310
```



??? note "Conda Conflict"
    Conda environment may be conflicted with arch linux update. Therefore, we strongly recommend you deactivate your conda before you update your system in arch linux.







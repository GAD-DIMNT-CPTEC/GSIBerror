# Instalação

Before using the class, make shure that it is accessible. In general, it can be put in the same directory of your working files.

In the project repository, there is a file called [`environment.yml`](https://github.com/cfbastarz/GSIBerror/blob/main/environment.yml) that can be used to create an Anaconda Python environment with all te libraries and packages needed for the use of the `GSIBerror` class.

To create an Python environment for the use of the `GSIBerror` class, download the last release and issue the following command:

```bash linenums="1"
conda env create -f environment.yml
```

After that, activate the new environment by issuing:

```bash linenums="1"
conda activate GSIBerror
```

The file [`GSIBerror.py`](https://github.com/cfbastarz/GSIBerror/blob/main/GSIBerror.py) must be placed in the same working directory where the Jupyter Notebook will be loaded. It is also possiblem to place the `GSIBerror.py` file elsewhere the user whants, (eg., `/home/user/Downloads/GSIBerror`) and export the variable `PYTHONPATH` pointing to the desired directory (considering the Bash):

```bash linenums="1"
export PYTHONPATH=/home/usuario/Downloads/GSIBerror
```

# Installation

The installation of the `GSIBerror` package, can be made by using `pip`, `conda` or the git repository. In this page, there are presented the those methods so the user can choose what best fit their needs.

## Pip

To install using `pip`, first make sure to have it installed on your computer, then use the command:

```bash linenums="1"
pip install GSIBerror
```

## Conda

To install using `conda`, first make sure to have either Anaconda or Miniconda installed on your computer, then use the command:

```bash linenums="1"
conda install -c conda-forge gsiberror
```

!!! note "Note"

    It is recommended to create a Python environment to use the `GSIBerror` package. A Python environment can be set up by using either `virtualenv` or `conda`.

    With `virtualenv, create an environment for the `GSIBerror` package:

    ```bash linenums="1"
    python -m venv GSIBerror
    source GSIBerror/bin/activate
    pip install GSIBerror
    ```
    
    With `conda`, create an environment for the `GSIBerror` package:

    ```bash linenums="1"
    conda create -n GSIBerror
    conda activate GSIBerror
    conda install -c conda-forge gsiberror
    ```    

## Repository

In the project repository, there is a file called [`environment.yml`](https://github.com/cfbastarz/GSIBerror/blob/main/environment.yml) that can be used to create an Anaconda Python environment with all te libraries and packages needed for the use of the `GSIBerror` package.

To create an Python environment for the use of the `GSIBerror` class, download the last release and issue the following command:

```bash linenums="1"
conda env create -f environment.yml
```

After that, activate the new environment by issuing:

```bash linenums="1"
conda activate GSIBerror
```

!!! note "Note"

    If you want to contribute to the `GSIBerror` development, it is recommended to install the code using the repository method.

With the installation of the `GSIBerror` package done, explore the available notebooks with a demonstration of the package.

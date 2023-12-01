# Installation

The installation of the `GSIBerror` package can be made trough the [PyPi](https://pypi.org/) or the git repository. In this page, there are presented the those methods so the user can choose what best fit their needs.

!!! warning "Warning"

    Before you begin, make sure you have a Python distribution installed in your computer. To make it easier, it is recommended the installation of [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/).

## PyPi

To install the `GSIBerror` release from PyPi, first create a Python virtual environment using `venv` and install the `GSIBerror` package using `pip`:

```bash linenums="1"
python -m venv GSIBerror
source GSIBerror/bin/activate
pip install GSIBerror
```

It is also possible to use `conda` to install the `GSIBerror` package. In the same way demonstrated by using the `venv`, use `conda` to create the virtual environment and install the `GSIBerror` package using `pip`:

## Conda

To install using `conda`, first make sure to have either Anaconda or Miniconda installed on your computer, then use the command:

```bash linenums="1"
conda create -n GSIBerror python=3.8.2
conda activate GSIBerror
pip install GSIBerror
```    

!!! note "Note"

    When you use `conda` to create a Python virtual environment for the `GSIBerror` package, it in necessary to indicate which python version must be installed. It will allow the `GSIBerror` to be used along with its basic dependencies (i.e., `xarray`, `numpy`, `cartopy` e `matplotlib`). When you use `venv`, both `python` and `pip` are automatically installed.

## Repository

In the project repository, there is a file called [`environment.yml`](https://github.com/cfbastarz/GSIBerror/blob/main/environment.yml) that can be used to create an Anaconda Python environment with all te libraries and packages needed for the use of the `GSIBerror` package.

To create an Python environment for the use of the `GSIBerror` package, download the last release and issue the following command:

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

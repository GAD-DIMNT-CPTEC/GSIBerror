# Instalação

A instalação do pacote `GSIBerror` pode ser feita a partir do `pip`, `conda` ou através do próprio repositório. Nesta página, são apresentados estes métodos de instalação e o usuário pode escolher o método que melhor lhe convier.

## Pip

Para instalar utilizando o `pip`, certifique-se de ter o `pip` instalado na sua máquina e utilize o seguinte comando:

```bash linenums="1"
pip install GSIBerror
```

## Conda

Para instalar utilizando o `conda`, certifique-se de ter o Anaconda ou Miniconda instalado na sua máquia e utilize o seguinte comando:

```bash linenums="1"
conda install -c conda-forge gsiberror
```

!!! note "Nota"

    Recomenda-se a criação de um ambiente Python para a utilização do pacote `GSIBerror`. Isso pode ser feito por meio do `virtualenv` ou através do próprio `conda`. 

    Com o `virtualenv`, crie um ambiente para o pacote `GSIBerror`:

    ```bash linenums="1"
    python -m venv GSIBerror
    source GSIBerror/bin/activate
    pip install GSIBerror
    ```

    Com o `conda`, crie um ambiente para o pacote `GSIBerror`:

    ```bash linenums="1"
    conda create -n GSIBerror
    conda activate GSIBerror
    conda install -c conda-forge gsiberror
    ```    

## Repositório

No repositório do projeto, há o arquivo [`environment.yml`](https://github.com/cfbastarz/GSIBerror/blob/main/environment.yml) que pode ser utilizado para criar um ambiente com o pacote `GSIBerror` junto com todas as bibliotecas do Python necessárias para a utilização do pacote.

Para criar o ambiente Python para uso da classe `GSIBerror`, utilizando o `conda`, basta fazer:

```bash linenums="1"
conda env create -f environment.yml
```

Após a criação do ambiente, basta ativá-lo com o comando:

```bash linenums="1"
conda activate GSIBerror
```

!!! note "Nota"

    Quando o usuário desejar contrubuir com o desenvolvimento do pacote `GSIBerror`, recomenda-se a utilização do código do repositório.

Com a instalação do pacote `GSIBerror`, explore os notebooks disponíveis no repositório com exemplos de uso.

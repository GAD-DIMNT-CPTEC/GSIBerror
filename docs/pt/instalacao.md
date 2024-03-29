# Instalação

A instalação do pacote `GSIBerror` pode ser feita a partir `pip` ou através do próprio repositório. Nesta página, são apresentados estes métodos de instalação para que o usuário escolha o método que melhor lhe convier.

!!! warning "Atenção"

    Antes de iniciar a instalação do pacote `GSIBerror`, certifique-se de ter uma distribuição do Python instalada na sua máquina. Para facilitar o processo recomenda-se a instalação do [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/). 


## Pip

Para instalar utilizando a distribuição do pacote `GSIBerror`, crie primeiro um ambiente virtual com o `venv` e instale o pacote utilizando o `pip`:

```bash linenums="1"
python -m venv GSIBerror
source GSIBerror/bin/activate
pip install GSIBerror
```

É possível utilizar também o `conda` para a utilização do pacote `GSIBerror`. Da mesma forma como foi demonstrado com o `venv`, crie um ambiente com o `conda` e instale o pacote `GSIBerror` utilizando o `pip`: 

```bash linenums="1"
conda create -n GSIBerror python=3.9.18
conda activate GSIBerror
pip install GSIBerror
```    

!!! note "Nota"

    Ao criar um ambiente com o `conda`, é necessário indicar a versão do Python a ser utilizada, assim como foi mostrado acima. Isso é necessário para que o pacote `GSIBerror` possa ser utilizado junto com as suas dependências básicas (i.e., `xarray`, `numpy`, `cartopy` e `matplotlib`). Ao criar um ambiente virtual com o `venv`, o `python` e o `pip` são automaticamente instalados.

## Repositório

No repositório do projeto, há o arquivo `environment.yml` que pode ser utilizado para criar um ambiente com o pacote `GSIBerror` junto com todas as bibliotecas do Python necessárias para a sua utilização.

Para criar o ambiente Python para uso do pacote `GSIBerror` utilizando o `conda` e o arquivo `environment.yml`, baixe uma cópia do repositório e execute os comandos:

```bash linenums="1"
gh repo clone GAD-DIMNT-CPTEC/GSIBerror
cd GSIBerror
conda env create -f environment.yml
```

Após a criação do ambiente, basta ativá-lo com o comando:

```bash linenums="1"
conda activate GSIBerror
```

!!! tip "Dica"

    Quando o usuário desejar contrubuir com o desenvolvimento do pacote `GSIBerror`, recomenda-se a utilização do código do repositório.

Com a instalação do pacote `GSIBerror`, explore também os notebooks disponíveis no repositório com exemplos de uso.

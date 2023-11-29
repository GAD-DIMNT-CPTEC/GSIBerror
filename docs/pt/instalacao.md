# Instalação

Antes de utilizar a classe, certifique-se de que ela está acessível. Geralmente, ela pode ser colocada no mesmo diretório em que se está trabalhando.

No repositório do projeto, há o arquivo [`environment.yml`](https://github.com/cfbastarz/GSIBerror/blob/main/environment.yml) que pode ser utilizado para criar um ambiente do Anaconda com todas as bibliotecas do python necessárias para a utilização da classe `GSIBerror`.

Para criar o ambiente Python para uso da classe `GSIBerror`, basta fazer:

```bash linenums="1"
conda env create -f environment.yml
```

Após a criação do ambiente, basta ativá-lo com o comando:

```bash linenums="1"
conda activate GSIBerror
```

O arquivo [`GSIBerror.py`](https://github.com/cfbastarz/GSIBerror/blob/main/GSIBerror.py) deve estar dentro do mesmo diretório onde o Jupyter Notebook será carregado. Pode-se também armazenar o arquivo em algum local de preferência do usuário (eg., `/home/usuario/Downloads/GSIBerror`) e utilizar a variável `PYTHONPATH` apontando para ele (considerando o Bash):

```bash linenums="1"
export PYTHONPATH=/home/usuario/Downloads/GSIBerror
```

# Publicação no PyPI

O workflow `.github/workflows/publish-pypi.yml` publica os pacotes no PyPI
quando uma release estável é publicada no GitHub. Rascunhos e pré-releases
não publicam. A execução manual apenas compila e testa, sem enviar ao PyPI.

## Configuração inicial

Em https://pypi.org/manage/project/gsiberror/settings/publishing/, cadastre
um Trusted Publisher do GitHub:

- Owner: `GAD-DIMNT-CPTEC`
- Repository: `GSIBerror`
- Workflow: `publish-pypi.yml`
- Environment: `pypi`

O environment `pypi` do GitHub identifica o job de publicação. A autenticação
usa OIDC, sem token permanente nos secrets do repositório.

## Nova versão

1. Atualize a versão em `setup.py` e `CITATION.cff`, incluindo a data de lançamento.
2. Envie o código e execute **Actions > Publish to PyPI > Run workflow**.
3. Após a validação, crie uma tag `vX.Y.Z` no commit testado e publique a release
   correspondente no GitHub, documentando as mudanças desde a tag anterior.
4. Aguarde o job `publish` e confirme a disponibilidade da versão no PyPI.

O workflow gera o pacote fonte e um wheel Python independente de plataforma,
construído a partir do pacote fonte. Instala o wheel e executa os testes do
repositório em Python 3.9 e 3.11 antes de publicar. As dependências do pacote,
como Cartopy, continuam sujeitas à disponibilidade para cada plataforma.

Se uma execução falhar, verifique os logs e o estado no PyPI antes de tentar
novamente. Arquivos já publicados não podem ser sobrescritos; não reutilize
uma tag para outro conteúdo após a publicação no PyPI.

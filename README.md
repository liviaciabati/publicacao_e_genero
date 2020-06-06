# Publição e Gênero

Por favor, consulte a nossa publicação no [link]().

Em seguide, explicamos passo-a-passo como realizar a coleta de dados e ánalise.
É importante ressaltar que os dados que colhemos são de domínio público.
Também é preciso saber que atualizações occorem tanto em páginas da USP quanto no Publons, portanto os números no artigo podem diferir.

## Primeio iniciei seu ambiente pip

```
pipenv install
```

```
pipenv shell
```
## (Opcional) Modifique os `paths` no arquivo config.json

```json
{
    "depts":"../depts/",
    "people":"../people/",
    "output":"../output/"
}
```

## Em seguida execute os seguintes `python scripts`

### Para recuperar departamentos da USP

```
 python retrieve_depts.py
```

### Para recuperar pesquisadores por departamento

```
python retrieve_people.py
```

### Obtenha os ids publons

```
python retrieve_publons_info.py
```

### Remova ids publons duplicados, faltantes e verifica nomes que são não similares aos nomes usp

```
python parse_publons_info.py
```

### ATENÇÃO - Passo Manual

É preciso verificar manualmente o arquivo: `publons_info_not_matching.csv` para verificar nomes que diferem entre USP e Publons

### Em seguida, esses ids podem ser removidos (basta adicionar o vetor de números USP selecionados no arquivo)

```
python filter_publons_info.py
```

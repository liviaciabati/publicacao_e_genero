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
    "publons_info":"../publons/info",
    "publons_data":"../publons/data"
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

### Remova ids publons duplicados, faltantes e verifique nomes que não são similares aos nomes usp

```
python parse_publons_info.py
```

### ATENÇÃO - Passo Manual

Abra o arquivo: `publons_info_not_matching.csv` para verificar nomes que diferem entre USP e Publons

### Em seguida, remova esses ids
#### Basta adicionar o vetor de números USP selecionados no script python abaixo

```
python filter_publons_info.py
```

### É necessário agora obter os dados do Publons para cada pesquisador

```
python retrieve publons_data.py
```
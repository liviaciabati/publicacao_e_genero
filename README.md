# Publição e Gênero

Por favor, consulte a nossa publicação no [link]().

Em seguide, explicamos passo-a-passo como realizar a coleta de dados e ánalise.

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
	"people":"../people/"
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
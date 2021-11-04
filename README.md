# Publição e Gênero

Por favor, consulte a nossa publicação em portugues no [link](http://www.rsp.fsp.usp.br/wp-content/plugins/xml-to-html/include/lens/index.php/?xml=1518-8787-rsp-55-46.xml) e em inglês no [link](http://www.rsp.fsp.usp.br/wp-content/plugins/xml-to-html/include/lens/index.php?xml=1518-8787-rsp-55-46.xml&lang=en).

Nós também disponibilizamos o nosso arquivo final processado para análise no seguinte [link]().
Mais a cópia do nosso `jupyter notebook` com a análise final no [link]().

Para outras questões, por favor, contate a pesquisadora principal: liviaciabati@gmail.com

É importante ressaltar que os dados que colhemos são de domínio público.
Também, que atualizações occorem tanto em páginas da Universidade de São Paulo (USP) quanto no Publons, portanto os números no artigo podem diferir um pouco.

Em seguida, explicamos passo-a-passo como realizar a coleta de dados e ánalise.

## Primeio clone nosso repositório do github

```
git clone https://github.com/liviaciabati/publicacao_e_genero.git
```

## Depois da clonagem, iniciei seu ambiente pip dentro do repositório
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
    "resources":"../resources/",
    "publons_info":"../publons/info",
    "publons_data":"../publons/data",
    "publons_results":"../publons/results"
}
```

## Em seguida, entre na seguinte pasta e execute os seguintes `python scripts`

```
cd src
```

### Para recuperar departamentos da USP

```
 python retrieve_depts.py
```

### Para recuperar pesquisadores por departamento

```
python retrieve_people.py
```

### Para obter os ids publons dos pesquisadores

```
python retrieve_publons_info.py
```

### Para remover os ids publons duplicados, faltantes e verificar nomes que são diferentes dos nomes USP

```
python parse_publons_info.py
```

### ATENÇÃO - Passo Manual

Abra o arquivo: `publons_info_not_matching.csv` para verificar nomes que diferem entre USP e Publons

### Em seguida, remova os ids quando constatar que os pesquisadores não são a mesma pessoa
#### Basta adicionar os ids USP selecionados no script python abaixo

```
python filter_publons_info.py
```

### É necessário agora obter os dados do Publons para cada pesquisador
#### Como há um limite de 2000 requisições por dia, limitamos cada execução do script a 2000 ciclos
#### No atual estudo foram necessários 2 dias para recuperar todos os dados

```
python retrieve_publons_data.py
```

#### (OPCIONAL) Se for necesário recuperar dados que falharam, os scripts abaixo podem ser executados

```
python retry_missing_publons.py
python retrieve publons_data.py
```

### Depois de recuperar os dados Publons, eles precisam ser processados

```
python parse_publons_data.py
```

### O próximo passo é identificar o gênero dos pesquisadores
Com base em dados do CENSO de 2010 (https://brasil.io/dataset/genero-nomes/nomes/?=format=csv)
#### Execute o script abaixo
```
python identify_gender.py
```
### ATENÇÃO - Passo Manual
Acesse o portal de transparência da USP

[https://uspdigital.usp.br/portaltransparencia/portaltransparenciaListar](https://uspdigital.usp.br/portaltransparencia/portaltransparenciaListar)

1. Clique em: _Registro atual de todos os docentes / funcionários (arquivo texto)_
2. Preencha o CAPTCHA
3. Clique no ícone, faça o download do arquivo e copie-o para a pasta: `resources`

## Em seguida, execute o script abaixo para adicionar o tempo de trabalho dos professores e também unidade e departamento

```
python identify_time.py
```

## Por fim, criamos um script que remove os números USP e embaralha as linhas para que os resultados sejam compartilhados
Lembrando: todos os dados são públicos e abertos mas, como agregamos informações de diversas bases, optamos por preservar a privacidade dos envolvidos
```
python anonymize.py
```

Com os arquivos de output e o arquivo final: `publons/results/results_publons_gender_time_anonymized.csv`

Siga para a análise em nossos `jupyter notebooks`
```
pipenv run jupyter notebook
```

Execute as células para verificar os resultados.

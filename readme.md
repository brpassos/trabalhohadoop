# Analise de Sentimento com Ecossistema Hadoop

## Escopo

Utilizar o ecossistema hadoop para pegar dados do twitter e fazer a analise de sentimento.

#### Pergunta

Qual o sentimento das pessoas em relação ao Governo Bolsonaro?


## Ambiente

 - [VM Cloudera Quick Start 5.13](https://www.cloudera.com/downloads/quickstart_vms/5-13.html)
 - Recursos Utilizados
    - Flume 
    - Hive
    - Spark
        - python 3.4
        - Bibliotecas Adicionais: unidecode, [TextBlob](https://github.com/sloria/TextBlob/) 
        e [GoogleTranslator](https://github.com/BoseCorp/py-googletrans)
        
    - Power BI
    
[Informações Adicionais](infos_adicionais.md)
    
### Flume

O flume foi utilizado para pegar os dados do twitter e gravar no hdfs. Os tweets foram capturados no dia **20/07(sábado)**.

[flume_twitter_governo_bolsonaro.conf](flume_twitter_governo_bolsonaro.conf)
 
### Hive

Foram criadas duas tabelas para organizar o dados.

[Create_Twitter_Schema.hql](Create_Twitter_Schema.hql)
  
### Spark

No script de analise de sentimento é utilizado a lib TextBlob. Em função desta lib traduzir apenas textos em inglê foi necessário traduzilos de porguês para inglês usando a api de tradução do google.

Através do script [traduzir.py](traduzir.py) os tweets são lidos da tabela trabalho_incremental_tweets, traduzidos e gravados no HDFS para então serem carregados na tabela trabalho_translated_tweets.

O script [analisar-sentimento.py](analisar-sentimento.py) lê da tabela trabalho_translated_tweets, utiliza a biblioteca TextBlob para realizar a analize de sentinmento e grava o resultado em arquivos csv.
    
## Resultado

**Gráficos usando o PowerBI**

[retorno.csv](retorno.csv)

[Gráfico 1](https://app.powerbi.com/view?r=eyJrIjoiZGZlNmExZWItNjBhMS00MTM4LWIzOTktYzI3MzQxNWI0YmQzIiwidCI6IjczNWQ4NTMwLTNkY2EtNGVmNy1iZTFkLWY1N2I4MGYyNmYzZSJ9)<br>
[Gráfico 2](https://app.powerbi.com/view?r=eyJrIjoiNDI3MmEyNDUtMGI3MC00ZmQwLWI1ZDMtOWM3ZmYzYWY4YWNhIiwidCI6IjczNWQ4NTMwLTNkY2EtNGVmNy1iZTFkLWY1N2I4MGYyNmYzZSJ9)<br>
[Gráfico 3](https://app.powerbi.com/view?r=eyJrIjoiNWI3YmYzNDktYjA0OS00MWQ2LWJlN2UtNDM2NGUyMjdjMDc0IiwidCI6IjczNWQ4NTMwLTNkY2EtNGVmNy1iZTFkLWY1N2I4MGYyNmYzZSJ9)

**Gráficos usando o LibreOffice**

[retorno_gr1](retorno_gr1)
[retorno_gr2](retorno_gr2)

[mskgrafico](mskgrafico)



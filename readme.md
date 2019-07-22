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
        
    - (colocar aqui o software que vai gerar os gráficos)
    
[Informações Adicionais](infos_adicionais.md)
    
### Flume

O flume foi utilizado para pegar os dados do twitter e gravar no hdfs.

[flume_twitter_governo_bolsonaro.conf](flume_twitter_governo_bolsonaro.conf)
 
### Hive

Foi criada uma tabela para organizar o dados.

[Create_Twitter_Schema.hql](Create_Twitter_Schema.hql)
  
### Spark

Executado script python para analise de sentimento. 

[analisar-sentimento.py](analisar-sentimento.py)

    
## Resultado

[retorno.csv](retorno.csv)

[Gráficos](https://app.powerbi.com/view?r=eyJrIjoiZGZlNmExZWItNjBhMS00MTM4LWIzOTktYzI3MzQxNWI0YmQzIiwidCI6IjczNWQ4NTMwLTNkY2EtNGVmNy1iZTFkLWY1N2I4MGYyNmYzZSJ9)

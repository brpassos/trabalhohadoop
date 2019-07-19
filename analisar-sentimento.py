from googletrans import Translator
from textblob import TextBlob
from unidecode import unidecode
import csv
import json

# Note - SparkContext available as sc, HiveContext available as sqlCtx.
from pyspark import SparkContext
from pyspark import HiveContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="AnaliseSentimentosTwitter")
sqlCtx = HiveContext(sc)


tweets = sqlCtx.sql("select text from trabalho_incremental_tweets")

#Contadores
numPos = 0
numNeg = 0
numNul = 0
total = 0
score = 0

tweetTexts = tweets.map(lambda p: "text: " + p.text)

#deve ser substituido pela qtd de tweetTexts. Foi colocado assim apenas para testes.
qtd = 100

for text in tweetTexts.collect():

    # pegando o texto
    textPTBR = unidecode(text)

    # traduzindo
    textEN = Translator().translate(textPTBR)

    # analisando o sentimento
    sentiment = TextBlob(textEN.text)

    # atualizando o score
    score += sentiment.polarity

    #contabilizando
    total += 1
    if sentiment.polarity > 0:
        numPos += 1
    elif sentiment.polarity < 0:
        numNeg += 1
    else:
        numNul += 1

    percent = total * 100 / qtd

    if percent % 5 == 0:
        print(percent, '%')

    #deverá ser removido
    if total == qtd:
        break


# Sentimento geral
mediaPos = round(numPos / total, 2)
mediaNeg = round(numNeg / total, 2)
mediaNul = round(numNul / total, 2)


with open('retorno.csv', 'w') as csvfile:
    fieldnames = ['nm_label', 'nu_resultado']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()

    writer.writerow({'nm_label':'Porcentagem Positiva','nu_resultado':mediaPos})
    writer.writerow({'nm_label':'Porcentagem Negativa','nu_resultado':mediaNeg})
    writer.writerow({'nm_label':'Porcentagem Nula','nu_resultado':mediaNul})
    writer.writerow({'nm_label':'Qtd Positivo','nu_resultado':numPos})
    writer.writerow({'nm_label':'Qtd Negativo','nu_resultado':numNeg})
    writer.writerow({'nm_label':'Qtd Nulo','nu_resultado':numNul})
    writer.writerow({'nm_label':'Qtd Total','nu_resultado':total})
    writer.writerow({'nm_label':'Score','nu_resultado':score})
        



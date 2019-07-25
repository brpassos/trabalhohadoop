from googletrans import Translator
from unidecode import unidecode
import csv
import requests
from urllib.parse import quote

import time
import json
from datetime import datetime

# Note - SparkContext available as sc, HiveContext available as sqlCtx.
from pyspark import SparkContext
from pyspark import HiveContext
from pyspark.streaming import StreamingContext

from pyspark.sql import *

sc = SparkContext(appName="AnaliseSentimentosTwitter")
sqlCtx = HiveContext(sc)

tweets = sqlCtx.sql("select id, text from trabalho_incremental_tweets")
tweetTexts = tweets
#tweetTexts = tweets.map(lambda p: "text: " + p.text)


#coloque um valor caso deseje limitar o número de traduções
qtd = len(tweetTexts.collect())

print("##########################")
print("qtd:", qtd)
print("##########################")

traduzidos=[]

#abre o arquivo com os ids dos tweets já traduzidos
with open('traduzidos.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        traduzidos.append(int(row['id']))
        print(row['id'])


total = 0

dataTranslated = []


for tweet in tweetTexts.collect():

    #verifica se o tweet não foi traduzido
    if not (tweet.id in traduzidos):
                
        total += 1

        print(tweet.id)
        print(total)

        traduzidos.append(tweet.id)

        # pegando o texto
        textPTBR = unidecode(tweet.text)        

        # traduzindo

        #alternativa usando lib não oficial###########################
        #textEN = Translator().translate(textPTBR)
        #dataTranslated.append({'id': tweet.id, 'text': textEN.text})
        ##############################################################

        #usando a api oficial do google para traduzir

        #prepara o texto para ser colocado na url
        textPTBR = quote(textPTBR)

        #substitua os asteristicos pela sua key
        googleKey = "********************************"

        #envia requisicao para api
        response = requests.get('https://translation.googleapis.com/language/translate/v2?q='+textPTBR+'&target=en&source=pt_BR&key='+googleKey)
        
        #converte o json
        datastore = json.loads(response.text)
        
        textEN = datastore["data"]["translations"][0]["translatedText"]     
        
        dataTranslated.append({'id': tweet.id, 'text': textEN})

        if total == qtd:
            break
        


sql = SQLContext(sc)

df = sql.read.json(sc.parallelize(dataTranslated))
#df.show()

#cria um nome único
now = datetime.now()
nameJson = datetime.timestamp(now)

#grava os dados no HDFS
df.write.json("/trabalhopitanga/translated/" + str(nameJson))

#criar uma partição na tablea hive apontando para pasta no HDFS com o nome único
sqlCtx.sql("ALTER TABLE trabalho_translated_tweets ADD PARTITION(json_name='" + str(nameJson) + "') LOCATION '/trabalhopitanga/translated/" + str(nameJson) + "/'")

#atualiza a listagem de tweets traduzidos para pode traduzir de forma incremental
with open('traduzidos.csv', 'w') as csvfile:
    fieldnames = ['id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()

    for tweetId in traduzidos:
        writer.writerow({'id':tweetId})
    



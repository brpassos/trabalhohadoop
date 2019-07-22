from googletrans import Translator
from unidecode import unidecode
import csv

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

#deve ser substituido pela qtd de tweetTexts. Foi colocado assim apenas para testes.
qtd = 100
qtdRows = len(tweetTexts.collect())

print("##########################")
print("qtd:", qtd)
print("##########################")
print("qtd:", qtdRows)
print("##########################")

traduzidos=[]

with open('traduzidos.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        traduzidos.append(int(row['id']))
        print(row['id'])


total = 0

dataTranslated = []

for tweet in tweetTexts.collect():

    time.sleep(2)

    #print(tweet.id)
    

    #deverá ser removido
    if total >= qtd:
        break

    #print(tweet.id in traduzidos)

    if not (tweet.id in traduzidos):

        total += 1

        print(tweet.id)

        traduzidos.append(tweet.id)

        # pegando o texto
        textPTBR = unidecode(tweet.text)

        # traduzindo
        textEN = Translator().translate(textPTBR)

        dataTranslated.append({'id': tweet.id, 'text': textEN.text})

 
    print("=====================================================")

sql = SQLContext(sc)

df = sql.read.json(sc.parallelize(dataTranslated))
df.show()
#df.printSchema()

now = datetime.now()
nameJson = datetime.timestamp(now)
dataJson = json.dumps(dataTranslated)

#with open('translated-' + str(nameJson) + '.json', 'w', encoding='utf-8') as f:
    #json.dump(dataTranslated, f, ensure_ascii=False, indent=4)

df.write.json("/trabalhopitanga/translated/" + str(nameJson))

sqlCtx.sql("ALTER TABLE trabalho_translated_tweets ADD PARTITION(json_name='" + str(nameJson) + "') LOCATION '/trabalhopitanga/translated/" + str(nameJson) + "/'")

with open('traduzidos.csv', 'w') as csvfile:
    fieldnames = ['id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()

    for tweetId in traduzidos:
        writer.writerow({'id':tweetId})
    


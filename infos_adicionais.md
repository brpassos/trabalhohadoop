### Informações Adicionais
    
#### Instalando python3 e pip no cloudera:

    sudo yum install epel-release
    sudo yum --disablerepo="*" --enablerepo="epel" install python34
    curl -O https://bootstrap.pypa.io/get-pip.py
    sudo /usr/bin/python3.4 get-pip.py
    python3 --version

#### Instalando bibliotecas

    sudo pip3 install -U textblob
    sudo python3 -m textblob.download_corpora
    
#### Configurando Spark para usar o python3

    sudo vim /etc/spark/conf.dist/spark-env.sh
    
**Adicionar no final do aquivo:**

    export PYSPARK_PYTHON=/usr/bin/python3
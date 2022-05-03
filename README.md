# PSPD_Final

## Como rodar a primeira parte
Primeiro é necessário instalar o pyspark, para isso podemos utilizar o comando:
```
pip3 install pyspark
```
Após a instalação, utilizaremos no NetCat para podermos utilizar facilmente as sockets.
Para isso, precisamos abrir outros dois terminais (para simular um cluster). Em cada terminal digite o seguinte comando:
```
nc -lk $porta
```
onde deve-se substituir o valor '$porta' pela porta que se deseja utilizar para se comunicar com o servidor.

Após os dois terminais rodando (podem ser em máquinas diferentes), utilize o seguinte comando para iniciar o servidor:
```
python3 projeto.py $host $porta $host2 $porta2
```
onde deve-se substituir o valor '$host' e '$porta' pelo ip/hostname e porta que foram utilizadas ao iniciar o NetCat.

Com isso já é possível realizar o teste do programa, basta escrever qualquer texto nos terminais rodando o NetCat e assim poderemos ver a saida incrementando o numero de palavras a cada escrita.

## Como rodar a segunda parte
Primeiro é necessário fazer o download do spark, para isso use o link de download:
https://spark.apache.org/downloads.html

Também é necessário instalar e configurar o Kafka com os seguintes passos:

Passo 1: Instalação
	Para começar o experimento é necessário a instalação do JAVA versão 8 ou superior que é a versão recomendada pelo próprio Kafka.
	Logo em seguida é necessário o download do Kafka pelo link, após o download utilize os seguintes comandos:
	
	tar -xzf kafka_2.13-3.1.0.tgz 
	cd kafka_2.13-3.1.0
	```
Passo 2: Iniciando o ambiente
	Após isso temos de inicializar o ambiente do Kafka rodando os seguintes comandos em ordem, cada um em um terminal diferente:
```
# Start the ZooKeeper service (terminal 1)
bin/zookeeper-server-start.sh config/zookeeper.properties
# Start the Kafka broker service(terminal 2)
bin/kafka-server-start.sh config/server.properties
```

Depois que todos os serviços forem iniciados com sucesso, você terá um ambiente Kafka básico em execução e pronto para uso.

Passo 3: Criando um tópico
	Kafka é uma plataforma de streaming de eventos distribuída que permite ler, gravar, armazenar e processar eventos (também chamados de registros ou mensagens na documentação) em várias máquinas.
	Exemplos de eventos são transações de pagamento, atualizações de geolocalização de telefones celulares, pedidos de remessa, medições de sensores de dispositivos IoT, etc. Esses eventos são organizados e armazenados em tópicos. Muito simplificadamente, um tópico é semelhante a uma pasta em um sistema de arquivos, e os eventos são os arquivos desta pasta.

Portanto, antes de escrever seus primeiros eventos, você deve criar um tópico. Abra outra sessão de terminal e execute:
```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```
Passo 4: Escrevendo eventos no tópico
Um cliente Kafka se comunica com os brokers Kafka por meio da rede para escrever (ou ler) eventos. Uma vez recebidos, os brokers armazenam os eventos de maneira durável e tolerante a falhas pelo tempo que você precisar, até mesmo para sempre.

Execute o cliente produtor do console com o comando abaixo para gravar alguns eventos em seu tópico. Por padrão, cada linha inserida resultará em um evento separado sendo gravado no tópico.
```
bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
```
Para rodar o programa precisamos de rodar o seguinte comando na pasta do spark:
```
bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 projeto2.py localhost:9092 subscribe quickstart-events
```
onde 'localhost' pode ser substituido por outro host, 'subscribe' que é o tipo do subscribe pode ser 'assign', 'subscribe', ou 'subscribePattern' e 'quickstar-events' pode ser substituido pelo nome do tópico, se necessário podem ser escritos separados por virgula.

Com o programa rodando, podemos testar enviando mensagens a partir do terminal que está rodando o producer.

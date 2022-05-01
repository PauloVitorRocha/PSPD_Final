import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: app.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    #inicia a sessão no spark
    spark = SparkSession\
      .builder\
        .appName("newAPP TESTE")\
        .getOrCreate()

    # cria o dataframe que representará os dados da stream
    lines = spark\
        .readStream\
        .format('socket')\
        .option('host', host)\
        .option('port', port)\
        .load()

    # separa as linhas em palavras
    words = lines.select(
        # explode transforma cada item do array em uma linha
        explode(
            split(lines.value, ' ')
        ).alias('word')
    )
    
    # agrupa as palavras todas na mesma tabela
    wordCounts = words.groupBy('word').count()

    # Start running the query that prints the running counts to the console
    # escreve a resposta em modo de 
    query = wordCounts\
        .writeStream\
        .outputMode('complete')\
        .format('console')\
        .start()

    query.awaitTermination()
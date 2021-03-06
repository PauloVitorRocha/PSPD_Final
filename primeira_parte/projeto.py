#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: app.py <hostname> <port> <hostname2> <port2>", file=sys.stderr)
        sys.exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    host2 = sys.argv[3]
    port2 = int(sys.argv[4])

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

    lines2 = spark\
      .readStream\
      .format('socket')\
      .option('host', host2)\
      .option('port', port2)\
      .load()

    lines = lines.union(lines2)

    # separa as linhas em palavras
    words = lines.select(
        # explode transforma cada item do array em uma linha
        explode(
            split(lines.value, ' ')
        ).alias('word')
    )
    
    # agrupa as palavras todas na mesma tabela
    wordCounts = words.groupBy('word').count()

    # escreve a resposta toda vez que houver mudança na stream
    query = wordCounts\
        .writeStream\
        .outputMode('complete')\
        .option("numRows", 50)\
        .format('console')\
        .start()

    query.awaitTermination()
    

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

"""
 Run the example
    `$ bin/spark-submit projeto2 \
    host1:port1,host2:port2 subscribe topic1,topic2`
"""
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import pyspark.sql.functions as F

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        Usage: structured_kafka_wordcount.py <bootstrap-servers> <subscribe-type> <topics>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]

    spark = SparkSession\
        .builder\
        .appName("StructuredKafkaWordCount")\
        .getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    # Create DataSet representing the stream of input lines from kafka
    lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .load()\
        .selectExpr("CAST(value AS STRING)")

    # Split the lines into words
    words = lines.select(
        # explode turns each item in an array into a separate row
        explode(
            split(lines.value, ' ')
        ).alias('word')
    )

    
    # Generate running word count
    wordCounts = words.groupBy('word').count()
    todasPalavras = words.groupBy().count()
    pPalavra = words.filter(F.col("word").substr(1, 1) == "p").groupBy().count()
    pPalavra = pPalavra.selectExpr("cast (count as string) p")

    sPalavra = words.filter(F.col("word").substr(1, 1) == "s").groupBy().count()
    sPalavra = sPalavra.selectExpr("cast (count as string) s")

    rPalavra = words.filter(F.col("word").substr(1, 1) == "r").groupBy().count()
    rPalavra = rPalavra.selectExpr("cast (count as string) r")


    # Start running the query that prints the running counts to the console
    query = wordCounts\
        .writeStream\
        .outputMode('complete')\
        .format('console')\
        .start()

    query2 = todasPalavras\
        .writeStream\
        .outputMode('complete')\
        .format('console')\
        .start()

    query3 = pPalavra\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    query4 = sPalavra\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    query5 = rPalavra\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    query.awaitTermination()
    query2.awaitTermination()
    query3.awaitTermination()
    query4.awaitTermination()
    query5.awaitTermination()


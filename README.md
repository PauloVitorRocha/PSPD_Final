# PSPD_Final

## Como rodar o programa
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

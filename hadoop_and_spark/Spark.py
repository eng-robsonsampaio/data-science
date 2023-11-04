# PG600205 - Desenvolvimento de Soluções com Hadoop e Spark - Turma 5
# Link do arquivo: https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews
#Larisse Maia Mesquita - larimmesq@gmail.com - P23100362
#Robson dos Santos Sampaio - robsonsampaio90@gmail.com - P23100456
#Ariclecio Cavalcanti - ariclecio.cavalcanti@gmail.com - P23100367
#João Paulo Pinto Beserra - jpaulopbeserra@gmail.com - P23100372

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, concat_ws
import time
from pyspark.sql import SparkSession
from datetime import datetime
import pandas as pd
from pyspark.sql.functions import sum as spark_sum
import os  



# Configurar o Spark com nível de log "ERROR" para reduzir mensagens de log
spark = SparkSession.builder.appName('WordCount').getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print('Spark')
print('Equipe: Ariclecio, João Paulo, Larisse e Robson')
print("-----------------------------------------------------------------------------------------------")

def main():
    spark = SparkSession.builder.appName('WordCount').getOrCreate()

    nome_arquivo = 'arquivo_tratado.csv'
    num_linhas = 'TUDO'
    
    inicio_total = time.time()
    inicio_leitura = time.time()
    
    # Lendo o arquivo CSV
    if num_linhas == 'TUDO':
        df = spark.read.csv(nome_arquivo, header=True, sep=';')
    else:
        df = spark.read.csv(nome_arquivo, header=True, sep=';').limit(num_linhas)
    
    # Concatenando todas as colunas em uma única coluna
    df = df.withColumn('texto', concat_ws(';', *df.columns))
    
    # Dividindo e explodindo a coluna concatenada
    palavras = df.select(explode(split(df['texto'], ';')).alias('palavra'))
    
   # Filtrando as palavras que contêm apenas letras (sem espaços vazios)
    palavras = palavras.filter(palavras.palavra.rlike('^[a-zA-Z]+$'))
    
    fim_leitura = time.time()
    inicio_contagem = time.time()
    
    # Contando a frequência das palavras
    contagem = palavras.groupBy('palavra').count()
        
    # Filtrando as palavras que se repetem
    palavras_repetidas = contagem.filter(contagem['count'] > 1)
    # palavras_repetidas = sorted(palavras_repetidas)
    
    # # Imprimindo a lista de todas as palavras repetidas
    # for i, row in enumerate(palavras_repetidas.collect(), start=1):
    #     print(f'{i}° palavra repetida: {row["palavra"]} - Quantidade de vezes que ela se repete: {row["count"]}')
    

    print("-> Itens solicitados no trabalho: ")
    print(f'1) Quantidade total de palavras: {contagem.groupBy().sum().collect()[0][0]:,}')   
    print(f'2) Quantidade de palavras REPETIDAS: {palavras_repetidas.count():,}')
    print(f'3) Quantidade de palavras DISTINTAS: {contagem.count():,}')
 #-----------------------------------------------------------   
    # Encontrando as palavras que mais se repetem (as 3 maiores contagens)
    # top3_mais_repetidas = contagem.orderBy(contagem['count'].desc()).limit(3).collect()

    palavras_mais_repetidas = palavras_repetidas.orderBy(palavras_repetidas['count'].desc()).limit(3).collect()
    top3_mais_repetidas = [(row['palavra'], row['count']) for row in palavras_mais_repetidas]
    print(f"4) As 3 palavras que mais se repetem são:", top3_mais_repetidas)


    # Encontrando as palavras que menos se repetem (as 3 menores contagens)
    palavras_menos_repetidas = palavras_repetidas.orderBy(palavras_repetidas['count'].asc()).limit(3).collect()
    top3_menos_repetidas = [(row['palavra'], row['count']) for row in palavras_menos_repetidas]
    print(f"5) As 3 palavras que menos se repetem são:", top3_menos_repetidas)

    # top3_menos_repetidas = palavras_repetidas.orderBy(palavras_repetidas['count'].asc()).limit(3).collect()
    
#-----------------------------------------------------------
    # Encontrando a palavra que mais se repete e a quantidade
    # palavra_mais_repetida_row = palavras_repetidas.orderBy(palavras_repetidas['count'].desc()).first()
    # print(f'6)A palavra que mais se repete é: {palavra_mais_repetida_row["palavra"]} - Quantidade de vezes que ela se repete: {palavra_mais_repetida_row["count"]:,}')
    palavra_mais_repetida = palavras_repetidas.orderBy(palavras_repetidas['count'].desc()).limit(1).collect()
    top1_mais_repetida = [(row['palavra'], row['count']) for row in palavra_mais_repetida]
    print(f"6) A palavra que mais se repete é:", top1_mais_repetida)

    # # Encontrando a palavra que menos se repete e a quantidade
    # palavra_menos_repetida_row = palavras_repetidas.orderBy(palavras_repetidas['count'].asc()).first()
    # print(f'7) A palavra que menos se repete é: {palavra_menos_repetida_row["palavra"]} - Quantidade de vezes que ela se repete: {palavra_menos_repetida_row["count"]:,}')

    palavra_menos_repetida = palavras_repetidas.orderBy(palavras_repetidas['count'].asc()).limit(1).collect()
    top1_menos_repetida = [(row['palavra'], row['count']) for row in palavra_menos_repetida]
    print(f"7) A palavra que menos se repete é:", top1_menos_repetida)
    
    fim_contagem = time.time()
    fim_total = time.time()

    ############################Contagem dos tempos
    print('8) Duração do processamento:')
    tempo_total_segundos = round(fim_total - inicio_total, 2)
    horas, resto = divmod(tempo_total_segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    print(f'Tempo total: {int(horas)}:{int(minutos)}:{segundos}')

    tempo_leitura_segundos = round(fim_leitura - inicio_leitura, 2)
    horas, resto = divmod(tempo_leitura_segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    print(f'Tempo de leitura: {int(horas)}:{int(minutos)}:{segundos}')

    tempo_contagem_segundos = round(fim_contagem - inicio_contagem, 2)
    horas, resto = divmod(tempo_contagem_segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    print(f'Tempo de cálculo: {int(horas)}:{int(minutos)}:{segundos}')
    print(f'------------------------------------------------------------------------------------------------------------------------------')

    # Complemento para criar e escrever no arquivo CSV

    total_contagens = contagem.agg(spark_sum('count')).collect()[0][0]


    log_df = pd.DataFrame({
        "Nome do programa": ["Spark"],
        "Dia da execução": [datetime.now().strftime('%Y-%m-%d')],
        "Tipo": ["SPARK"],
        "Quantidade total de palavras": [total_contagens],
        "Quantidade de palavras repetidas": [palavras_repetidas.count()],
        "Quantidade de palavras distintas": [contagem.count()],
        "Palavra mais repetida": [top1_mais_repetida[0][0]],
        "Frequência da palavra mais repetida": [top1_mais_repetida[0][1]],
        "Palavra menos repetida": [top1_menos_repetida[0][0]],
        "Frequência da palavra menos repetida": [top1_menos_repetida[0][1]],
        "Tempo do cálculo (HH:MM:SS)": [f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"],
        "Tempo total de execução do programa (HH:MM:SS)": [f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"],
        "3 palavras que mais se repetem são: ": [top3_mais_repetidas],
        "3 palavras que menos se repetem são: ": [top3_menos_repetidas] 
    })

    # Verifica se o arquivo 'log.csv' já existe
    if os.path.isfile('log.csv'):
        # Se existir, anexa as novas linhas ao arquivo existente
        log_df.to_csv('log.csv', mode='a', header=False, sep=';', encoding="utf-8", index=False)
        # spark.stop()
    else:
        # Se não existir, cria um novo arquivo e escreve as linhas
        log_df.to_csv('log.csv', sep=';', encoding="utf-8", index=False)
        print('Arquivo log.csv gerado com sucesso!')
        # spark.stop()

if __name__ == "__main__":
    main()
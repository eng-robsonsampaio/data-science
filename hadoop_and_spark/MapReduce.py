# PG600205 - Desenvolvimento de Soluções com Hadoop e Spark - Turma 5
# Link do arquivo: https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews
#Larisse Maia Mesquita - larimmesq@gmail.com - P23100362
#Robson dos Santos Sampaio - robsonsampaio90@gmail.com - P23100456
#Ariclecio Cavalcanti - ariclecio.cavalcanti@gmail.com - P23100367
#João Paulo Pinto Beserra - jpaulopbeserra@gmail.com - P23100372

print('MapReduce"')
print('Equipe: Ariclecio, João Paulo, Larisse e Robson')
print("-----------------------------------------------------------------------------------------------")
#Importando as Bibliotecas
import time
from collections import Counter
import csv
import os
from datetime import datetime
import pandas as pd

###INÍCIO MAP REDUCE
inicio_total = time.time()

nome_arquivo = 'arquivo_tratado.csv'
num_linhas = 'TUDO'

###INÍCIO TEMPO LEITURA
inicio_leitura = time.time()
print("Iniciando a leitura do arquivo...")
if num_linhas == 'TUDO':
    df = pd.read_csv(nome_arquivo, skiprows=1, header=None, encoding="utf-8", sep=';')
else:
    df = pd.read_csv(nome_arquivo, skiprows=1, header=None, encoding="utf-8", sep=';', nrows=num_linhas)
print("Leitura do arquivo concluída!")
print("Criando a lista de palavras...")
palavras = []
for col in df.columns:
    palavras += df[col].astype(str).str.split(";").explode().tolist()
palavras = [palavra.strip() for palavra in palavras if palavra.strip() != "" and palavra.strip().isalpha() and palavra.strip().lower() != "nan"]
print("Lista de palavras criada!")

###FIM TEMPO LEITURA E CÁLCULO
fim_leitura = time.time()
inicio_calculo = time.time()

#Cálculo frequência das palavras
print("Contando a frequência das palavras...")
contagem = Counter(palavras)


#Cálculo das palavras repetidas
palavras_repetidas = [(palavra, frequencia) for palavra, frequencia in contagem.items() if frequencia > 1 and palavra.strip() != ""]
# print("Imprimindo a lista de todas as palavras repetidas...")
# for i, (palavra, frequencia) in enumerate(palavras_repetidas, start=1):
#     print(f'{i}ª palavra repetida: {palavra} - Quantidade de vezes que se repete: {frequencia}')

print("----------------------------------------------------------------------------------------------------")
print("-> Itens solicitados no trabalho: ")
print(f"1) Quantidade total de palavras: {sum(contagem.values()):,}")
print(f"2) Quantidade de palavras REPETIDAS: {len(palavras_repetidas):,}")
print(f"3) Quantidade de palavras DISTINTAS: {len(contagem):,}")

# Ordena as palavras repetidas em ordem decrescente de frequência e pega as top 3
top3_mais_repetidas = sorted(palavras_repetidas, key=lambda x: x[1], reverse=True)[:3]
print(f"4) As 3 palavras que mais se repetem são: {top3_mais_repetidas}")

# Ordena as palavras repetidas em ordem crescente de frequência e pega as top 3
top3_menos_repetidas = sorted(palavras_repetidas, key=lambda x: x[1])[:3]
print(f"5) As 3 palavras que menos se repetem são: {top3_menos_repetidas}")

palavra_mais_repetida, frequencia_mais_repetida = max(palavras_repetidas, key= lambda x: x[1])
print(f"6) A palavra que mais se repete é: {palavra_mais_repetida} - Quantidade de vezes que ela se repete: {frequencia_mais_repetida}")

palavra_menos_repetida, frequencia_menos_repetida = min(palavras_repetidas, key= lambda x: x[1])
print(f"7) A palavra que menos se repete é: {palavra_menos_repetida} - Quantidade de vezes que ela se repete: {frequencia_menos_repetida}")

###FIM TEMPO CÁLCULO
fim_calculo = time.time()
###FIM MAP REDUCE
fim_total = time.time()

############################Contagem dos tempos
print('8)Duração do processamento:')
#Tempo Total
tempo_total_segundos = round(fim_total - inicio_total, 2)
horas, resto = divmod(tempo_total_segundos, 3600)
minutos, segundos = divmod(resto, 60)
milissegundos = int((tempo_total_segundos - int(tempo_total_segundos)) * 1000)
print(f"Tempo Total: {int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}.{milissegundos:03d}")

#Tempo de leitura
tempo_leitura_segundos = round(fim_leitura - inicio_leitura, 2)
horas_leitura, resto_leitura = divmod(tempo_leitura_segundos, 3600)
minutos_leitura, segundos_leitura = divmod(resto_leitura, 60)
milissegundos_leitura = int((tempo_leitura_segundos - int(tempo_leitura_segundos)) * 1000)
print(f"Tempo de Leitura: {int(horas_leitura):02d}:{int(minutos_leitura):02d}:{int(segundos_leitura):02d}.{milissegundos_leitura:03d}")

#Tempo de cálculo
tempo_calculo_segundos = round(fim_calculo - inicio_calculo, 2)
horas_calculo, resto_calculo = divmod(tempo_calculo_segundos, 3600)
minutos_calculo, segundos_calculo = divmod(resto_calculo, 60)
milissegundos_calculo = int((tempo_calculo_segundos - int(tempo_calculo_segundos)) * 1000)
print(f"Tempo de Cálculo: {int(horas_calculo):02d}:{int(minutos_calculo):02d}:{int(segundos_calculo):02d}.{milissegundos_calculo:03d}")

############# CRIANDO ARQUIVO LOG.CSV
# Escrevendo os tempos no arquivo de log

# Salvando as informações em um arquivo CSV
log_df = pd.DataFrame({
    "Nome do programa": ["MapReduce"],
    "Dia da execução": [datetime.now().strftime('%Y-%m-%d')],
    "Tipo": ["MAPREDUCE"],
    "Quantidade total de palavras": [sum(contagem.values())],
    "Quantidade de palavras repetidas": [len(palavras_repetidas)],
    "Quantidade de palavras distintas": [len(contagem)],
    "Palavra mais repetida": [palavra_mais_repetida],
    "Frequência da palavra mais repetida": [frequencia_mais_repetida],
    "Palavra menos repetida": [palavra_menos_repetida],
    "Frequência da palavra menos repetida": [frequencia_menos_repetida],
    "Tempo do cálculo (HH:MM:SS)": [f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"],
    "Tempo total de execução do programa (HH:MM:SS)": [f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"],
    "3 palavras que mais se repetem são: ": [top3_mais_repetidas],
    "3 palavras que menos se repetem são: ": [top3_menos_repetidas] 
})

# Verifica se o arquivo 'log.csv' já existe
if os.path.isfile('log.csv'):
    # Se existir, anexa as novas linhas ao arquivo existente
    log_df.to_csv('log.csv', mode='a', header=False, sep=';', encoding="utf-8", index=False)
else:
    # Se não existir, cria um novo arquivo e escreve as linhas
    log_df.to_csv('log.csv', sep=';', encoding="utf-8", index=False)
    print('Arquivo log.csv gerado com sucesso!')
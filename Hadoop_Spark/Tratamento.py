# PG600205 - Desenvolvimento de Soluções com Hadoop e Spark - Turma 5
# Link do arquivo: https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews
#Larisse Maia Mesquita - larimmesq@gmail.com - P23100362
#Robson dos Santos Sampaio - robsonsampaio90@gmail.com - P23100456
#Ariclecio Cavalcanti - ariclecio.cavalcanti@gmail.com - P23100367
#João Paulo Pinto Beserra - jpaulopbeserra@gmail.com - P23100372


print('Tratamento da base "Amazon books reviews"')
print('Equipe: Ariclecio, João Paulo, Larisse e Robson')
print("-----------------------------------------------------------------------------------------------")
#Importando as bibliotecas
import pandas as pd
import os
import time

#Nomeando os arquivos
arquivo_original = 'Books_rating.csv'
arquivo_tratado = 'arquivo_tratado.csv'
print("Iniciando o processamento...")

#Cálculo do tempo
tempo_inicial = time.time()
#tentativa de leitura do arquivo original com diferentes codificações
codificacoes = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252', 'windows-1252']
for cod in codificacoes:
    try:
        df = pd.read_csv(arquivo_original, sep=',', dtype=str, encoding=cod)
        print(f"Arquivo lido com sucesso usando a codificação {cod}!")
        break
    except UnicodeDecodeError:
        continue
    

#contagem das linhas do arquivo original
linhas_originais = len(df)
print("Número de linhas do arquivo original: ", linhas_originais)
print("-----------------------------------------------------------------------------------------------")
#Removendo as aspas duplas
print("Removendo as aspas duplas...")
df = df.replace('"','', regex=True)
print("Concluído a remoção das aspas duplas!")
print("-----------------------------------------------------------------------------------------------")
import string
print("Identificando colunas para remoção...")
#Remoção das colunas que contem caracteres de controle
#colunas_para_remover = [col for col in df.columns if not df[col].apply(lambda x: all(char in string.printable for char in str(x))).all()]

#Também remover as colunas de valores numéricos
colunas_para_remover = ['Id', 
                        'User_id', # Removido por conter muitos valores na
                        'profileName', # Removido por conter muitos valores na
                        'Price',
                        'review/helpfulness',
                        'review/score','review/time']
print("Colunas identificadas para remoção: ", colunas_para_remover)
print("-----------------------------------------------------------------------------------------------")
print("Removendo a(s) coluna(s)...")
df.drop(columns=colunas_para_remover, inplace=True)
print("Coluna(s) removida(s)!")

linhas_tratadas = len(df)
print("->Numero de linhas do arquivo original: ", linhas_tratadas)
print("-----------------------------------------------------------------------------------------------")

#Gravação do arquivoo tratado com a mesma codiificação do arquivo original      
print("Gravando o arquivo tratado...")
df.to_csv(arquivo_tratado, sep=";", index=False, header=True, encoding=cod)            
print("Arquivo gravado com sucesso!")
print("-----------------------------------------------------------------------------------------------")
#Fimm da contagem de tempo
tempo_final = time.time()

#Calculo do tamanho dos arquivos
tamanho_original_mb = round(os.path.getsize(arquivo_original) / (1024 * 1024), 2) #tamanho em MB
tamanho_tratado_mb = round(os.path.getsize(arquivo_tratado) / (1024 * 1024), 2) #tamanho em MB

tamanho_original_gb = round(tamanho_original_mb / (1024), 2) #tamanho em GB
tamanho_tratado_gb = round(tamanho_tratado_mb / (1024), 2) #tamanho em GB

reducao_tamanho_mb = round(tamanho_original_mb - tamanho_tratado_mb, 2)
reducao_tamanho_gb = round(tamanho_original_gb - tamanho_tratado_gb, 2)

#calculo do tempo total em horas, minutos e segundos
tempo_total_segundo = tempo_final - tempo_inicial
tempo_total_minuto, tempo_total_segundo = divmod(tempo_total_segundo, 60)
tempo_total_hora, tempo_total_minuto = divmod(tempo_total_minuto, 60)

print(f"->Tamanho do arquivo original: {tamanho_original_mb} MB, ({tamanho_original_gb} GB)")
print(f"->Tamanho do arquivo tratado: {tamanho_tratado_mb} MB, ({tamanho_tratado_gb} GB)")
print(f"->Espaço reduzido: {reducao_tamanho_mb} MB, ({reducao_tamanho_gb} GB)")
print("-----------------------------------------------------------------------------------------------")
print(f"Tempo total para realizar o tratamento: {int(tempo_total_hora)} Horas, {int(tempo_total_minuto)} Minutos e {round(tempo_total_segundo, 2)} Segundos")
print("-----------------------------------------------------------------------------------------------")
print("Processamento concluído!")
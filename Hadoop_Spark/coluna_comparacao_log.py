# PG600205 - Desenvolvimento de Soluções com Hadoop e Spark - Turma 5
# Link do arquivo: https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews
#Larisse Maia Mesquita - larimmesq@gmail.com - P23100362
#Robson dos Santos Sampaio - robsonsampaio90@gmail.com - P23100456
#Ariclecio Cavalcanti - ariclecio.cavalcanti@gmail.com - P23100367
#João Paulo Pinto Beserra - jpaulopbeserra@gmail.com - P23100372

#COMPARAR TEMPOS NO ARQUIVO LOG
import pandas as pd
from datetime import datetime

# Leia o arquivo de log existente
log_df = pd.read_csv('log.csv', sep=';')

# Separe os tempos de execução do MapReduce e do Spark com base no identificador
tempo_execucao_mapreduce = log_df[log_df['Nome do programa'] == 'MapReduce']['Tempo total de execução do programa (HH:MM:SS)'].values[0]
tempo_execucao_spark = log_df[log_df['Nome do programa'] == 'Spark']['Tempo total de execução do programa (HH:MM:SS)'].values[0]

# Converta os tempos de execução para um formato de tempo (datetime)
tempo_execucao_mapreduce = datetime.strptime(tempo_execucao_mapreduce, '%H:%M:%S')
tempo_execucao_spark = datetime.strptime(tempo_execucao_spark, '%H:%M:%S')

# Calcule a diferença de tempo
diferenca_tempo = abs(tempo_execucao_mapreduce - tempo_execucao_spark)

# Calcule a diferença de tempo em horas, minutos e segundos
horas, resto = divmod(diferenca_tempo.total_seconds(), 3600)
minutos, segundos = divmod(resto, 60)

# Formate a diferença de tempo no formato HH:MM:SS
diferenca_tempo_formatada = f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"

# Adicione a coluna de diferença de tempo formatada ao DataFrame do log
log_df['Diferença de tempo (HH:MM:SS)'] = diferenca_tempo_formatada
print("Coluna de comparação adicionada com sucesso!!")
# Salve o DataFrame do log de volta no arquivo log.csv com a nova coluna
log_df.to_csv('log.csv', sep=';', encoding='utf-8', index=False)
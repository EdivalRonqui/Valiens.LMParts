import requests
import json
import pandas as pd
import time
from datetime import datetime, timedelta
import variaveis
from pathlib import Path

def getCentroCustos(conn):

    #### Inicio do processo de coleta de dados ####
    arquivo = 'centrocustos'
    print('-'*50)
    print(f'{'-'*20}[{arquivo}]{'-'*20}')
    # Marcar o início
    inicio = time.time()

    ###### Relação das empresas e suas respectivas chaves ######
    empresas = variaveis.empresas
    ###### Relação das empresas e suas respectivas chaves ######

    # tokens de cada uma das empresas conforme dicionario acima
    tokens = variaveis.tokens

    # define a lista das empresas e dos tokens
    lista_empresas = list(tokens.keys())
    lista_tokens = list(tokens.values())

    # requisicao conforme url abaixo
    def requisicao(token):
        url = "https://services.contaazul.com/finance-pro/v1/cost-centers?search=&page_size=100&page=1"
        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-authorization": token
        }
        response = requests.request("GET", url, headers=headers)
        return response
    
    total_empresas = len(lista_tokens)

    i = 0

    while i < total_empresas: 
        print('-'*50)
        print(f'Total de empresas: {total_empresas}. Empresa atual: {i+1}\n')
        # invoca requisição conforme token
        
        consulta = requisicao(lista_tokens[i])
        consulta.encoding = 'utf-8'
        # convertendo a string JSON para um dicionário
        data = json.loads(consulta.text)
        df = pd.json_normalize(data)
        json_items = df['items'].explode()
        df_final = pd.json_normalize(json_items)
        # insere o id da empresa
        df_final['id_empresa'] = lista_empresas[i]    

        # define pasta onde será salvo
        folder_path = f'c:/_work/valiens/lm parts/{arquivo}/{lista_empresas[i]}'
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        folder_path = f'{folder_path}/centroCusto.csv'
        
        # codifica os textos conforme necessário para aceitar caracteres latino americano
        # df_final.to_csv(folder_path,index=False, encoding='utf-8-sig', sep=';')
        # print(df_final)
        df_final.to_sql(arquivo, conn, if_exists='replace', index=False)

        i += 1

    # Marcar o fim
    fim = time.time()

    # Calcular a diferença
    tempo_execucao = fim - inicio

    # Converter para horas, minutos e segundos
    tempo_formatado = str(timedelta(seconds=tempo_execucao))

    print(f"Tempo de execução da requisição {arquivo} : {tempo_formatado}")
    
# if __name__ == '__main__':
#     main()
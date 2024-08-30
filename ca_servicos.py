import requests
import json
import pandas as pd
import time
import variaveis
from datetime import timedelta
from pathlib import Path

def getServicos(conn):

    arquivo = 'servicos'
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
    lista_nomeEmpresas = list(empresas.values())

    # requisicao conforme url abaixo
    def requisicao(token : str, pagina : int):
        url = f'https://services.contaazul.com/app/service/v2?page={pagina}&pageSize=100'
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
        pg = 0
        print('-'*50)
        print(f'Total de empresas: {total_empresas}. Empresa atual: {i+1}')
        empresa = lista_nomeEmpresas[i]
        # invoca requisição conforme token
        consulta = requisicao(lista_tokens[i], pg)
        # convertendo a string JSON para um dicionário
        data = json.loads(consulta.text)
        # extratindo itens do movimento
        json_data = data['data']
        total_paginas = data['_metadata']['pagination']['totalPages'] - 1
        # dataframe da empresa
        
        while pg <= total_paginas:
            consulta = requisicao(lista_tokens[i], pg)
            # convertendo a string JSON para um dicionário
            data = json.loads(consulta.text)
            # extratindo itens do movimento
            json_data = data['data']
            df = pd.json_normalize(json_data)
            
            # insere o id da empresa
            
            if len(df.columns) == 0:
                None
            else:
                df['id_empresa'] = lista_empresas[i]
                df['pk_produto'] = lista_empresas[i] + '|' + df['id']
                df = df.replace(r'\n', ' ', regex=True)
                expected_columns = [
                'id',
                'serviceId',
                'description',
                'cost',
                'status',
                'serviceType',
                'taxScenarioList',
                'price',
                'id_empresa',
                'pk_produto'
            ]

                # Adicionar colunas que estão faltando
                for column in expected_columns:
                    if column not in df.columns:
                        df[column] = None

                df = df[expected_columns]   
                folder_path = f'{variaveis.path}{arquivo}/{lista_empresas[i]}/'
                Path(folder_path).mkdir(parents=True, exist_ok=True)
                folder_path = f'{folder_path}{pg}.csv'
                # df.to_csv(folder_path, index=False, encoding='utf-8-sig', sep=';',quotechar='"')
                df.to_sql(arquivo, conn, if_exists='append', index=False)
            
            pg += 1

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
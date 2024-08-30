import requests
import json
import pandas as pd
import math
import time
from datetime import timedelta
import variaveis
from pathlib import Path

def getClientes(conn):
    arquivo = 'clientes'
    print('-'*50)
    print(f'{'-'*20}[{arquivo}]{'-'*20}')
    # Marcar o início
    inicio = time.time()
    ###### Relação das empresas e suas respectivas chaves ######
    empresas = variaveis.empresas
    # tokens de cada uma das empresas conforme dicionario acima
    tokens = variaveis.tokens

    # define a lista das empresas e dos tokens
    lista_empresas = list(tokens.keys())
    lista_tokens = list(tokens.values())
    lista_nomeEmpresas = list(empresas.values())

    # requisicao conforme url abaixo
    def requisicao(token,pagina):
        url = "https://services.contaazul.com/contaazul-bff/person-registration/v1/persons"
        querystring = {"search_term":"","page":f"{pagina}","page_size":"100"}  
        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-authorization": token
        }
        response = requests.request("GET", url, headers=headers, params=querystring)  
        return response

    total_empresas = len(lista_tokens)

    i = 0
    pg = 1

    while i < total_empresas: 
        # invoca requisição conforme token
        consulta = requisicao(lista_tokens[i],pg)
        
        # convertendo a string JSON para um dicionário
        data = json.loads(consulta.text)
        
        # extraindo total de páginas
        total_paginas = math.ceil(data['totalItems'] / 100)
        
        while pg <= total_paginas:
            print('-'*50)
            print(f'Total de empresas: {total_empresas}. Empresa atual: {i+1}')
            empresa = lista_nomeEmpresas[i]
            # invoca requisição conforme token
            consulta = requisicao(lista_tokens[i],pg)
            # convertendo a string JSON para um dicionário
            data = json.loads(consulta.text)
            # extratindo itens do movimento
            movimentos = data['items']
            # dataframe da empresa
            df = pd.json_normalize(movimentos)
            # insere o id da empresa
            df['id_empresa'] = lista_empresas[i]


            expected_columns = [
                'uuid',
                'name',
                'document',
                'profiles',
                'personType',
                'active',
                'email',
                'phone',
                'personLegacyId',
                'personLegacyUUID',
                'id_empresa'
            ]

            # Adicionar colunas que estão faltando
            for column in expected_columns:
                if column not in df.columns:
                    df[column] = None

            df = df[expected_columns]
            df['profiles'] = df['profiles'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)

            folder_path = f'c:/_work/valiens/lm parts/{arquivo}/{lista_empresas[i]}'
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            folder_path = f'{folder_path}/clientes{pg}.csv'
            # df.to_csv(folder_path,index=False, encoding='utf-8-sig', sep=';')
            df.to_sql(arquivo, conn, if_exists='append', index=False)

            print(f'Empresa {empresa}\n Total de páginas: {total_paginas}. Página atual: {pg}')
            pg += 1
            # Aguarda 5 segundos
            if total_paginas > 1:
                time.sleep(5)
            else:
                continue
        
        i += 1
        pg = 1

        # Marcar o fim
    fim = time.time()

    # Calcular a diferença
    tempo_execucao = fim - inicio

    # Converter para horas, minutos e segundos
    tempo_formatado = str(timedelta(seconds=tempo_execucao))
    
    print(f"Tempo de execução da requisição {arquivo} : {tempo_formatado}")


# if __name__ == '__main__':
#     main()
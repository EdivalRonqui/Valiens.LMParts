import requests
import json
import pandas as pd
import time
import datetime
import variaveis
from pathlib import Path

def getCategorias(conn):

    #### Inicio do processo de coleta de dados ####
    arquivo = 'categorias'
    print('-'*50)
    print(f'{'-'*20}[{arquivo}]{'-'*20}')
    # Marcar o início
    inicio = time.time()
    # tokens de cada uma das empresas conforme dicionario acima
    tokens = variaveis.tokens

    # define a lista das empresas e dos tokens
    lista_empresas = list(tokens.keys())
    lista_tokens = list(tokens.values())

    # requisicao conforme url abaixo
    def requisicao(token,categoria):
        url = f"https://services.contaazul.com/app/finance/v1/category/activation/{categoria}"
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
    tipoCategoria = ['expenses', 'revenues']

    while i < total_empresas: 
        print('-'*50)
        print(f'Total de empresas: {total_empresas}. Empresa atual: {i+1}\n')
        # invoca requisição conforme token
        
        for tipo in tipoCategoria:
            consulta = requisicao(lista_tokens[i],tipo)
            consulta.encoding = 'utf-8'
            # convertendo a string JSON para um dicionário
            data = json.loads(consulta.text)
            df = pd.json_normalize(data)
            # insere o id da empresa
            df['id_empresa'] = lista_empresas[i]    

            
            # define pasta onde será salvo
            
            folder_path = f'c:/_work/valiens/lm parts/{arquivo}/{lista_empresas[i]}'
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            folder_path = f'{folder_path}/{tipo}.csv'
            
            # Lista de colunas esperadas
            expected_columns = [
                'id', 'uuid', 'code', 'description', 'type', 'level', 'feedDRECost', 'accountancyCodeBlocked',
                'hasBlockedStatements', 'configurable', 'hasPendingConfiguration', 'hasChildren', 'financeAccountId',
                'financeAccountDescription', 'parentLedgerAccountId', 'isReprocessing', 'accountancyCode', 
                'accountancyCodeDescription', 'accountancyRuleDescription', 'originsOfAccountancyEvents', 
                'accountancyAccount', 'id_empresa'
            ]

            # Adicionar colunas que estão faltando
            for column in expected_columns:
                if column not in df.columns:
                    df[column] = None

            df = df[expected_columns]

            # codifica os textos conforme necessário para aceitar caracteres latino americano
            # df.to_csv(folder_path, index=False, encoding='utf-8-sig', sep=';')
            df.to_sql(arquivo, conn, if_exists='append', index=False)

            if tipo == 'expenses':
                df_categorias = df
            else:
                df_categorias = pd.concat([df_categorias,df], ignore_index=True)

            # dataframe final
            if i == 0:
                df_final = df_categorias
            else:
                df_final = pd.concat([df_final, df], ignore_index=True)
        
        i += 1

    # Marcar o fim
    fim = time.time()

    # Calcular a diferença
    tempo_execucao = fim - inicio

    # Converter para horas, minutos e segundos
    tempo_formatado = str(datetime.timedelta(seconds=tempo_execucao))

    print(f"Tempo de execução da requisição {arquivo} : {tempo_formatado}")

# if __name__ == '__main__':
#     main()
import requests
import json
import pandas as pd
import math
import time
import variaveis
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import ast
from pathlib import Path

def getContasPagar(conn):
    #### Inicio do processo de coleta de dados ####
    
    arquivo = 'contaspagar'
    print('-'*50)
    print(f'{'-'*20}[{arquivo}]{'-'*20}')
    
    # Marcar o início
    inicio = time.time()
    
    ###### Relação das empresas e suas respectivas chaves ######
    empresas = variaveis.empresas

    # tokens de cada uma das empresas conforme dicionario acima
    tokens = variaveis.tokens

    # define quantidade de meses que utilizaremos para realizar a consulta incremental
    # meses = int(variaveis.meses_retroativos)

    # define quantidade de anos que utilizaremos para realizar a consulta incremental
    # anos = int(variaveis.anos_consulta)

    # define a lista das empresas e dos tokens
    lista_empresas = list(tokens.keys())
    lista_tokens = list(tokens.values())
    lista_nomeEmpresas = list(empresas.values())

    # requisicao conforme url abaixo
    def requisicao(token,data_inicio,data_fim,pagina):
        url = "https://services.contaazul.com/finance-pro-reader/v1/installment-view"
        querystring = {"page":f"{pagina}","page_size":"100"} 
        payload = {
            "dueDateFrom": data_inicio.strftime('%Y-%m-%d'),
            "dueDateTo": data_fim.strftime('%Y-%m-%d'),
            "quickFilter": "ALL",
            "search": "",
            "type": "EXPENSE"
        }
        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-authorization": token
        }
        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
        return response

    def requisicao_detalhes(token,id):
        url = f"https://services.contaazul.com/contaazul-bff/finance/v1/financial-events/{id}/summary"
        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-authorization": token
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            try:
                json_categorias = json.loads(response.text)['categoriesRatio']
                return json.dumps(json_categorias)
            except Exception:
                None
        else:
            return None
        # return response
    total_empresas = len(lista_tokens)

    # Data atual
    data = datetime.today()

    # define inicio das consultas retrotativas
    data_atual = data + relativedelta( days = -1)
    # data_atual = data_atual.replace(day=1)
    # data_atual = datetime(2024,1,1) #para testes
    
    # define última data a ser consultada
    data_fim = data + relativedelta( days = -1)
    # data_fim = data + relativedelta( years= anos)
    # data_fim = datetime(2024,2,1) #para testes

    # Lista de todas as colunas a serem verificadas
    colunas = [
    'id',
    'acquittanceScheduled',
    'attachment',
    'authorizedBankSlipId',
    'categoryId',
    'chargeRequest',
    'conciliated',
    'description',
    'dueDate',
    'expectedPaymentDate',
    'financialAccount_cashierAccount',
    'financialAccount_contaAzulDigital',
    'financialAccount_id',
    'financialAccount_type',
    'financialEvent_categoryCount',
    'financialEvent_categoryDescriptions',
    'financialEvent_competenceDate',
    'financialEvent_costCenterCount',
    'financialEvent_description',
    'financialEvent_id',
    'financialEvent_negotiator_id',
    'financialEvent_negotiator_name',
    'financialEvent_numberOfInstallments',
    'financialEvent_recurrenceIndex',
    'financialEvent_reference_id',
    'financialEvent_reference_origin',
    'financialEvent_reference_revision',
    'financialEvent_scheduled',
    'financialEvent_type',
    'financialEvent_value',
    'financialEvent_version',
    'fk_categoria',
    'hasDigitalReceipt',
    'id_empresa',
    'index',
    'lastAcquittanceDate',
    'loss',
    'note',
    'paid',
    'paymentRequest',
    'recurrent',
    'reference',
    'status',
    'totalNetValue',
    'unpaid',
    'valueCategory',
    'valueComposition_discount',
    'valueComposition_fee',
    'valueComposition_fine',
    'valueComposition_grossValue',
    'valueComposition_interest',
    'valueComposition_netValue',
    'version',
    'categoryValue',
    'costCenterId',
    'costCenterValue',
    'valor_lancamento',
    'fk_centroCusto'
    ]

    tipos = {
        'conciliated': 'bool',
        'description': 'str',
        'dueDate': 'str',  # pandas não tem tipo 'date' nativo, use 'str' e depois converta
        'expectedPaymentDate': 'str',
        'financialAccount_cashierAccount': 'bool',
        'financialAccount_contaAzulDigital': 'bool',
        'financialAccount_id': 'str',
        'financialAccount_type': 'str',
        'financialEvent_categoryCount': 'int',
        'financialEvent_categoryDescriptions': 'str',
        'financialEvent_competenceDate': 'str',
        'financialEvent_costCenterCount': 'int',
        'financialEvent_description': 'str',
        'financialEvent_id': 'str',
        'financialEvent_negotiator_id': 'str',
        'financialEvent_negotiator_name': 'str',
        'financialEvent_numberOfInstallments': 'int',
        'financialEvent_recurrenceIndex': 'int',
        'financialEvent_reference_id': 'str',
        'financialEvent_reference_origin': 'str',
        'financialEvent_reference_revision': 'int',
        'financialEvent_scheduled': 'bool',
        'financialEvent_type': 'str',
        'financialEvent_value': 'float',
        'financialEvent_version': 'int',
        'fk_categoria': 'str',
        'hasDigitalReceipt': 'bool',
        'id_empresa': 'str',
        'index': 'int',
        'lastAcquittanceDate': 'str',
        'loss': 'str',
        'note': 'str',
        'paid': 'float',
        'paymentRequest': 'str',
        'recurrent': 'bool',
        'reference': 'str',
        'status': 'str',
        'totalNetValue': 'float',
        'unpaid': 'float',
        'valueCategory': 'float',
        'valueComposition_discount': 'float',
        'valueComposition_fee': 'float',
        'valueComposition_fine': 'float',
        'valueComposition_grossValue': 'float',
        'valueComposition_interest': 'float',
        'valueComposition_netValue': 'float',
        'version': 'int',
        'categoryValue' : 'str',
        'costCenterId' : 'str',
        'costCenterValue': 'float',
        'valor_lancamento': 'float',
        'fk_centroCusto' : 'str'
    }

    i = 0
    pg = 1

    while data_atual <= data_fim:
        
        data_inicial = data_atual
        data_final = data_inicial
        # data_final = data_atual.replace(day=calendar.monthrange(data_atual.year, data_atual.month)[1])
        data_final = data_final + timedelta(days=1)
        print(data_atual)
        print(data_final)
        while i < total_empresas: 
            print('-'*50)
            print(f'Total de empresas: {total_empresas}. Empresa atual: {i+1}\n')
            # invoca requisição conforme token
            consulta = requisicao(lista_tokens[i],data_inicial,data_final,pg)
            
            # convertendo a string JSON para um dicionário
            data = json.loads(consulta.text)
            
            # definindo variaveis para criar o nome do arquivo
            ano = data_atual.strftime('%Y')
            mes = data_atual.strftime('%m')
            dia = data_atual.strftime('%d')

            # extraindo total de páginas
            total_paginas = math.ceil(data['totalItems'] / 100)
            
            while pg <= total_paginas:
                print(f'Pagina atual {pg} de {total_paginas}')
                # id_empresa = lista_empresas[i]
                empresa = lista_nomeEmpresas[i]
                # invoca requisição conforme token
                consulta = consulta = requisicao(lista_tokens[i],data_inicial,data_final,pg)
                # convertendo a string JSON para um dicionário
                data = json.loads(consulta.text)
                # extratindo itens do movimento
                movimentos = data['items']
                # dataframe da empresa
                df = pd.json_normalize(movimentos)
                # insere o id da empresa
                df['id_empresa'] = lista_empresas[i]
                
                for index, row in df.iterrows():
                    # faz o script aguardar um segundo para próxima linha
                    time.sleep(1.5)
                    print(row['financialEvent.id'], datetime.now())
                    try:
                        df.at[index, 'retorno'] = requisicao_detalhes(lista_tokens[i], row['financialEvent.id'])
                    except Exception as e:
                        print(f"Erro ao processar o evento financeiro {row['financialEvent.id']}: {e}")
                        continue

                df.reset_index(inplace=True)
                df.rename(columns={'level_0': 'original_index'}, inplace=True)

                # Função corrigida para extrair e expandir os dados da coluna 'categoriesRatio'
                def extract_and_expand(data):
                    extracted_data = []
                    
                    for _, row in data.iterrows():
                        categories_ratio_content = str(row.get('retorno', ''))
                        if pd.notna(categories_ratio_content) and categories_ratio_content != 'nan':
                            try:
                                categories_ratio = ast.literal_eval(categories_ratio_content)
                            except Exception:
                                print("Erro ao avaliar categories_ratio_content: ", categories_ratio_content)
                                continue  # Continua para a próxima iteração do loop se não conseguir avaliar
                            
                            if categories_ratio is not None:  # Adiciona esta linha para verificar se categories_ratio é None
                                for item in categories_ratio:
                                    if 'costCentersRatio' in item and item['costCentersRatio']:
                                        for cost_center in item['costCentersRatio']:
                                            entry = {
                                                'original_index': row['original_index'],
                                                'category': item.get('category', None),
                                                'categoryId': item.get('categoryId', None),
                                                'categoryValue': item.get('value', None),
                                                'costCenterId': cost_center.get('costCenterId', None),
                                                'costCenter': cost_center.get('costCenter', None),
                                                'costCenterValue': cost_center.get('value', None)
                                            }
                                            extracted_data.append(entry)
                                    else:
                                        # Caso não existam costCentersRatio, cria um registro sem eles
                                        entry = {
                                            'original_index': row['original_index'],
                                            'category': item.get('category', None),
                                            'categoryId': item.get('categoryId', None),
                                            'categoryValue': item.get('value', None),
                                            'costCenterId': None,
                                            'costCenter': None,
                                            'costCenterValue': None
                                        }
                                        extracted_data.append(entry)
                    
                    return pd.DataFrame(extracted_data)

                extracted_data = extract_and_expand(df)
                complete_merged_df = pd.merge(df.drop(columns=['retorno']),
                                            extracted_data,
                                            on='original_index',
                                            how='left').drop(columns=['original_index'])

                # cria uma coluna com valor final do lançamento considerando o detalhamento das categorias e dos centros de custos
                complete_merged_df['valor_lancamento'] = complete_merged_df.apply(
                    lambda row: row['costCenterValue'] if pd.notnull(row['costCenterValue']) and row['costCenterValue'] != 0 else row['categoryValue'], 
                    axis=1
                    )

                df_final = complete_merged_df

                # substitui no nome das colunas o "." por "_"
                df_final.rename(columns=lambda x: x.replace('.', '_'), inplace=True)

                # df_final.to_excel('validaColunas.xlsx')

                # cria a chave composta entre empresa e chave da categoria
                df_final['fk_categoria'] = df_final['id_empresa'].astype(str) + '|' + df_final['categoryId'].astype(str)
                df_final['fk_centroCusto'] = df_final['id_empresa'].astype(str) + '|' + df_final['costCenterId'].astype(str)

                # Para adicionar colunas que não existem no DataFrame como nulas
                for coluna in colunas:
                    if coluna not in df_final.columns:
                        df_final[coluna] = None

                # Verifica as colunas do DataFrame que não estão na lista desejada
                colunas_para_remover = [col for col in df_final.columns if col not in colunas]

                # Remove as colunas indesejadas
                df_final = df_final.drop(columns=colunas_para_remover)

                df_final = df_final[colunas]
                df_final.fillna(0, inplace=True)
                df_final = df_final.astype(tipos)

                print(f'{lista_empresas[i]} - Empresa {empresa}\nTotal de páginas: {total_paginas}. Página atual: {pg}\n')
                
                # define pasta onde será salvo
                folder_path = f'c:/_work/valiens/lm parts/{arquivo}/'
                Path(folder_path).mkdir(parents=True, exist_ok=True)
                folder_path = f'{folder_path}{ano}{mes}__pagina_{pg}.csv'
                # df_final.to_csv(folder_path,index=False, encoding='utf-8-sig', sep=';')
                df_final.to_sql(arquivo, conn, if_exists='append', index=False)

                pg += 1
                # Aguarda 5 segundos
                if total_paginas > 1:
                    time.sleep(1.5)
                else:
                    continue
            
            i += 1
            pg = 1
        
        # data_atual = data_inicial + relativedelta(months=1)
        data_atual = data_atual + timedelta(days=1)
        print(data_atual)
        time.sleep(5)
        i = 0
    
    # Marcar o fim
    fim = time.time()
    # Calcula a diferença de tempo
    diferenca_tempo = fim - inicio
   
    tempo_formatado = str(timedelta(seconds=diferenca_tempo))

    print(f"Tempo de execução da requisição {arquivo} : {tempo_formatado}")

# if __name__ == '__main__':
#     main()

import requests
import json
import pandas as pd
import math
import time
import variaveis
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ast

def getVendas(conn):
    #### Inicio do processo de coleta de dados ####
    arquivo = 'vendas'
    print('-'*50)
    print(f'{'-'*20}[{arquivo}]{'-'*20}')
    
    # Marcar o início
    inicio = datetime.now()
    
    ###### Relação das empresas e suas respectivas chaves ######
    empresas = variaveis.empresas
    ###### Relação das empresas e suas respectivas chaves ######

    # tokens de cada uma das empresas conforme dicionario acima
    tokens = variaveis.tokens

    # define quantidade de meses que utilizaremos para realizar a consulta incremental
    meses = int(variaveis.meses_retroativos)

    # define quantidade de anos que utilizaremos para realizar a consulta incremental
    anos = int(variaveis.anos_consulta)

    # define a lista das empresas e dos tokens
    lista_empresas = list(tokens.keys())
    lista_tokens = list(tokens.values())
    lista_nomeEmpresas = list(empresas.values())

    # requisicao conforme url abaixo
    def requisicao(token,data_inicio,data_fim,pagina):
        url = "https://services.contaazul.com/contaazul-bff/sale/v1/sales/searches"
        querystring = {"page":f"{pagina}","page_size":"100"} 
        payload = {
            "totals":"ALL",
            "period":{
                "startDate":data_inicio.strftime('%Y-%m-%d'),
                "endDate":data_fim.strftime('%Y-%m-%d')
            }
        }
        headers = {
                "authority": "services.contaazul.com",
                "accept": "application/json",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://app.contaazul.com",
                "referer": "https://app.contaazul.com/",
                "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "sec-ch-ua-mobile": "?0",
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
        url = f"https://services.contaazul.com/contaazul-bff/sale/v1/sales/{id}"
        headers = {
                "authority": "services.contaazul.com",
                "accept": "application/json",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://app.contaazul.com",
                "referer": "https://app.contaazul.com/",
                "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "x-authorization": token
        }
        response = requests.request("GET", url, headers=headers)
        return response
  
    def requisicao_detalhes_itens(token,id):
        url = f"https://services.contaazul.com/app/v1/negotiations/{id}/items?page=1&page_size=10"
        headers = {
                "authority": "services.contaazul.com",
                "accept": "application/json",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://app.contaazul.com",
                "referer": "https://app.contaazul.com/",
                "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "sec-ch-ua-mobile": "?0",
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
                json_categorias = json.loads(response.text)['data']['items']
                return json_categorias
            except:
                None
        else:
            return None


    # Data atual
    data = datetime.now()

    # define inicio das consultas retrotativas
    data_atual = data #- timedelta( meses * 30)
    data_atual = data_atual.replace(day=1) - relativedelta(months=4)
    # data_atual = datetime(2024,3,1) #para testes
    
    # define última data a ser consultada
    data_fim = data #+ timedelta( meses * 30)
    data_fim = data_fim.replace(day=1)
    # data_fim = datetime(2024,3,1) #para testes

    i = 0
    pg = 1
    total_empresas = len(lista_tokens)

    while data_atual <= data_fim:
        print(f'Data Atual: {data_atual} - Data fim: {data_fim}')
        i = 0
        data_inicial = data_atual
        data_final = data_atual.replace(day=calendar.monthrange(data_atual.year, data_atual.month)[1])

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
            # total_paginas = 1
            while pg <= total_paginas:
                print(f'Pagina atual {pg} de {total_paginas}')
                id_empresa = lista_empresas[i]
                empresa = lista_nomeEmpresas[i]
                # invoca requisição conforme token
                consulta = requisicao(lista_tokens[i],data_inicial,data_final,pg)
                # convertendo a string JSON para um dicionário
                data = json.loads(consulta.text)
                # extratindo itens do movimento
                movimentos = data['items']
                # dataframe da empresa
                df = pd.json_normalize(movimentos)
                # insere o id da empresa
                df['id_empresa'] = lista_empresas[i]

                lista_id = df['id'].tolist()
                total_itens = len(lista_id)
                
                df_detalhes = pd.DataFrame()
                contador = 1
                for venda in lista_id:
                    print(f'{contador} de {total_itens}', data_inicial)
                    # print(venda, data_inicial)
                    
                    
                    max_tentativas = 5
                    tentativa_atual = 0
                    sucesso = False

                    while tentativa_atual < max_tentativas and not sucesso:
                        try:
                            consulta = requisicao_detalhes(lista_tokens[i], venda)
                            
                            # Verifica se o status code é 200 (sucesso)
                            if consulta.status_code == 200:
                                # Convertendo a string JSON para um dicionário
                                data = json.loads(consulta.text)
                                # Extraindo itens do movimento
                                df_temp = pd.json_normalize(data)
                                # Supondo que aqui você faça algo para inserir o id da empresa no df_temp...
                                sucesso = True
                            else:
                                tentativa_atual += 1
                                print(f"Tentativa {tentativa_atual} falhou. Status code: {consulta.status_code}. Tentando novamente...")
                        except Exception as e:
                            tentativa_atual += 1
                            print(f"Erro durante a requisição: {e}. Tentativa {tentativa_atual} de {max_tentativas}.")

                    if not sucesso:
                        print("Falha após várias tentativas de requisição.")
                        print('-'*50)
                    else:
                        print("Requisição bem-sucedida.")
                        print('-'*50)
                    # # insere o id da empresa
                    df_temp['id_empresa'] = lista_empresas[i]
                    # Adiciona os dados do DataFrame temporário ao DataFrame principal
                    df_detalhes = pd.concat([df_detalhes, df_temp], ignore_index=True)
                    time.sleep(1)
                    contador += 1
                    # pg += 1

                if total_itens < 20:
                    time.sleep(5)
                else:
                    time.sleep(20)
                
                contador = 1
                df_detalhes['retorno'] = None 
                print('Iniciando processo de coleta de dados do detalhamento da venda!')
                for index, row in df_detalhes.iterrows():
                    print(f'{contador} de {total_itens}')
                    print(row['id'], data_inicial) 
                    
                    
                    try:
                        print(f'tentativa de requisição linha {index}')
                        print('-'*50)
                        df_detalhes.at[index, 'retorno'] = requisicao_detalhes_itens(lista_tokens[i], row['id'])
                    except Exception as e:
                        print(f"Erro ao fazer a requisição para a linha {index}: {e}")
                        df_detalhes.at[index, 'retorno'] = "Erro na requisição"  # Ou qualquer valor padrão
                    # faz o script aguardar um segundo para próxima linha
                    contador += 1
                    time.sleep(2)

                df_detalhes.reset_index(inplace=True)
                df_detalhes.rename(columns={'index': 'original_index'}, inplace=True)
                
                # Lista para armazenar os dados extraídos
                retorno_detalhado = []

                for index, row in df_detalhes.iterrows():
                    retorno = str(row.get('retorno', ''))
                    if pd.notna(retorno) and retorno != 'nan':
                        try:
                            retorno = ast.literal_eval(retorno)
                        except:
                            print("Erro ao avaliar retorno_content: ", retorno)
                            continue  # Continua para a próxima iteração do loop se não conseguir avaliar
                        
                        if retorno is not None:
                            for item in retorno:
                                entry = {
                                    'original_index': index,  # Capture o índice da linha original
                                    # Adicione as outras informações de interesse
                                    'id': item.get('id', None),
                                    'legacyId': item.get('legacyId', None),
                                    'name': item.get('name', None),
                                    'type': item.get('type', None),
                                    'amount': item.get('amount', None),
                                    'value': item.get('value', None),
                                    'saleItemId': item.get('saleItemId', None),
                                    'saleItemLegacyId': item.get('saleItemLegacyId', None),
                                    'reserved': item.get('reserved', None)
                                }
                                retorno_detalhado.append(entry)

                # Convertendo a lista de dicionários extraídos em um DataFrame
                df_retorno_detalhado = pd.DataFrame(retorno_detalhado)

                df_retorno_detalhado.rename(columns={'id': 'id_produto'}, inplace=True)

                # Resetando o índice do DataFrame original para usar como chave de merge
                df_detalhes_reset_index = df_detalhes.reset_index()

                # Unindo os DataFrames
                merged_df = pd.merge(df_detalhes_reset_index, df_retorno_detalhado, left_on='index', right_on='original_index', how='left')

                colunas_renomear = {col: col.replace('.', '_') for col in merged_df.columns}

                # Renomeia as colunas usando o dicionário de mapeamento
                df_colunas_renomeadas = merged_df.rename(columns=colunas_renomear)

                # df_colunas_renomeadas.to_excel('vendasssss.xlsx')

                colunas_selecionadas = [
                    'id_empresa',
                    'id',
                    'type_x', 
                    'categoryId', 
                    'committedDate',
                    'status',
                    'discountConfiguration_discountType', 
                    'discountConfiguration_discountRate', 
                    'valueComposition_grossValue', 
                    'valueComposition_discount', 
                    'valueComposition_shipping', 
                    'valueComposition_taxes', 
                    'valueComposition_insurance',
                    'valueComposition_netValue',
                    'negotiator_uuid',  
                    'financialEvent_description', 
                    'financialEvent_type',  
                    'amount', 
                    'value',
                    'id_produto',
                    'saleItemId',
                    'saleItemLegacyId'
                ]

                # Seleciona somente as colunas desejadas
                df_selecionado = df_colunas_renomeadas[colunas_selecionadas]

                traducao_colunas = {
                    'type_x': 'tipo',
                    'number': 'numero',
                    'categoryId': 'id_categoria',
                    'committedDate': 'data',
                    'status': 'status',
                    'invoice_status': 'fatura_status',
                    'invoice_alertType': 'fatura_tipo_alerta',
                    'invoice_alertTitle': 'fatura_titulo_alerta',
                    'invoice_alertMessage': 'fatura_mensagem_alerta',
                    'invoice_type': 'fatura_tipo',
                    'discountConfiguration_discountType': 'configuracao_desconto_tipo',
                    'discountConfiguration_discountRate': 'configuracao_desconto_taxa',
                    'valueComposition_grossValue': 'composicao_valor_bruto',
                    'valueComposition_discount': 'composicao_valor_desconto',
                    'valueComposition_shipping': 'composicao_valor_frete',
                    'valueComposition_taxes': 'composicao_valor_impostos',
                    'valueComposition_insurance': 'composicao_valor_seguro',
                    'valueComposition_netValue': 'composicao_valor_liquido',
                    'negotiator_uuid': 'negociador_uuid',
                    'financialEvent_description': 'evento_financeiro_descricao',
                    'financialEvent_type': 'evento_financeiro_tipo',
                    'id_empresa': 'id_empresa',
                    'amount': 'quantidade',
                    'value': 'valor',
                    'saleItemId' : 'id_item_vendido',
                    'saleItemLegacyId' : 'id_item_vendido_legado'
                }

                df_renomeado = df_selecionado.rename(columns=traducao_colunas)
                df_renomeado['venda_id'] = lista_empresas[i]+"|"+df_renomeado['id']
                df_renomeado['fk_categoria'] = lista_empresas[i]+"|"+df_renomeado['id_categoria']
                df_renomeado['fk_cliente'] = lista_empresas[i]+"|"+df_renomeado['negociador_uuid']
                df_renomeado['fk_produto'] = lista_empresas[i]+"|"+df_renomeado['id_produto']

                df_final = df_renomeado
                    
                print(f'{lista_empresas[i]} - Empresa {empresa}\nTotal de páginas: {total_paginas}. Página atual: {pg}\n')
                
                # define pasta onde será salvo
                # folder_path = f'{arquivo}/{lista_empresas[i]}/{ano}{mes}_{id_empresa}_pagina_{pg}.csv'
                # df_final.to_csv(folder_path,index=False, encoding='utf-8-sig', sep=';')
                df_final.to_sql(arquivo, conn, if_exists='append', index=False)

                pg += 1
                # Aguarda 5 segundos
                if total_paginas > 1:
                    time.sleep(1)
                else:
                    continue

            i += 1
            pg = 1
        
        data_atual = data_inicial + relativedelta(months=1)
        print(data_atual)
        time.sleep(1)
    
    # Marcar o fim
    fim = datetime.now()
    # Calcula a diferença de tempo
    diferenca_tempo = fim - inicio

    # Converte a diferença para segundos
    total_segundos = diferenca_tempo.total_seconds()

    # Calcula horas, minutos e segundos
    horas = int(total_segundos // 3600)
    minutos = int((total_segundos % 3600) // 60)
    segundos = int(total_segundos % 60)

    # Formata o tempo para exibição
    tempo_formatado = f"{horas}h {minutos}m {segundos}s"

    print(f"Tempo de execução da requisição {arquivo} : {tempo_formatado}")
    


# if __name__ == '__main__':
#     main()

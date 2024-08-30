import pandas as pd
import variaveis
from pathlib import Path
# import yaml
# from google.cloud import storage

def getEmpresas(conn):

    #### Término das configurações para salvar os dados no GCP ####
    arquivo = 'empresas'
    print('-'*50)
    print(f'{'-'*20}[{arquivo}]{'-'*20}')

    ###### Relação das empresas e suas respectivas chaves ######
    empresas = variaveis.empresas

    df = pd.DataFrame(list(empresas.items()), columns=['id_empresa', 'empresa'])
    df['empresa'] = df['empresa'].str.upper()
    folder_path = f'c:/_work/valiens/lm parts/{arquivo}/'
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    folder_path = f'{folder_path}empresas.csv'

    # codifica os textos conforme necessário para aceitar caracteres latino americano
    # df.to_csv(folder_path,index=False, encoding='utf-8-sig', sep=';')
    df.to_sql(arquivo, conn, if_exists='append', index=False)


# if __name__ == '__main__':
#     main()
import sqlite3
from datetime import datetime, timedelta
from conexao import DatabaseConnections, sqlite_db, DataManager
# import variaveis
import sys
import queries
import logging

# from ca_categorias import getCategorias
# from ca_centroCustos import getCentroCustos
# from ca_clientes import getClientes
# from ca_empresas import getEmpresas
# from ca_servicos import getServicos
# from ca_vendas import getVendas
from ca_contasPagar_cat import getContasPagar
from ca_contasReceber_cat import getContasReceber

logging.basicConfig(
    filename="ImportaDados.log",  
    level=logging.ERROR,  
    format="%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
)

def main():
    db_connections = DatabaseConnections(sqlite_db)
    try:
        sqlite_conn = db_connections.connect_sqlite()
        data_manager = DataManager(sqlite_conn.cursor())
        
        # qry = {
        #     "categorias": [queries.create_Categorias],
        #     "centrocustos": [queries.create_CentroCustos],
        #     "clientes": [queries.create_Clientes],
        #     "contaspagar": [queries.create_ContasPagar],
        #     "contasreceber": [queries.create_ContasReceber],
        #     "empresas": [queries.create_Empresas],
        #     "servicos": [queries.create_Servicos],
        #     "vendas": [queries.create_Vendas]gh
        # }

        # for _, query in qry.items():
            # data_manager.create_table(query[0])
    
        # Processos executados mensalmente
        # getCategorias(sqlite_conn)
        # getCentroCustos(sqlite_conn)
        # getClientes(sqlite_conn)
        # getEmpresas(sqlite_conn)
        # getServicos(sqlite_conn)
        # getVendas(sqlite_conn)
        
        # Processos executados DIARIAMENTE

        if len(sys.argv) > 1: 
            hoje = datetime.strptime(sys.argv[1], "%d-%m-%Y").date()
            data_inicio = hoje
            data_fim = hoje
        else:
            hoje = datetime.today()
            data = datetime.strptime(data_manager.select_data(queries.select_MaxContasPagar).fetchone()[0], "%Y-%m-%d")
            data_inicio = data +  timedelta(days = +1)
            data_fim = datetime(hoje.year, hoje.month, hoje.day) +  timedelta(days = -1)
        
        print('-'*50)
        print(f'data inicio: {data_inicio} | data fim: {data_fim}')
        getContasPagar(sqlite_conn, data_inicio, data_fim)
        
        if len(sys.argv) > 1: 
            hoje = datetime.strptime(sys.argv[1], "%d-%m-%Y").date()
            data_inicio = hoje
            data_fim = hoje
        else:
            hoje = datetime.today()
            data = datetime.strptime(data_manager.select_data(queries.select_MaxContasReceber).fetchone()[0], "%Y-%m-%d")
            data_inicio = data +  timedelta(days = +1)
            data_fim = datetime(hoje.year, hoje.month, hoje.day) +  timedelta(days = -1)

        print('-'*50)
        print(f'data inicio: {data_inicio} | data fim: {data_fim}')
        getContasReceber(sqlite_conn, data_inicio, data_fim)
        print('-'*50)
        
    except sqlite3.Error as e:
        print("Erro ao conectar ou inserir dados no SQLite:", e)
        logging.error(f"Erro ao conectar ou inserir dados no SQLite: {e}", exc_info=True)
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
        logging.error(f"Ocorreu um erro inesperado: {e}", exc_info=True)
    finally:
        db_connections.close_connections()

if __name__ == "__main__":
    main()
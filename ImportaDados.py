import sqlite3
from conexao import DatabaseConnections, sqlite_db #, DataManager
# import queries
# from ca_categorias import getCategorias
# from ca_centroCustos import getCentroCustos
# from ca_clientes import getClientes
from ca_contasPagar_cat import getContasPagar
from ca_contasReceber_cat import getContasReceber
# from ca_empresas import getEmpresas
# from ca_servicos import getServicos
# from ca_vendas import getVendas

def main():

    db_connections = DatabaseConnections(sqlite_db)
    try:
        sqlite_conn = db_connections.connect_sqlite()
        # data_manager = DataManager(sqlite_conn.cursor())
        
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
        #     data_manager.create_table(query[0])
    
        # getCategorias(sqlite_conn)
        # getCentroCustos(sqlite_conn)
        # getClientes(sqlite_conn)
        # getEmpresas(sqlite_conn)
        # getServicos(sqlite_conn)
        # getVendas(sqlite_conn)
        getContasPagar(sqlite_conn)
        getContasReceber(sqlite_conn)
        
    except sqlite3.Error as e:
        print("Erro ao conectar ou inserir dados no SQLite:", e)
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
    finally:
        db_connections.close_connections()

if __name__ == "__main__":
    main()
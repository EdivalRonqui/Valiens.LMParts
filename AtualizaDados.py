import sqlite3
from datetime import datetime
from conexao import DatabaseConnections, sqlite_db
import logging
import wx

from ca_contasPagar_cat import getContasPagar
from ca_contasReceber_cat import getContasReceber

logging.basicConfig(
    filename="AtualizaDados.log",  
    level=logging.ERROR,  
    format="%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    )

def AtualizaContasPagar(data):
    db_connections = DatabaseConnections(sqlite_db)
    try:
        sqlite_conn = db_connections.connect_sqlite()
        
        print('-'*50)
        print(f'Atualizando Contas a Pagar de {data}')
        getContasPagar(sqlite_conn, data, data)
        print('-'*50)
        
    except sqlite3.Error as e:
        print("Erro ao conectar ou inserir dados no SQLite:", e)
        logging.error(f"Erro ao conectar ou inserir dados no SQLite: {e}", exc_info=True)
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
        logging.error(f"Ocorreu um erro inesperado: {e}", exc_info=True)
    finally:
        db_connections.close_connections()
    
def AtualizaContasReceber(data):
    db_connections = DatabaseConnections(sqlite_db)
    try:
        sqlite_conn = db_connections.connect_sqlite()

        print('-'*50)
        print(f'Atualizando Contas a Receber de {data}')
        getContasReceber(sqlite_conn, data, data)
        print('-'*50)
        
    except sqlite3.Error as e:
        print("Erro ao conectar ou inserir dados no SQLite:", e)
        logging.error(f"Erro ao conectar ou inserir dados no SQLite: {e}", exc_info=True)
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
        logging.error(f"Ocorreu um erro inesperado: {e}", exc_info=True)
    finally:
        db_connections.close_connections()
        
class AtualizaDados(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Atualizar dados", size=(600, 400))
        
        painel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(painel, label="Digite uma data (DD/MM/AAAA):")
        sizer.Add(self.label, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        self.entrada_data = wx.TextCtrl(painel)
        sizer.Add(self.entrada_data, flag=wx.ALL | wx.EXPAND, border=10)

        botoes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_Pagar = wx.Button(painel, label="Contas a Pagar")
        btn_Pagar.Bind(wx.EVT_BUTTON, self.validar_data)
        botoes_sizer.Add(btn_Pagar, flag=wx.ALL, border=5)
        
        btn_Receber = wx.Button(painel, label="Contas a Receber")
        btn_Receber.Bind(wx.EVT_BUTTON, self.validar_data)
        botoes_sizer.Add(btn_Receber, flag=wx.ALL, border=5)
        
        btn_sair = wx.Button(painel, label="Sair")
        btn_sair.Bind(wx.EVT_BUTTON, self.sair)
        botoes_sizer.Add(btn_sair, flag=wx.ALL, border=5)

        sizer.Add(botoes_sizer, flag=wx.ALIGN_CENTER)

        painel.SetSizer(sizer)
        self.Centre()
        self.Show()

    def validar_data(self, event):
        data = self.entrada_data.GetValue()
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
            AtualizaContasPagar(data) if event.GetEventObject().GetLabel() == "Contas a Pagar" else AtualizaContasReceber(data) 
        except ValueError:
            wx.MessageBox("Data inválida! Use DD/MM/AAAA.", "Erro", wx.OK | wx.ICON_ERROR)

    def sair(self, event):
        self.Close()



if __name__ == "__main__":
    app = wx.App(False)
    AtualizaDados()
    app.MainLoop()

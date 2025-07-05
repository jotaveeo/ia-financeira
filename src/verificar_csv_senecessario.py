import pandas as pd
from pathlib import Path

def carregar_dados(caminho_arquivo, tipo_banco):
    if tipo_banco == "Nubank":
        data = pd.read_csv(caminho_arquivo)
        colunas_esperadas = {'Data', 'Valor', 'Identificador', 'Descrição'}
        if not colunas_esperadas.issubset(data.columns):
            raise ValueError(f"Colunas esperadas não encontradas no arquivo Nubank: {colunas_esperadas}")
        data['Descrição'] = data['Descrição'].apply(lambda x: x.strip())
    elif tipo_banco == "Banco do Brasil":
        data = pd.read_csv(caminho_arquivo, encoding='latin1', sep=',')
        # Remove espaços e normaliza nomes das colunas
        data.columns = [col.strip().replace('\ufeff', '') for col in data.columns]
        # Renomeia corretamente
        data.rename(columns={
            'Lançamento': 'Descrição',  # Corrigido aqui
            'Valor': 'Valor'
        }, inplace=True)
        if 'Descrição' not in data.columns:
            raise ValueError(f"Coluna 'Lançamento' não encontrada ou não pôde ser renomeada. Colunas atuais: {data.columns}")
        data = data[data['Descrição'].notna() & (data['Descrição'] != "Saldo Anterior") & (data['Descrição'] != "Saldo do dia") & (data['Descrição'] != "S A L D O")]
        data['Descrição'] = data['Descrição'].apply(lambda x: x.strip())
        data['Valor'] = data['Valor'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    else:
        raise ValueError("Tipo de banco não suportado.")
    
    if 'Descrição' not in data.columns or 'Valor' not in data.columns:
        raise ValueError(f"As colunas 'Descrição' e 'Valor' são obrigatórias. Colunas atuais: {data.columns}")
    
    return data

#dados_nubank = carregar_dados('nubank.csv', 'Nubank')
#dados_bb = carregar_dados('bb.csv', 'Banco do Brasil')
#print(dados_nubank.head())
#print(dados_bb.head())

dados_exemplo =  carregar_dados('transacoes_exemplo.csv', 'Nubank')
print(dados_exemplo.head())
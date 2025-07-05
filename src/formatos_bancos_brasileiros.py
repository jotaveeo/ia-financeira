# Formatos de CSV dos principais bancos brasileiros
# Baseado em análise de extratos reais e documentação

FORMATOS_BANCOS = {
    "nubank": {
        "colunas": ["Data", "Valor", "Identificador", "Descrição"],
        "formato_data": "%d/%m/%Y",
        "separador": ",",
        "encoding": "utf-8",
        "exemplo": {
            "Data": "01/05/2025",
            "Valor": "-37.79",
            "Identificador": "68138eea-2dd1-40ae-898f-6ebf077ff936",
            "Descrição": "Compra no débito via NuPay - iFood"
        }
    },
    
    "itau": {
        "colunas": ["data", "lancamento", "valor", "saldo"],
        "formato_data": "%d/%m/%Y",
        "separador": ",",
        "encoding": "latin-1",
        "exemplo": {
            "data": "01/05/2025",
            "lancamento": "COMPRA CARTAO DEBITO - IFOOD",
            "valor": "-37,79",
            "saldo": "1.234,56"
        }
    },
    
    "bradesco": {
        "colunas": ["Data", "Histórico", "Valor", "Saldo"],
        "formato_data": "%d/%m/%Y",
        "separador": ";",
        "encoding": "latin-1",
        "exemplo": {
            "Data": "01/05/2025",
            "Histórico": "COMPRA CARTÃO DÉBITO IFOOD",
            "Valor": "-37,79",
            "Saldo": "1.234,56"
        }
    },
    
    "santander": {
        "colunas": ["Data", "Descrição", "Valor", "Saldo"],
        "formato_data": "%d/%m/%Y",
        "separador": ";",
        "encoding": "latin-1",
        "exemplo": {
            "Data": "01/05/2025",
            "Descrição": "COMPRA DÉBITO - IFOOD",
            "Valor": "-37,79",
            "Saldo": "1234,56"
        }
    },
    
    "caixa": {
        "colunas": ["Data", "Descrição", "Valor", "Saldo"],
        "formato_data": "%d/%m/%Y",
        "separador": ",",
        "encoding": "latin-1",
        "exemplo": {
            "Data": "01/05/2025",
            "Descrição": "COMPRA CARTAO DEBITO IFOOD",
            "Valor": "-37,79",
            "Saldo": "1234,56"
        }
    },
    
    "bb": {  # Banco do Brasil
        "colunas": ["Data", "Lançamento", "Detalhes", "N° documento", "Valor", "Tipo Lançamento"],
        "formato_data": "%d/%m/%Y",
        "separador": ",",
        "encoding": "latin-1",
        "exemplo": {
            "Data": "01/05/2025",
            "Lançamento": "Pix - Enviado",
            "Detalhes": "12/03 21:08 João Vitor Oliveira Teixeira",
            "N° documento": "31201",
            "Valor": "-370,00",
            "Tipo Lançamento": "Saída"
        }
    },
    
    "inter": {
        "colunas": ["Data", "Descrição", "Valor", "Categoria", "Conta"],
        "formato_data": "%Y-%m-%d",
        "separador": ",",
        "encoding": "utf-8",
        "exemplo": {
            "Data": "2025-05-01",
            "Descrição": "Compra no débito - iFood",
            "Valor": "-37.79",
            "Categoria": "Alimentação",
            "Conta": "Conta Corrente"
        }
    },
    
    "c6": {
        "colunas": ["Data", "Categoria", "Título", "Valor"],
        "formato_data": "%d/%m/%Y",
        "separador": ",",
        "encoding": "utf-8",
        "exemplo": {
            "Data": "01/05/2025",
            "Categoria": "Alimentação",
            "Título": "iFood",
            "Valor": "-37,79"
        }
    },
    
    "original": {
        "colunas": ["Data", "Descrição", "Valor", "Saldo", "Categoria"],
        "formato_data": "%d/%m/%Y",
        "separador": ",",
        "encoding": "utf-8",
        "exemplo": {
            "Data": "01/05/2025",
            "Descrição": "COMPRA DÉBITO IFOOD",
            "Valor": "-37,79",
            "Saldo": "1234,56",
            "Categoria": "Alimentação"
        }
    },
    
    "next": {
        "colunas": ["data", "descricao", "valor", "categoria"],
        "formato_data": "%Y-%m-%d",
        "separador": ",",
        "encoding": "utf-8",
        "exemplo": {
            "data": "2025-05-01",
            "descricao": "Compra débito iFood",
            "valor": "-37.79",
            "categoria": "Alimentação"
        }
    }
}

# Mapeamento de colunas para formato padrão
MAPEAMENTO_COLUNAS = {
    # Coluna Data
    "data_aliases": ["Data", "data", "DATE", "Data Movimento", "Data da Transação"],
    
    # Coluna Descrição
    "descricao_aliases": [
        "Descrição", "descricao", "Histórico", "historico", "Lancamento", "lancamento",
        "Título", "titulo", "Descrição da Transação", "Detalhes", "detalhes",
        "Estabelecimento", "estabelecimento", "DESCRIPTION", "description"
    ],
    
    # Coluna Valor
    "valor_aliases": ["Valor", "valor", "VALUE", "Quantia", "quantia", "Montante", "montante"],
    
    # Coluna Saldo (opcional)
    "saldo_aliases": ["Saldo", "saldo", "BALANCE", "Saldo Atual", "saldo_atual"],
    
    # Coluna Categoria (opcional)
    "categoria_aliases": ["Categoria", "categoria", "CATEGORY", "Tipo", "tipo", "Classificação"],
    
    # Coluna Identificador (opcional)
    "id_aliases": ["Identificador", "identificador", "ID", "id", "UUID", "Número do documento"]
}

# Padrões de formato de data comuns
FORMATOS_DATA = [
    "%d/%m/%Y",      # 01/05/2025
    "%Y-%m-%d",      # 2025-05-01
    "%d-%m-%Y",      # 01-05-2025
    "%d.%m.%Y",      # 01.05.2025
    "%Y/%m/%d",      # 2025/05/01
    "%d/%m/%y",      # 01/05/25
    "%y-%m-%d",      # 25-05-01
]

# Padrões de separadores decimais
SEPARADORES_DECIMAIS = {
    "virgula": ",",    # 1.234,56 (Brasil)
    "ponto": "."       # 1,234.56 (EUA)
}

print("Formatos de bancos brasileiros carregados!")
print(f"Total de bancos mapeados: {len(FORMATOS_BANCOS)}")
print(f"Bancos: {', '.join(FORMATOS_BANCOS.keys())}")


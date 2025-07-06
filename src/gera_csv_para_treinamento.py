import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# ============================================================================
# SOLUÇÃO EMERGENCIAL APLICADA - BASEADA NOS DADOS REAIS DO USUÁRIO
# ============================================================================

# Configurações
EXEMPLOS_POR_CATEGORIA = 30  # Mais exemplos para categorias críticas
DATA_INICIO = "01/01/2024"
DATA_FIM = "31/12/2024"

print("🚨 GERADOR DE CSV CORRIGIDO - SOLUÇÃO EMERGENCIAL")
print("Baseado nos dados reais do usuário para resolver problemas de produção")
print("=" * 70)

# ============================================================================
# CATEGORIAS CORRIGIDAS - REMOVENDO PROBLEMÁTICAS
# ============================================================================

# RECEITAS (mantidas)
CATEGORIAS_RECEITAS = [
    "Salário", "Freelance", "Investimentos", "Comissões", 
    "Aluguel Recebido", "Vendas", "13º Salário", "Férias", 
    "Bonificação", "Restituição IR", "Pensão Recebida", "Renda Extra"
]

# DESPESAS - REMOVENDO "Taxas Bancárias" que estava causando 40% dos erros
CATEGORIAS_DESPESAS = [
    # Essenciais
    "Alimentação", "Supermercado", "Transporte", "Combustível",
    "Moradia", "Aluguel", "Energia Elétrica", "Água", "Internet", "Telefone", "Gás",
    
    # Saúde
    "Saúde", "Medicamentos", "Plano de Saúde", "Academia", "Terapia",
    
    # Educação  
    "Educação", "Cursos", "Livros", "Material Escolar",
    
    # Lazer
    "Lazer", "Cinema", "Streaming", "Jogos", "Viagens", "Restaurantes", "Bares",
    
    # Vestuário
    "Roupas", "Sapatos", "Cabeleireiro", "Cosméticos",
    
    # Financeiro (SEM Taxas Bancárias)
    "Cartão de Crédito", "Empréstimos", "Financiamentos", "Seguros",
    
    # Impostos
    "Impostos", "IPTU", "IPVA", "Multas",
    
    # Família
    "Crianças", "Pets", "Presentes",
    
    # Investimentos (como despesa)
    "Poupança", "Previdência",
    
    # Diversos
    "Doações", "Assinaturas", "Outros"
]

# ============================================================================
# EMPRESAS REAIS DO USUÁRIO - BASEADAS NO CSV REAL
# ============================================================================

EMPRESAS_REAIS = {
    "Transporte": [
        # Uber (formato exato do banco)
        "Uber - 17.895.646/0001-87 - EBANX IP LTDA. (0383) Agência: 1 Conta: 1000752180-1",
        "Uber",
        "EBANX IP LTDA",
        "Posto São Cristóvão", 
        "Posto Elo Centro",
        "99", "inDriver"
    ],
    
    "Streaming": [
        # GOGIPSY (formato exato do banco)
        "GOGIPSY E/OU GOGIPSY BRASIL - 37.813.735/0001-44 - MERCADO PAGO IP LTDA. (0323) Agência: 1 Conta: 7996434832-1",
        "GOGIPSY",
        "GOGIPSY BRASIL", 
        "Netflix", "Spotify", "Amazon Prime", "Disney+"
    ],
    
    "Alimentação": [
        "iFood", 
        "GIL DA TAPIOCA", 
        "CAFE PREMIUM", 
        "ESPETINHO MICHEL",
        "TARDELLI RESTAURANTE", 
        "MILK SHAKE MIX ITA", 
        "JAPEDIU DELIVERY - 38.026.413/0001-18 - EFÍ S.A. - IP (0364) Agência: 1 Conta: 296299-3",
        "CafeDoCampus",
        "MP *THEOEVENTOS"
    ],
    
    "Supermercado": [
        "SUPERM SAO LUIZ", 
        "SUPERMERCADO PAULO BEL", 
        "BOM VIZINHO",
        "TAKE A CASE",
        "Carrefour", "Extra"
    ],
    
    "Medicamentos": [
        "PAGUE MENOS 243", 
        "BORALE",
        "Drogasil", "Ultrafarma", "Pacheco"
    ],
    
    "Roupas": [
        "RIACHUELO-FILIAL.108", 
        "FORTALEZA IGUATEMI",
        "Renner", "C&A", "Zara"
    ],
    
    "Energia Elétrica": [
        "NUVEI DO BRASIL INSTITUICAO DE PAGAMENTO LTDA. - 13.492.000/0001-06 - DOCK IP S.A. (0301) Agência: 1 Conta: 4701-7",
        "FRANCISCO SEVERINO CHAVES - 13.682.442/0001-07 - NU PAGAMENTOS - IP (0260) Agência: 1 Conta: 792923040-9",
        "Enel", "Light", "Copel"
    ],
    
    "Freelance": [
        "JOSE TEIXEIRA CORREIA - •••.640.433-•• - BCO BRADESCO S.A. (0237) Agência: 1351 Conta: 672038-2",
        "DIGITAL COLLEGE FORTALEZA LTDA - 43.082.596/0003-90 - ITAÚ UNIBANCO S.A. (0341) Agência: 8142 Conta: 98166-4",
        "FRANCISCA E M P AZEVEDO ME - 20.725.700/0001-50 - CAIXA ECONOMICA FEDERAL (0104) Agência: 748 Conta: 578389441-5",
        "JOAO V O TEIXEIRA CORREIA - •••.593.083-•• - BCO DO BRASIL S.A. (0001) Agência: 374 Conta: 71394-5"
    ]
}

# ============================================================================
# GERADORES ESPECÍFICOS BASEADOS NOS DADOS REAIS
# ============================================================================

def gerar_descricao_transporte():
    """Gera descrições de transporte baseadas nos dados reais"""
    tipo = random.choice(["uber", "posto", "outros"])
    
    if tipo == "uber":
        formatos = [
            "Transferência enviada pelo Pix - Uber - 17.895.646/0001-87 - EBANX IP LTDA. (0383) Agência: 1 Conta: 1000752180-1",
            "Reembolso recebido pelo Pix - Uber - 17.895.646/0001-87 - EBANX IP LTDA. (0383) Agência: 1 Conta: 1000752180-1",
            "Compra no débito via NuPay - Uber",
            "Uber - Corrida",
            "Pagamento Uber via PIX"
        ]
    elif tipo == "posto":
        posto = random.choice(["Posto São Cristóvão", "Posto Elo Centro", "Ipiranga", "Shell"])
        formatos = [
            f"Compra no débito - {posto}",
            f"Pagamento {posto} via PIX",
            f"{posto} - Abastecimento"
        ]
    else:
        empresa = random.choice(["99", "inDriver", "Estacionamento"])
        formatos = [
            f"Compra no débito - {empresa}",
            f"Transferência enviada pelo Pix - {empresa}",
            f"{empresa} - Viagem"
        ]
    
    return random.choice(formatos)

def gerar_descricao_streaming():
    """Gera descrições de streaming baseadas nos dados reais"""
    tipo = random.choice(["gogipsy", "netflix", "outros"])
    
    if tipo == "gogipsy":
        formatos = [
            "Transferência enviada pelo Pix - GOGIPSY E/OU GOGIPSY BRASIL - 37.813.735/0001-44 - MERCADO PAGO IP LTDA. (0323) Agência: 1 Conta: 7996434832-1",
            "Transferência enviada pelo Pix - GOGIPSY BRASIL",
            "Compra no débito - GOGIPSY",
            "GOGIPSY - Assinatura"
        ]
    elif tipo == "netflix":
        formatos = [
            "Netflix - Assinatura mensal",
            "Compra no débito - Netflix",
            "Netflix Premium",
            "Assinatura Netflix"
        ]
    else:
        empresa = random.choice(["Spotify", "Amazon Prime", "Disney+", "YouTube Premium"])
        formatos = [
            f"Assinatura {empresa}",
            f"Compra no débito - {empresa}",
            f"{empresa} - Plano Premium"
        ]
    
    return random.choice(formatos)

def gerar_descricao_alimentacao():
    """Gera descrições de alimentação baseadas nos dados reais"""
    empresa = random.choice(EMPRESAS_REAIS["Alimentação"])
    
    if empresa == "iFood":
        formatos = [
            "Compra no débito via NuPay - iFood",
            "Compra no débito - IFD*IFOOD CLUB",
            "iFood - Pedido",
            "Transferência enviada pelo Pix - iFood"
        ]
    elif "JAPEDIU" in empresa:
        return f"Transferência enviada pelo Pix - {empresa}"
    else:
        formatos = [
            f"Compra no débito - {empresa}",
            f"Transferência enviada pelo Pix - {empresa}",
            f"{empresa} - Refeição"
        ]
    
    return random.choice(formatos)

def gerar_descricao_supermercado():
    """Gera descrições de supermercado baseadas nos dados reais"""
    empresa = random.choice(EMPRESAS_REAIS["Supermercado"])
    
    formatos = [
        f"Compra no débito - {empresa}",
        f"Transferência enviada pelo Pix - {empresa}",
        f"{empresa} - Compras"
    ]
    
    return random.choice(formatos)

def gerar_descricao_medicamentos():
    """Gera descrições de medicamentos baseadas nos dados reais"""
    empresa = random.choice(EMPRESAS_REAIS["Medicamentos"])
    
    formatos = [
        f"Compra no débito - {empresa}",
        f"Transferência enviada pelo Pix - {empresa}",
        f"{empresa} - Medicamentos"
    ]
    
    return random.choice(formatos)

def gerar_descricao_roupas():
    """Gera descrições de roupas baseadas nos dados reais"""
    empresa = random.choice(EMPRESAS_REAIS["Roupas"])
    
    formatos = [
        f"Compra no débito - {empresa}",
        f"Transferência enviada pelo Pix - {empresa}",
        f"{empresa} - Vestuário"
    ]
    
    return random.choice(formatos)

def gerar_descricao_energia():
    """Gera descrições de energia baseadas nos dados reais"""
    if random.random() < 0.3:  # 30% chance de usar formato real
        empresa = random.choice(EMPRESAS_REAIS["Energia Elétrica"])
        return f"Transferência enviada pelo Pix - {empresa}"
    else:
        empresa = random.choice(["Enel", "Light", "Copel", "Cemig"])
        formatos = [
            f"Transferência enviada pelo Pix - {empresa}",
            f"Compra no débito - {empresa}",
            f"{empresa} - Energia elétrica"
        ]
        return random.choice(formatos)

def gerar_descricao_freelance():
    """Gera descrições de freelance baseadas nos dados reais"""
    if random.random() < 0.5:  # 50% chance de usar formato real
        pessoa = random.choice(EMPRESAS_REAIS["Freelance"])
        return f"Transferência recebida pelo Pix - {pessoa}"
    else:
        formatos = [
            "Transferência Recebida - Freelance",
            "PIX Recebido - Trabalho freelance",
            "TED Recebida - Projeto freelance",
            "Depósito - Serviço prestado"
        ]
        return random.choice(formatos)

def gerar_descricao_investimentos():
    """Gera descrições de investimentos baseadas nos dados reais"""
    tipo = random.choice(["aplicacao", "resgate", "outros"])
    
    if tipo == "aplicacao":
        return "Aplicação RDB"
    elif tipo == "resgate":
        return "Resgate RDB"
    else:
        formatos = [
            "Tesouro Direto - Aplicação",
            "CDB - Investimento",
            "Poupança - Depósito",
            "Fundo de investimento"
        ]
        return random.choice(formatos)

# ============================================================================
# CONFIGURAÇÃO DE GERADORES POR CATEGORIA
# ============================================================================

GERADORES_ESPECIFICOS = {
    "Transporte": gerar_descricao_transporte,
    "Streaming": gerar_descricao_streaming,
    "Alimentação": gerar_descricao_alimentacao,
    "Supermercado": gerar_descricao_supermercado,
    "Medicamentos": gerar_descricao_medicamentos,
    "Roupas": gerar_descricao_roupas,
    "Energia Elétrica": gerar_descricao_energia,
    "Freelance": gerar_descricao_freelance,
    "Investimentos": gerar_descricao_investimentos
}

# ============================================================================
# FAIXAS DE VALORES REALISTAS
# ============================================================================

def determinar_faixa_valor(categoria):
    """Faixas baseadas nos dados reais do usuário"""
    faixas = {
        # RECEITAS
        "Salário": (1500, 8000),
        "Freelance": (100, 2000),
        "Investimentos": (50, 3000),
        "13º Salário": (1500, 8000),
        "Aluguel Recebido": (800, 3000),
        "Comissões": (100, 1500),
        "Vendas": (50, 1000),
        "Férias": (1000, 6000),
        "Bonificação": (200, 3000),
        "Restituição IR": (100, 2000),
        "Pensão Recebida": (300, 1500),
        "Renda Extra": (100, 800),
        
        # DESPESAS CRÍTICAS (baseadas nos dados reais)
        "Transporte": (5, 50),        # Uber: R$ 5-50
        "Alimentação": (5, 80),       # Cafés e refeições: R$ 5-80
        "Supermercado": (30, 200),    # Compras: R$ 30-200
        "Streaming": (10, 50),        # Assinaturas: R$ 10-50
        "Medicamentos": (10, 100),    # Farmácias: R$ 10-100
        "Roupas": (50, 500),          # Vestuário: R$ 50-500
        
        # OUTRAS DESPESAS
        "Combustível": (30, 200),
        "Moradia": (100, 1000),
        "Aluguel": (600, 4000),
        "Energia Elétrica": (60, 300),
        "Água": (25, 120),
        "Internet": (50, 150),
        "Telefone": (30, 100),
        "Gás": (20, 80),
        "Saúde": (50, 300),
        "Plano de Saúde": (150, 600),
        "Academia": (50, 150),
        "Terapia": (80, 250),
        "Educação": (200, 1500),
        "Cursos": (50, 400),
        "Livros": (20, 100),
        "Material Escolar": (30, 150),
        "Lazer": (30, 200),
        "Cinema": (15, 50),
        "Jogos": (20, 150),
        "Viagens": (200, 3000),
        "Restaurantes": (25, 150),
        "Bares": (20, 100),
        "Sapatos": (80, 300),
        "Cabeleireiro": (30, 150),
        "Cosméticos": (25, 200),
        "Cartão de Crédito": (100, 2000),
        "Empréstimos": (200, 1500),
        "Financiamentos": (300, 2000),
        "Seguros": (50, 400),
        "Impostos": (100, 1500),
        "IPTU": (200, 1500),
        "IPVA": (200, 1500),
        "Multas": (50, 300),
        "Crianças": (100, 800),
        "Pets": (50, 200),
        "Presentes": (30, 300),
        "Poupança": (100, 2000),
        "Previdência": (100, 800),
        "Doações": (20, 150),
        "Assinaturas": (10, 80),
        "Outros": (10, 300)
    }
    
    return faixas.get(categoria, (20, 200))

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def gerar_uuid():
    """Gera UUID único"""
    return str(uuid.uuid4())

def gerar_data_aleatoria():
    """Gera data aleatória no período"""
    inicio = datetime.strptime(DATA_INICIO, "%d/%m/%Y")
    fim = datetime.strptime(DATA_FIM, "%d/%m/%Y")
    delta = fim - inicio
    dias_aleatorios = random.randint(0, delta.days)
    data_aleatoria = inicio + timedelta(days=dias_aleatorios)
    return data_aleatoria.strftime("%d/%m/%Y")

def gerar_descricao_categoria(categoria, tipo_categoria):
    """Gera descrição para uma categoria específica"""
    
    # Usar gerador específico se disponível
    if categoria in GERADORES_ESPECIFICOS:
        if random.random() < 0.8:  # 80% chance de usar gerador específico
            return GERADORES_ESPECIFICOS[categoria]()
    
    # Descrições genéricas para outras categorias
    if tipo_categoria == "receitas":
        formatos = [
            f"Transferência Recebida - {categoria}",
            f"PIX Recebido - {categoria}",
            f"Depósito - {categoria}",
            f"TED Recebida - {categoria}"
        ]
    else:
        formatos = [
            f"Compra no débito - {categoria}",
            f"Transferência enviada pelo Pix - {categoria}",
            f"{categoria} - Pagamento",
            f"Conta de {categoria}"
        ]
    
    return random.choice(formatos)

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def gerar_dados_categoria(categoria, tipo_categoria):
    """Gera dados para uma categoria específica"""
    dados = []
    min_valor, max_valor = determinar_faixa_valor(categoria)
    
    # Mais exemplos para categorias críticas
    exemplos = EXEMPLOS_POR_CATEGORIA
    if categoria in ["Transporte", "Streaming", "Alimentação", "Supermercado"]:
        exemplos = 50  # Dobrar exemplos para categorias que falharam
    
    for i in range(exemplos):
        # Gerar valor
        if tipo_categoria == "receitas":
            valor = round(random.uniform(min_valor, max_valor), 2)
        else:
            valor = -round(random.uniform(min_valor, max_valor), 2)
        
        # Gerar descrição
        descricao = gerar_descricao_categoria(categoria, tipo_categoria)
        
        dados.append({
            "Data": gerar_data_aleatoria(),
            "Valor": valor,
            "Identificador": gerar_uuid(),
            "Descrição": descricao,
            "Categoria": categoria
        })
    
    return dados

def main():
    """Função principal"""
    print("Gerando dataset com solução emergencial...")
    
    todos_dados = []
    
    # Gerar receitas
    print("Processando receitas...")
    for categoria in CATEGORIAS_RECEITAS:
        dados = gerar_dados_categoria(categoria, "receitas")
        todos_dados.extend(dados)
        print(f"  ✅ {categoria}: {len(dados)} exemplos")
    
    # Gerar despesas
    print("Processando despesas...")
    for categoria in CATEGORIAS_DESPESAS:
        dados = gerar_dados_categoria(categoria, "despesas")
        todos_dados.extend(dados)
        exemplos = 50 if categoria in ["Transporte", "Streaming", "Alimentação", "Supermercado"] else EXEMPLOS_POR_CATEGORIA
        print(f"  ✅ {categoria}: {len(dados)} exemplos")
    
    # Embaralhar dados
    random.shuffle(todos_dados)
    
    # Criar DataFrame
    df = pd.DataFrame(todos_dados)
    
    # Salvar
    nome_arquivo = 'transacoes_emergencial_producao.csv'
    df.to_csv(nome_arquivo, index=False)
    
    print(f"\n🎉 DATASET EMERGENCIAL GERADO!")
    print("=" * 50)
    print(f"📄 Arquivo: {nome_arquivo}")
    print(f"📊 Total: {len(df)} transações")
    print(f"📊 Receitas: {len(df[df['Valor'] > 0])}")
    print(f"📊 Despesas: {len(df[df['Valor'] < 0])}")
    print(f"📊 Categorias: {df['Categoria'].nunique()}")
    
    # Estatísticas das categorias críticas
    print(f"\n🎯 FOCO NAS CATEGORIAS CRÍTICAS:")
    categorias_criticas = ["Transporte", "Streaming", "Alimentação", "Supermercado"]
    for cat in categorias_criticas:
        count = len(df[df['Categoria'] == cat])
        print(f"  {cat}: {count} exemplos")
    
    print(f"\n🚨 CORREÇÕES APLICADAS:")
    print(f"  ❌ Removida categoria 'Taxas Bancárias' (causava 40% dos erros)")
    print(f"  ✅ Adicionadas empresas reais: Uber, GOGIPSY, GIL DA TAPIOCA, etc.")
    print(f"  ✅ Descrições idênticas ao formato do banco")
    print(f"  ✅ 50 exemplos para categorias que falharam")
    
    print(f"\n🎯 PRÓXIMO PASSO:")
    print(f"Modifique seu treinamento_modelo_pre_processamento.py:")
    print(f"Troque: df = pd.read_csv('transacoes_melhorado.csv')")
    print(f"Por:    df = pd.read_csv('transacoes_emergencial_producao.csv')")
    
    return df

if __name__ == "__main__":
    dataset = main()


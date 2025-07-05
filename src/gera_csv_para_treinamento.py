import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# Configurações
EXEMPLOS_POR_CATEGORIA = 25  # Aumentado para melhor cobertura
DATA_INICIO = "01/01/2024"
DATA_FIM = "31/12/2024"

# ============================================================================
# MELHORIA PONTUAL 1: CONFIGURAÇÃO DINÂMICA DE GERADORES
# ============================================================================

# Configuração dos geradores específicos (NOVO)
CONFIGURACAO_GERADORES = {
    "Transporte": {"gerador": "gerar_descricoes_transporte", "percentual": 0.85},
    "Streaming": {"gerador": "gerar_descricoes_streaming", "percentual": 0.90},
    "Internet": {"gerador": "gerar_descricoes_internet", "percentual": 0.80},
    "Telefone": {"gerador": "gerar_descricoes_internet", "percentual": 0.80},
    "Supermercado": {"gerador": "gerar_descricoes_supermercado", "percentual": 0.85},
    "Alimentação": {"gerador": "gerar_descricoes_alimentacao", "percentual": 0.80},
    "Saúde": {"gerador": "gerar_descricoes_saude", "percentual": 0.75},
    "Medicamentos": {"gerador": "gerar_descricoes_saude", "percentual": 0.80},
    "Investimentos": {"gerador": "gerar_descricoes_investimento", "percentual": 1.0},
    "Energia Elétrica": {"gerador": "gerar_descricoes_energia", "percentual": 0.70},
    "Água": {"gerador": "gerar_descricoes_agua", "percentual": 0.70}
}

## CATEGORIAS CORRIGIDAS (RECEITAS EXPANDIDAS)
CATEGORIAS_CORRIGIDAS = {
    "receitas": {
        "Salário": [
            "Transferência Recebida - Salário mensal",
            "Depósito - Salário empresa",
            "TED Recebida - Pagamento salário",
            "Transferência - Salário líquido",
            "Crédito em conta - Salário"
        ],
        "Freelance": [
            "Transferência Recebida - Freelance",
            "PIX Recebido - Trabalho freelance",
            "TED Recebida - Projeto freelance",
            "Depósito - Serviço prestado"
        ],
        "Investimentos": [
            "Aplicação RDB - Resgate",
            "Tesouro Direto - Resgate",
            "CDB - Vencimento",
            "Poupança - Rendimento",
            "Fundo de investimento - Resgate"
        ],
        "Comissões": [
            "Transferência Recebida - Comissão",
            "PIX Recebido - Comissão de vendas",
            "TED Recebida - Comissão",
            "Depósito - Comissão recebida"
        ],
        "Aluguel Recebido": [
            "Transferência Recebida - Aluguel",
            "PIX Recebido - Aluguel imóvel",
            "TED Recebida - Aluguel",
            "Depósito - Aluguel recebido"
        ],
        "Vendas": [
            "Transferência Recebida - Venda de produto",
            "PIX Recebido - Venda",
            "TED Recebida - Venda",
            "Depósito - Venda realizada"
        ],
        "13º Salário": [
            "Transferência Recebida - 13º Salário",
            "Depósito - 13º Salário",
            "TED Recebida - 13º Salário",
            "Crédito em conta - 13º Salário"
        ],
        "Férias": [
            "Transferência Recebida - Férias",
            "Depósito - Férias",
            "TED Recebida - Férias",
            "Crédito em conta - Férias"
        ],
        "Bonificação": [
            "Transferência Recebida - Bonificação",
            "PIX Recebido - Bonificação",
            "TED Recebida - Bonificação",
            "Depósito - Bonificação recebida"
        ],
        "Restituição IR": [
            "Transferência Recebida - Restituição IR",
            "PIX Recebido - Restituição IR",
            "TED Recebida - Restituição IR",
            "Depósito - Restituição IR"
        ],
        "Pensão Recebida": [
            "Transferência Recebida - Pensão",
            "PIX Recebido - Pensão",
            "TED Recebida - Pensão",
            "Depósito - Pensão recebida"
        ],
        "Renda Extra": [
            "Transferência Recebida - Renda extra",
            "PIX Recebido - Renda extra",
            "TED Recebida - Renda extra",
            "Depósito - Renda extra"
        ]
    },
    "despesas": {
        # ESSENCIAIS (12 categorias)
        "Alimentação": [
            "iFood", "Uber Eats", "Rappi", "McDonald's", "Burger King",
            "Restaurante", "Lanchonete", "Padaria", "Delivery Much", "Aiqfome",
            "James Delivery", "Zé Delivery", "Daki", "Cornershop", "Quero Delivery",
            "Foody Delivery", "SODE", "Entregas Rápidas", "Apptite", "One Pizza",
            "China In Box", "Pizza Hut", "Bob's", "Habib's", "Cacau Show"
        ],
        "Supermercado": [
            "Carrefour", "Assaí Atacadista", "Grupo Mateus", "Supermercados BH",
            "GPA (Grupo Pão de Açúcar)", "Grupo Muffato", "Grupo Pereira", "Cencosud Brasil",
            "Mart Minas & Dom Atacadista", "Koch Supermercados", "DMA Distribuidora", "Zaffari",
            "Sonda Supermercados", "Rede Economia Prix", "Super Muffato", "Supermercado Amigão",
            "Supermercados Brasil", "Supermercado Pague Menos", "Supermercado Extrabom", "Extra"
        ],
        "Transporte": [
            "Uber", "99", "inDriver", "Lady Driver", "Wappa", "Garupa", "Rota Pop", 
            "Ubiz Car", "Chofer46", "Bibi Mob", "Buser", "Flapper", "Moovit", "Turbi",
            "Passagem de ônibus", "Metrô São Paulo", "Estacionamento shopping", "Pedágio rodovia", "Transferência enviada pelo Pix - Uber",
            "Compra no débito via NuPay - Uber", "Uber - Corrida", "Pagamento Uber via PIX"
        ],
        "Combustível": [
            "Posto Shell", "Ipiranga", "BR Petrobras", "Ale Combustíveis",
            "Posto Texaco", "Posto Esso", "BR Mania", "Posto Sinopec",
            "Abastecimento", "Gasolina", "Etanol", "Diesel", "GNV"
        ],
        "Moradia": [
            "Condomínio residencial", "Taxa de administração", "Manutenção predial",
            "Reforma do apartamento", "Pintura da casa", "Conserto hidráulico",
            "Serviço de limpeza", "Jardinagem", "Segurança predial", "Portaria", "Reforma do apartamento", "Pintura da casa",
            "Conserto hidráulico", "Manutenção predial"
        ],
        "Aluguel": [
            "Aluguel apartamento", "Aluguel casa", "Aluguel comercial",
            "Aluguel residencial", "Aluguel mensal", "Locação imóvel",
            "Aluguel quitinete", "Aluguel escritório", "Aluguel loja", "Aluguel galpão"
        ],
        "Energia Elétrica": [
            "Enel", "Light", "Copel", "Cemig", "Eletrobras", "Engie Brasil", 
            "CPFL Energia", "Neoenergia", "Equatorial Energia", "Coelce",
            "Conta de energia elétrica", "Conta de luz", "Fatura energia"
        ],
        "Água": [
            "Sabesp", "Cedae", "Sanepar", "Aegea Saneamento", "Iguá Saneamento",
            "Cagece", "SAAE", "Copasa", "Embasa", "Caern",
            "Conta de água", "Fatura de água", "Água e esgoto"
        ],
        "Internet": [
            "Vivo Fibra", "NET", "Tim Live", "Oi Fibra", "Claro",
            "Brisanet", "Vero Internet", "V.tal", "Algar Telecom", "Equatorial Telecom",
            "Giga+ Fibra", "Zaaz Telecom", "Marinter Telecom", "Tríade Fibra", "NTC", "Internet banda larga Vivo",
            "Fibra ótica NET", "Wi-Fi residencial Tim", "Plano de internet Oi"
        ],
        "Telefone": [
            "Vivo", "Claro", "Tim", "Oi", "Celular", "Plano pós-pago",
            "Plano móvel", "Telefone fixo", "Conta móvel", "Recarga celular", "Plano móvel Vivo", "Celular pós-pago Claro",
            "Recarga Tim", "Conta do celular"
        ],
        "Gás": [
            "Botijão de gás", "Gás de cozinha", "Gás natural", "Conta de gás",
            "Gás encanado", "Botijão P13", "Gás residencial", "Entrega de gás",
            "Recarga de gás", "Gás doméstico"
        ],
        "Outros": [
            "Despesa diversa", "Gasto não categorizado", "Compra variada",
            "Despesa geral", "Outros gastos", "Despesa eventual",
            "Gasto esporádico", "Compra ocasional", "Despesa extra", "Gasto imprevisto"
        ],

        # SAÚDE E BEM-ESTAR (5 categorias)
        "Saúde": [
            "Unimed", "Bradesco Saúde", "SulAmérica", "Hapvida NotreDame Intermédica", 
            "Amil", "Grupo NotreDame Intermédica", "Consulta médica", "Exame laboratorial",
            "Consulta dentista", "Fisioterapia", "Psicólogo", "Dermatologista"
        ],
        "Medicamentos": [
            "Raia Drogasil", "Grupo DPSP", "Pague Menos", "Drogaria São Paulo", 
            "Drogaria Pacheco", "Drogasil", "Ultrafarma", "Drogal", "Farmácias Pague Menos",
            "Medicamento controlado", "Remédio de uso contínuo", "Farmácia popular"
        ],
        "Plano de Saúde": [
            "Plano de saúde Unimed", "Plano de saúde Hapvida", "Plano de saúde Bradesco",
            "Fatura plano de saúde", "Plano de saúde Amil", "Plano de saúde SulAmérica",
            "Plano de saúde NotreDame", "Plano de saúde Prevent Senior", "Convênio médico"
        ],
        "Academia": [
            "Mensalidade academia", "Smart Fit", "Bio Ritmo", "Bodytech", "Bluefit",
            "Academia local", "Personal trainer", "Aulas de dança", "Pilates", "Crossfit"
        ],
        "Terapia": [
            "Sessão de psicoterapia", "Psicólogo clínico", "Terapia de casal",
            "Psiquiatra", "Terapia familiar", "Análise psicológica", "Consulta psicológica",
            "Terapia cognitiva", "Acompanhamento psicológico", "Sessão terapêutica"
        ],

        # EDUCAÇÃO (4 categorias)
        "Educação": [
            "Mensalidade escola", "Universidade particular", "Curso técnico",
            "Pós-graduação", "MBA executivo", "Curso profissionalizante",
            "Faculdade", "Colégio particular", "Escola infantil", "Ensino fundamental"
        ],
        "Cursos": [
            "Curso de inglês", "Curso online Udemy", "Curso de programação",
            "Curso de idiomas", "Curso profissionalizante", "Curso de marketing",
            "Curso de design", "Curso de culinária", "Curso de música", "Curso de fotografia"
        ],
        "Livros": [
            "Compra de livros Amazon", "Livraria Saraiva", "Livro comprado na Amazon",
            "Compra de livro didático", "Aquisição de livros", "Compra de livros usados",
            "Compra de livros digitais", "Compra de livros escolares", "Compra de livros técnicos"
        ],
        "Material Escolar": [
            "Papelaria escolar", "Material didático", "Cadernos e canetas",
            "Mochila escolar", "Calculadora científica", "Estojo escolar",
            "Lápis de cor", "Material de arte", "Régua e compasso", "Agenda escolar"
        ],

        # LAZER (7 categorias)
        "Lazer": [
            "Parque de diversões",
            "Boliche",
            "Karaokê",
            "Escape room",
            "Paintball", "Kart", "Clube recreativo", "Parque aquático",
            "Zoológico", "Museu", "Teatro", "Show musical"
        ],
        "Cinema": [
            "Cinema Iguatemi", "Cinema UCI", "Sessão de cinema Cinépolis",
            "Cinema Centerplex", "Cinema Cinemark", "Cinema Moviecom",
            "Cinema Kinoplex", "Cinema PlayArte", "Cinema Cinesystem", "Cinema Lumière"
        ],
        "Streaming": [
            "Netflix", "Spotify", "Amazon Prime Video", "Disney+", "YouTube Premium",
            "Globoplay", "HBO Max", "Apple TV+", "Paramount+", "Star+", "Looke", "Mubi",
            "Telecine Play", "Crunchyroll", "UOL Play", "Watch Brasil", "Netflix - Assinatura mensal", "Spotify Premium",
            "Amazon Prime Video", "Disney+ assinatura"
        ],
        "Jogos": [
            "Steam jogos", "PlayStation Store", "Xbox Game Pass", "Nintendo eShop",
            "Epic Games Store", "Jogo mobile", "Compra de jogo", "DLC jogo",
            "Assinatura gaming", "Créditos de jogo"
        ],
        "Viagens": [
            "Passagem aérea", "Hotel reserva", "Booking.com", "Airbnb hospedagem",
            "Aluguel de carro", "Seguro viagem", "Excursão turística",
            "Pacote de viagem", "Transfer aeroporto", "Hospedagem"
        ],
        "Restaurantes": [
            "Restaurante italiano", "Churrascaria rodízio", "Sushi delivery",
            "Pizzaria artesanal", "Hambúrguer gourmet", "Comida mexicana",
            "Restaurante árabe", "Comida chinesa", "Restaurante vegetariano", "Bistrô francês"
        ],
        "Bares": [
            "Bar da esquina", "Pub irlandês", "Choperia local", "Bar de vinhos",
            "Boteco tradicional", "Cervejaria artesanal", "Lounge bar",
            "Bar temático", "Casa noturna", "Bar de coquetéis"
        ],

        # VESTUÁRIO (4 categorias)
        "Roupas": [
            "Renner", "C&A", "Zara", "Hering", "Riachuelo", "Marisa",
            "Forever 21", "Levis", "Nike", "Adidas", "Compra de vestuário", "Camiseta Renner", "Calça jeans C&A",
            "Vestido Zara", "Roupa íntima"
        ],
        "Sapatos": [
            "Tênis Nike", "Sapato social", "Sandália Havaianas", "Bota de couro",
            "Sapatênis casual", "Chinelo de dedo", "Sapato feminino", "Tênis Adidas",
            "Calçado esportivo", "Sapato infantil"
        ],
        "Cabeleireiro": [
            "Salão de beleza", "Corte de cabelo", "Escova progressiva",
            "Coloração capilar", "Hidratação capilar", "Manicure e pedicure",
            "Barbeiro", "Alisamento capilar", "Penteado para festa", "Tratamento capilar"
        ],
        "Cosméticos": [
            "Maquiagem Sephora", "Perfume importado", "Creme facial",
            "Shampoo e condicionador", "Protetor solar", "Base e corretivo",
            "Batom e gloss", "Creme hidratante", "Perfume nacional", "Kit de maquiagem"
        ],

        # FINANCEIRO (5 categorias)
        "Cartão de Crédito": [
            "Fatura cartão Nubank", "Fatura cartão Itaú", "Fatura cartão Santander",
            "Fatura cartão de crédito", "Fatura cartão Bradesco", "Fatura cartão Caixa",
            "Fatura cartão Banco do Brasil", "Fatura cartão Inter", "Anuidade cartão"
        ],
        "Empréstimos": [
            "Parcela empréstimo pessoal", "Crediário loja", "Financiamento estudantil",
            "Empréstimo consignado", "Crédito pessoal", "Empréstimo bancário",
            "Refinanciamento dívida", "Antecipação saque aniversário", "Microcrédito"
        ],
        "Financiamentos": [
            "Financiamento imobiliário", "Financiamento veículo", "Prestação casa própria",
            "Financiamento moto", "Consórcio imobiliário", "Consórcio automóvel",
            "Prestação apartamento", "Financiamento terreno", "Leasing veículo", "CDC veículo"
        ],
        "Taxas Bancárias": [
            "Taxa de manutenção conta", "Tarifa DOC/TED", "Taxa cartão de crédito",
            "Tarifa saque", "Taxa de transferência", "Anuidade conta corrente",
            "Taxa de serviços", "Tarifa bancária", "Taxa de administração", "Custo operacional"
        ],
        "Seguros": [
            "Seguro auto", "Seguro residencial", "Seguro de vida", "Seguro viagem",
            "Seguro celular", "Seguro prestamista", "Seguro empresarial",
            "Seguro acidentes pessoais", "Seguro bike", "Seguro pet"
        ],

        # IMPOSTOS (4 categorias)
        "Impostos": [
            "Imposto de Renda", "ISS serviços", "ITBI imóvel", "Taxa de licenciamento",
            "Contribuição sindical", "Taxa municipal", "Imposto estadual", "Taxa federal"
        ],
        "IPTU": [
            "IPTU anual", "IPTU parcelado", "Imposto predial", "Taxa territorial urbana",
            "IPTU à vista", "IPTU residencial", "IPTU comercial", "IPTU terreno",
            "IPTU apartamento", "IPTU casa"
        ],
        "IPVA": [
            "IPVA carro", "IPVA moto", "Imposto veículo", "IPVA anual",
            "IPVA parcelado", "IPVA à vista", "Licenciamento veículo",
            "IPVA automóvel", "IPVA motocicleta", "Taxa veicular"
        ],
        "Multas": [
            "Multa de trânsito", "Multa por velocidade", "Multa estacionamento",
            "Multa zona azul", "Multa semáforo", "Multa rodízio",
            "Multa administrativa", "Multa ambiental", "Infração de trânsito"
        ],

        # FAMÍLIA (3 categorias)
        "Crianças": [
            "Escola infantil", "Pediatra consulta", "Brinquedos", "Roupas infantis",
            "Fraldas e produtos", "Creche mensal", "Curso de natação",
            "Festa infantil", "Material escolar", "Lanche escolar"
        ],
        "Pets": [
            "Veterinário consulta", "Ração para cães", "Pet shop", "Vacina animal",
            "Banho e tosa", "Medicamento pet", "Brinquedo para pet",
            "Castração animal", "Hotel para pets", "Adestramento"
        ],
        "Presentes": [
            "Presente aniversário", "Presente Dia das Mães", "Presente Natal",
            "Presente casamento", "Presente Dia dos Pais", "Presente namorada",
            "Presente amigo", "Presente formatura", "Presente bebê", "Presente Páscoa"
        ],

        # INVESTIMENTOS (3 categorias)
        "Poupança": [
            "Depósito poupança", "Aplicação poupança", "Transferência para poupança",
            "Reserva de emergência", "Poupança mensal", "Economia pessoal",
            "Guardar dinheiro", "Poupança programada", "Aplicação automática", "Conta poupança"
        ],
        "Investimentos": [
            "Aplicação RDB", "Compra de ações", "Investimento CDB", "Tesouro Direto",
            "Fundo de investimento", "LCI/LCA", "Debêntures", "Criptomoedas",
            "COE investimento", "Previdência privada", "Aplicação RDB",
            "Compra de ações B3", "Tesouro Direto", "CDB Banco Inter"
        ],
        "Previdência": [
            "Previdência privada", "PGBL mensal", "VGBL aplicação", "Plano previdenciário",
            "Aposentadoria privada", "Contribuição previdência", "Fundo previdência",
            "Plano de aposentadoria", "Previdência complementar", "Reserva aposentadoria"
        ],

        # DIVERSOS (2 categorias)
        "Doações": [
            "Doação para ONG", "Doação igreja", "Doação para abrigo de animais",
            "Doação para hospital", "Doação para campanha", "Doação para instituição",
            "Doação para escola", "Doação para associação", "Doação para projeto social"
        ],
        "Assinaturas": [
            "Spotify Premium", "YouTube Premium", "Google One", "Dropbox Plus",
            "Office 365", "Adobe Creative", "iCloud storage", "Amazon Prime",
            "Coursera Plus", "LinkedIn Premium"
        ]
    }
}

# EMPRESAS REAIS POR CATEGORIA (mantendo sua estrutura)
EMPRESAS_TRANSPORTE = [
    "Uber", "99", "WINPAY SERVIÇOS LTDA", "UPPAY", "MOVIDA",
    "Posto Shell", "Ipiranga", "BR Petrobras", "Ale Combustíveis",
    "Estacionamento Rotativo", "Pedágio CCR", "Localiza"
]

EMPRESAS_STREAMING = [
    "Netflix", "Spotify", "Amazon Prime", "Disney+", "YouTube Premium",
    "Deezer", "Apple Music", "GOGIPSY", "Paramount+", "HBO Max",
    "Globoplay", "Crunchyroll", "Twitch"
]

EMPRESAS_INTERNET = [
    "Vivo Fibra", "NET Claro", "Tim Live", "Oi Fibra",
    "BOACOMPRA.COM", "Mercado Pago", "PagSeguro",
    "Copel Telecom", "Algar Telecom"
]

EMPRESAS_SUPERMERCADO = [
    "Extra Supermercado", "Carrefour", "Walmart", "Pão de Açúcar",
    "Super São Luiz", "Atacadão", "BIG", "Mercado Livre",
    "Supermercado Zona Sul", "Mercadinho do João"
]

EMPRESAS_ALIMENTACAO = [
    "iFood", "Uber Eats", "Rappi", "McDonald's", "Burger King",
    "KFC", "Subway", "Pizza Hut", "Domino's", "Outback"
]

EMPRESAS_SAUDE = [
    "Drogasil", "Drogaria São Paulo", "Ultrafarma", "Pacheco",
    "Unimed", "Bradesco Saúde", "SulAmérica", "Amil",
    "Hospital Albert Einstein", "Laboratório Fleury"
]

EMPRESAS_INVESTIMENTO = [
    "XP Investimentos", "Rico", "Clear", "Inter Invest",
    "Nubank Investimentos", "BTG Pactual", "Itaú Investimentos"
]

EMPRESAS_ENERGIA = [
    "Enel", "Light", "Copel", "Cemig", "Eletrobras",
    "Engie Brasil", "CPFL Energia", "Neoenergia", "Equatorial Energia"
]

EMPRESAS_AGUA = [
    "Sabesp", "Cedae", "Sanepar", "Aegea Saneamento", "Iguá Saneamento"
]

# Bancos e códigos reais (mantendo sua estrutura)
BANCOS = [
    ("Banco do Brasil", "001", "0001"),
    ("Caixa Econômica Federal", "104", "104"),
    ("Banco Bradesco", "237", "237"),
    ("Itaú Unibanco", "341", "341"),
    ("Banco Santander", "033", "033"),
    ("Banco Inter", "077", "077"),
    ("Nubank", "260", "260"),
    ("Banco Pan", "623", "623"),
    ("Banco Safra", "422", "422"),
    ("Banco BMG", "318", "318"),
    ("Banco do Nordeste", "004", "004"),
    ("Banco da Amazônia", "003", "003"),
    ("Banco Votorantim", "655", "655"),
    ("Banco Modal", "746", "746"),
    ("Banco Original", "212", "212")
]

# CNPJs e CPFs fictícios (mantendo sua estrutura)
CNPJS_FICTICIOS = [
    "17.895.646/0001-87", "09.370.323/0001-41", "48.533.288/0001-96",
    "21.575.374/0001-05", "06.375.668/0003-61", "43.082.596/0003-90"
]

CPFS_MASCARADOS = [
    "•••.536.383-••", "•••.876.933-••", "•••.431.142-••",
    "•••.707.073-••", "•••.593.083-••", "•••.968.523-••"
]

CONFIGURACAO_GERADORES = {
    "Transporte": {"gerador": "gerar_descricoes_transporte", "percentual": 0.85},
    "Streaming": {"gerador": "gerar_descricoes_streaming", "percentual": 0.90},
    "Internet": {"gerador": "gerar_descricoes_internet", "percentual": 0.80},
    "Telefone": {"gerador": "gerar_descricoes_internet", "percentual": 0.80},
    "Supermercado": {"gerador": "gerar_descricoes_supermercado", "percentual": 0.85},
    "Alimentação": {"gerador": "gerar_descricoes_alimentacao", "percentual": 0.80},
    "Saúde": {"gerador": "gerar_descricoes_saude", "percentual": 0.75},
    "Medicamentos": {"gerador": "gerar_descricoes_saude", "percentual": 0.80},
    "Investimentos": {"gerador": "gerar_descricoes_investimento", "percentual": 1.0},
    "Energia Elétrica": {"gerador": "gerar_descricoes_energia", "percentual": 0.70},
    "Água": {"gerador": "gerar_descricoes_agua", "percentual": 0.70}
}

def gerar_uuid():
    """Gera um UUID no formato usado pelo banco"""
    return str(uuid.uuid4())

def gerar_data_aleatoria():
    """Gera uma data aleatória no período especificado"""
    inicio = datetime.strptime(DATA_INICIO, "%d/%m/%Y")
    fim = datetime.strptime(DATA_FIM, "%d/%m/%Y")
    
    delta = fim - inicio
    dias_aleatorios = random.randint(0, delta.days)
    data_aleatoria = inicio + timedelta(days=dias_aleatorios)
    
    return data_aleatoria.strftime("%d/%m/%Y")

# ============================================================================
# MELHORIA PONTUAL 2: GERADORES ESPECÍFICOS MELHORADOS
# ============================================================================

def gerar_descricoes_transporte():
    """Versão melhorada com mais variação baseada no tipo de empresa"""
    empresa = random.choice(EMPRESAS_TRANSPORTE)
    
    # Diferentes tipos baseados na empresa
    if "Posto" in empresa or "Ipiranga" in empresa or "BR" in empresa or "Ale" in empresa:
        formatos = [
            f"Compra no débito - {empresa}",
            f"Pagamento {empresa} via PIX",
            f"{empresa} - Abastecimento",
            f"Combustível - {empresa}",
            f"Transferência enviada pelo Pix - {empresa}"
        ]
    elif "Pedágio" in empresa or "CCR" in empresa:
        formatos = [
            f"Pagamento {empresa} via PIX",
            f"{empresa} - Viagem",
            f"Taxa de pedágio - {empresa}",
            f"Transferência enviada pelo Pix - {empresa}"
        ]
    elif "Estacionamento" in empresa:
        formatos = [
            f"Pagamento {empresa} via PIX",
            f"{empresa} - Zona azul",
            f"Taxa de estacionamento - {empresa}",
            f"Compra no débito - {empresa}"
        ]
    else:  # Uber, 99, etc.
        formatos = [
            f"Transferência enviada pelo Pix - {empresa}",
            f"Compra no débito via NuPay - {empresa}",
            f"{empresa} - Corrida",
            f"{empresa} - Viagem",
            f"Pagamento {empresa} via PIX",
            f"{empresa} - Transporte urbano"
        ]
    
    return random.choice(formatos)

def gerar_descricoes_streaming():
    """Versão melhorada para streaming"""
    empresa = random.choice(EMPRESAS_STREAMING)
    
    formatos = [
        f"Transferência enviada pelo Pix - {empresa}",
        f"Compra no débito - {empresa}",
        f"{empresa} - Assinatura mensal",
        f"{empresa} - Plano {random.choice(['Básico', 'Padrão', 'Premium'])}",
        f"Assinatura {empresa}",
        f"{empresa} - Renovação automática",
        f"Pagamento {empresa} via PIX"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_internet():
    """Versão melhorada para internet/telefone"""
    empresa = random.choice(EMPRESAS_INTERNET)
    
    formatos = [
        f"Transferência enviada pelo Pix - {empresa}",
        f"Compra no débito - {empresa}",
        f"{empresa} - Mensalidade",
        f"{empresa} - Plano {random.choice(['Básico', 'Intermediário', 'Premium'])}",
        f"Pagamento {empresa} via PIX",
        f"{empresa} - Internet banda larga",
        f"{empresa} - Conta mensal"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_supermercado():
    """Versão melhorada para supermercado"""
    empresa = random.choice(EMPRESAS_SUPERMERCADO)
    
    formatos = [
        f"Compra no débito - {empresa}",
        f"Compra no débito via NuPay - {empresa}",
        f"Transferência enviada pelo Pix - {empresa}",
        f"{empresa} - Compras",
        f"{empresa} - Mercado",
        f"Pagamento {empresa} via PIX",
        f"{empresa} - Compras do mês"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_alimentacao():
    """Versão melhorada para alimentação"""
    empresa = random.choice(EMPRESAS_ALIMENTACAO)
    
    formatos = [
        f"Compra no débito via NuPay - {empresa}",
        f"Compra no débito - {empresa}",
        f"Transferência enviada pelo Pix - {empresa}",
        f"{empresa} - Pedido",
        f"{empresa} - Delivery",
        f"Pagamento {empresa} via PIX",
        f"{empresa} - Refeição"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_saude():
    """Versão melhorada para saúde"""
    empresa = random.choice(EMPRESAS_SAUDE)
    
    formatos = [
        f"Compra no débito - {empresa}",
        f"Compra no débito via NuPay - {empresa}",
        f"Transferência enviada pelo Pix - {empresa}",
        f"{empresa} - Medicamentos",
        f"{empresa} - Consulta",
        f"Pagamento {empresa} via PIX",
        f"{empresa} - Plano de saúde"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_investimento():
    """Versão melhorada para investimentos"""
    empresa = random.choice(EMPRESAS_INVESTIMENTO)
    tipo_operacao = random.choice(["Aplicação", "Resgate", "Transferência"])
    tipo_investimento = random.choice(["RDB", "CDB", "Tesouro Direto", "Ações", "Fundos"])
    
    formatos = [
        f"{tipo_operacao} {tipo_investimento}",
        f"{empresa} - {tipo_operacao}",
        f"{tipo_investimento} - {tipo_operacao}",
        f"Transferência - {tipo_investimento}",
        f"{empresa} - Investimento"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_energia():
    """Novo gerador para energia elétrica"""
    empresa = random.choice(EMPRESAS_ENERGIA)
    
    formatos = [
        f"Transferência enviada pelo Pix - {empresa}",
        f"Compra no débito - {empresa}",
        f"{empresa} - Energia elétrica",
        f"{empresa} - Conta de luz",
        f"Pagamento {empresa} via PIX",
        f"{empresa} - Conta mensal"
    ]
    
    return random.choice(formatos)

def gerar_descricoes_agua():
    """Novo gerador para água"""
    empresa = random.choice(EMPRESAS_AGUA)
    
    formatos = [
        f"Transferência enviada pelo Pix - {empresa}",
        f"Compra no débito - {empresa}",
        f"{empresa} - Conta de água",
        f"{empresa} - Saneamento",
        f"Pagamento {empresa} via PIX",
        f"{empresa} - Água e esgoto"
    ]
    
    return random.choice(formatos)

def determinar_faixa_valor(categoria):
    """Determina faixa de valor baseada na categoria - EXPANDIDA PARA 72 CATEGORIAS"""
    
    faixas = {
        # ====================================================================
        # RECEITAS
        # ====================================================================
        "Salário": (1500, 12000),
        "Freelance": (200, 3000),
        "Investimentos": (50, 8000),
        "Comissões": (100, 2000),
        "Aluguel Recebido": (500, 3000),
        "Vendas": (50, 1500),
        "13º Salário": (1500, 12000),
        "Férias": (1000, 8000),
        "Bonificação": (200, 5000),
        "Restituição IR": (100, 3000),
        "Pensão Recebida": (300, 2000),
        "Renda Extra": (100, 1000),
        "Recebimentos Gerais": (50, 2000),
        
        # ====================================================================
        # DESPESAS - ESSENCIAIS
        # ====================================================================
        "Alimentação": (15, 100),
        "Supermercado": (30, 400),
        "Transporte": (5, 40),
        "Combustível": (30, 200),
        "Moradia": (100, 1000),
        "Aluguel": (600, 4000),
        "Energia Elétrica": (60, 400),
        "Água": (25, 150),
        "Internet": (50, 200),
        "Telefone": (30, 120),
        "Gás": (20, 80),
        "Outros": (10, 500),
        
        # ====================================================================
        # DESPESAS - SAÚDE E BEM-ESTAR
        # ====================================================================
        "Saúde": (50, 500),
        "Medicamentos": (20, 300),
        "Plano de Saúde": (150, 800),
        "Academia": (50, 200),
        "Terapia": (80, 300),
        
        # ====================================================================
        # DESPESAS - EDUCAÇÃO
        # ====================================================================
        "Educação": (200, 2000),
        "Cursos": (50, 500),
        "Livros": (20, 150),
        "Material Escolar": (30, 200),
        
        # ====================================================================
        # DESPESAS - LAZER
        # ====================================================================
        "Lazer": (30, 300),
        "Cinema": (15, 60),
        "Streaming": (10, 60),
        "Jogos": (20, 200),
        "Viagens": (200, 5000),
        "Restaurantes": (25, 200),
        "Bares": (20, 150),
        
        # ====================================================================
        # DESPESAS - VESTUÁRIO
        # ====================================================================
        "Roupas": (50, 500),
        "Sapatos": (80, 400),
        "Cabeleireiro": (30, 200),
        "Cosméticos": (25, 300),
        
        # ====================================================================
        # DESPESAS - FINANCEIRO
        # ====================================================================
        "Cartão de Crédito": (100, 3000),
        "Empréstimos": (200, 2000),
        "Financiamentos": (300, 3000),
        "Taxas Bancárias": (5, 50),
        "Seguros": (50, 500),
        
        # ====================================================================
        # DESPESAS - IMPOSTOS
        # ====================================================================
        "Impostos": (100, 2000),
        "IPTU": (200, 2000),
        "IPVA": (200, 2000),
        "Multas": (50, 500),
        
        # ====================================================================
        # DESPESAS - FAMÍLIA
        # ====================================================================
        "Crianças": (100, 1000),
        "Pets": (50, 300),
        "Presentes": (30, 500),
        
        # ====================================================================
        # DESPESAS - INVESTIMENTOS
        # ====================================================================
        "Poupança": (100, 3000),
        "Investimentos": (100, 5000),  # Como despesa (aplicação)
        "Previdência": (100, 1000),
        
        # ====================================================================
        # DESPESAS - DIVERSOS
        # ====================================================================
        "Doações": (20, 200),
        "Assinaturas": (10, 100)
    }
    
    return faixas.get(categoria, (20, 300))

# ============================================================================
# MELHORIA PONTUAL 3: VALIDAÇÃO BÁSICA
# ============================================================================

def validar_dados_basico(dados, categoria, tipo_categoria):
    """Validação básica dos dados gerados"""
    erros = []
    
    for i, item in enumerate(dados):
        # Verificar campos obrigatórios
        if not all(key in item for key in ["Data", "Valor", "Identificador", "Descrição", "Categoria"]):
            erros.append(f"Item {i}: Campos obrigatórios ausentes")
            continue
        
        # Verificar sinal do valor
        if tipo_categoria == "receitas" and item["Valor"] <= 0:
            erros.append(f"Item {i}: Receita com valor negativo: {item['Valor']}")
        elif tipo_categoria == "despesas" and item["Valor"] >= 0:
            erros.append(f"Item {i}: Despesa com valor positivo: {item['Valor']}")
        
        # Verificar descrição
        if not item["Descrição"] or len(item["Descrição"]) < 3:
            erros.append(f"Item {i}: Descrição inválida: '{item['Descrição']}'")
        
        # Verificar categoria
        if item["Categoria"] != categoria:
            erros.append(f"Item {i}: Categoria incorreta: {item['Categoria']} != {categoria}")
    
    return len(erros) == 0, erros

# ============================================================================
# MELHORIA PONTUAL 4: FUNÇÕES AUXILIARES PARA DESCRIÇÕES
# ============================================================================

def gerar_descricao_receita(categoria, exemplos):
    """Gera descrição para receitas usando configuração dinâmica"""
    config = CONFIGURACAO_GERADORES.get(categoria)
    
    if config and random.random() < config["percentual"]:
        gerador_nome = config["gerador"]
        gerador_func = globals().get(gerador_nome)
        if gerador_func:
            return gerador_func()
    
    # Lógica específica para receitas
    if categoria in ["Salário", "Freelance"]:
        exemplo_base = random.choice(exemplos)
        if random.choice([True, False]):
            return f"Transferência recebida pelo Pix - {exemplo_base}"
        else:
            return exemplo_base
    else:
        return random.choice(exemplos)

def gerar_descricao_despesa(categoria, exemplos):
    """Gera descrição para despesas usando configuração dinâmica"""
    config = CONFIGURACAO_GERADORES.get(categoria)
    
    if config and random.random() < config["percentual"]:
        gerador_nome = config["gerador"]
        gerador_func = globals().get(gerador_nome)
        if gerador_func:
            return gerador_func()
    
    # Formato genérico para outras categorias
    exemplo_base = random.choice(exemplos)
    tipo_transacao = random.choice(["debito", "pix", "normal"])
    
    if tipo_transacao == "debito":
        if random.choice([True, False]):
            return f"Compra no débito via NuPay - {exemplo_base}"
        else:
            return f"Compra no débito - {exemplo_base}"
    elif tipo_transacao == "pix":
        return f"Transferência enviada pelo Pix - {exemplo_base}"
    else:
        return exemplo_base

# ============================================================================
# MELHORIA PONTUAL 5: FUNÇÃO PRINCIPAL SIMPLIFICADA
# ============================================================================

def gerar_dados_categoria(categoria, exemplos, tipo_categoria):
    """Versão simplificada com configuração dinâmica"""
    dados = []
    min_valor, max_valor = determinar_faixa_valor(categoria)
    
    for i in range(EXEMPLOS_POR_CATEGORIA):
        # Gerar valor baseado no tipo
        if tipo_categoria == "receitas":
            valor = round(random.uniform(min_valor, max_valor), 2)
        else:
            valor = -round(random.uniform(min_valor, max_valor), 2)
        
        # Gerar descrição usando funções auxiliares
        if tipo_categoria == "receitas":
            descricao = gerar_descricao_receita(categoria, exemplos)
        else:
            descricao = gerar_descricao_despesa(categoria, exemplos)
        
        dados.append({
            "Data": gerar_data_aleatoria(),
            "Valor": valor,
            "Identificador": gerar_uuid(),
            "Descrição": descricao,
            "Categoria": categoria
        })
    
    return dados

# ============================================================================
# MELHORIA PONTUAL 6: ESTATÍSTICAS MELHORADAS
# ============================================================================

def gerar_estatisticas_detalhadas(df):
    """Estatísticas mais detalhadas"""
    print(f"\n📊 ESTATÍSTICAS DETALHADAS:")
    print("=" * 60)
    
    # Por categoria
    print("\n📈 Por Categoria:")
    for categoria in sorted(df['Categoria'].unique()):
        cat_data = df[df['Categoria'] == categoria]
        valor_medio = cat_data['Valor'].mean()
        sinal = "+" if valor_medio > 0 else ""
        print(f"  {categoria:20} {len(cat_data):3} transações | Média: {sinal}R$ {abs(valor_medio):7.2f}")
    
    # Tipos de descrição
    print("\n🔍 Tipos de Transação:")
    tipos = {"PIX": 0, "Débito": 0, "Transferência": 0, "Assinatura": 0, "Outros": 0}
    
    for desc in df['Descrição']:
        desc_lower = desc.lower()
        if "pix" in desc_lower:
            tipos["PIX"] += 1
        elif "débito" in desc_lower:
            tipos["Débito"] += 1
        elif "transferência" in desc_lower:
            tipos["Transferência"] += 1
        elif "assinatura" in desc_lower:
            tipos["Assinatura"] += 1
        else:
            tipos["Outros"] += 1
    
    for tipo, count in tipos.items():
        percentual = (count / len(df)) * 100
        print(f"  {tipo:15} {count:4} ({percentual:5.1f}%)")
    
    # Distribuição de valores
    print(f"\n💰 Distribuição de Valores:")
    receitas = df[df['Valor'] > 0]
    despesas = df[df['Valor'] < 0]
    
    if len(receitas) > 0:
        print(f"  Receitas: Min R$ {receitas['Valor'].min():.2f} | Max R$ {receitas['Valor'].max():.2f} | Média R$ {receitas['Valor'].mean():.2f}")
    if len(despesas) > 0:
        print(f"  Despesas: Min R$ {abs(despesas['Valor'].max()):.2f} | Max R$ {abs(despesas['Valor'].min()):.2f} | Média R$ {abs(despesas['Valor'].mean()):.2f}")

def main():
    """Função principal melhorada"""
    print("🔧 Gerando dataset MELHORADO para treinamento de IA...")
    print("Melhorias: Configuração dinâmica + Validação + Estatísticas")
    print("=" * 70)
    
    todos_dados = []
    erros_totais = 0
    
    # Processar categorias de receita
    print("Processando categorias de receita...")
    for categoria, exemplos in CATEGORIAS_CORRIGIDAS["receitas"].items():
        dados_categoria = gerar_dados_categoria(categoria, exemplos, "receitas")
        
        # Validar dados
        valido, erros = validar_dados_basico(dados_categoria, categoria, "receitas")
        if not valido:
            print(f"  ⚠️  {categoria}: {len(dados_categoria)} exemplos ({len(erros)} erros)")
            erros_totais += len(erros)
        else:
            print(f"  ✅ {categoria}: {len(dados_categoria)} exemplos")
        
        todos_dados.extend(dados_categoria)
    
    # Processar categorias de despesa
    print("Processando categorias de despesa...")
    for categoria, exemplos in CATEGORIAS_CORRIGIDAS["despesas"].items():
        dados_categoria = gerar_dados_categoria(categoria, exemplos, "despesas")
        
        # Validar dados
        valido, erros = validar_dados_basico(dados_categoria, categoria, "despesas")
        if not valido:
            print(f"  ⚠️  {categoria}: {len(dados_categoria)} exemplos ({len(erros)} erros)")
            erros_totais += len(erros)
        else:
            print(f"  ✅ {categoria}: {len(dados_categoria)} exemplos")
        
        todos_dados.extend(dados_categoria)
    
    # Embaralhar os dados
    random.shuffle(todos_dados)
    
    # Criar DataFrame
    df = pd.DataFrame(todos_dados)
    
    # Salvar CSV
    nome_arquivo = 'transacoes_melhorado.csv'
    df.to_csv(nome_arquivo, index=False)
    
    print(f"\n=== DATASET MELHORADO GERADO COM SUCESSO ===")
    print(f"Arquivo: {nome_arquivo}")
    print(f"Total de transações: {len(df)}")
    print(f"Total de categorias: {len(CATEGORIAS_CORRIGIDAS['receitas']) + len(CATEGORIAS_CORRIGIDAS['despesas'])}")
    print(f"Período: {DATA_INICIO} a {DATA_FIM}")
    print(f"Exemplos por categoria: {EXEMPLOS_POR_CATEGORIA}")
    print(f"Erros de validação: {erros_totais}")
    
    # Estatísticas básicas
    receitas = df[df['Valor'] > 0]
    despesas = df[df['Valor'] < 0]
    
    print(f"\nEstatísticas Básicas:")
    print(f"  Receitas: {len(receitas)} transações (R$ {receitas['Valor'].sum():.2f})")
    print(f"  Despesas: {len(despesas)} transações (R$ {abs(despesas['Valor'].sum()):.2f})")
    
    # Estatísticas detalhadas
    gerar_estatisticas_detalhadas(df)
    
    # Mostrar exemplos das categorias corrigidas
    print(f"\n🎯 EXEMPLOS DAS MELHORIAS APLICADAS:")
    print("=" * 50)
    
    # Exemplos de Transporte
    transporte_exemplos = df[df['Categoria'] == 'Transporte']['Descrição'].head(5)
    if len(transporte_exemplos) > 0:
        print(f"\n🚗 Transporte:")
        for desc in transporte_exemplos:
            print(f"  - {desc}")
    
    # Exemplos de Streaming
    streaming_exemplos = df[df['Categoria'] == 'Streaming']['Descrição'].head(5)
    if len(streaming_exemplos) > 0:
        print(f"\n📺 Streaming:")
        for desc in streaming_exemplos:
            print(f"  - {desc}")
    
    print(f"\n🎯 PRÓXIMO PASSO:")
    print(f"Modifique seu treinamento_modelo_pre_processamento.py:")
    print(f"Troque: df = pd.read_csv('transacoes_corrigido.csv') caso seja necessário o nome do arquivo gerado")
    print(f"Por:    df = pd.read_csv('transacoes_melhorado_v2.csv')")
    print(f"Depois execute: python treinamento_modelo_pre_processamento.py")
    
    return df

if __name__ == "__main__":
    dataset = main()


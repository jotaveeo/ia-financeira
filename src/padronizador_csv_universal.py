import pandas as pd
import numpy as np
import re
from datetime import datetime
from formatos_bancos_brasileiros import FORMATOS_BANCOS, MAPEAMENTO_COLUNAS, FORMATOS_DATA, SEPARADORES_DECIMAIS

class PadronizadorCSV:
    """
    Classe para padronizar CSVs de diferentes bancos para um formato único
    que funciona com o modelo de IA treinado
    """
    
    def __init__(self):
        self.formato_padrao = {
            "colunas": ["Data", "Valor", "Identificador", "Descrição"],
            "formato_data": "%d/%m/%Y",
            "separador_decimal": "."
        }
        self.bancos_suportados = list(FORMATOS_BANCOS.keys())
    
    def detectar_banco(self, arquivo_csv=None, df=None, colunas=None):
        """
        Detecta automaticamente o banco baseado nas colunas do CSV
        """
        if colunas is None:
            if df is not None:
                colunas = list(df.columns)
            elif arquivo_csv is not None:
                # Tentar diferentes encodings e separadores
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    for sep in [',', ';', '\t']:
                        try:
                            df_temp = pd.read_csv(arquivo_csv, encoding=encoding, sep=sep, nrows=1)
                            colunas = list(df_temp.columns)
                            break
                        except:
                            continue
                    if colunas:
                        break
            else:
                raise ValueError("Deve fornecer arquivo_csv, df ou colunas")
        
        print(f"🔍 Detectando banco baseado nas colunas: {colunas}")
        
        # Normalizar nomes das colunas para comparação
        colunas_norm = [col.lower().strip() for col in colunas]
        
        # Calcular score de similaridade para cada banco
        scores = {}
        for banco, config in FORMATOS_BANCOS.items():
            colunas_banco = [col.lower() for col in config["colunas"]]
            
            # Contar quantas colunas coincidem
            matches = sum(1 for col in colunas_norm if col in colunas_banco)
            total_banco = len(colunas_banco)
            total_arquivo = len(colunas_norm)
            
            # Score baseado na proporção de matches
            if total_banco > 0:
                score = matches / total_banco
                scores[banco] = score
        
        # Selecionar banco com maior score
        if scores:
            banco_detectado = max(scores.keys(), key=lambda k: scores[k])
            score_max = scores[banco_detectado]
            
            print(f"✅ Banco detectado: {banco_detectado} (score: {score_max:.2f})")
            
            if score_max < 0.5:
                print(f"⚠️ Baixa confiança na detecção. Usando formato genérico.")
                return "generico"
            
            return banco_detectado
        else:
            print(f"❌ Não foi possível detectar o banco. Usando formato genérico.")
            return "generico"
    
    def mapear_colunas(self, colunas, banco_detectado=None):
        """
        Mapeia colunas do arquivo para o formato padrão
        """
        mapeamento = {}
        colunas_norm = [col.lower().strip() for col in colunas]
        
        print(f"🗺️ Mapeando colunas para formato padrão...")
        
        # Mapear Data
        for col_original, col_norm in zip(colunas, colunas_norm):
            if any(alias.lower() in col_norm for alias in MAPEAMENTO_COLUNAS["data_aliases"]):
                mapeamento["Data"] = col_original
                break
        
        # Mapear Descrição
        for col_original, col_norm in zip(colunas, colunas_norm):
            if any(alias.lower() in col_norm for alias in MAPEAMENTO_COLUNAS["descricao_aliases"]):
                mapeamento["Descrição"] = col_original
                break
        
        # Mapear Valor
        for col_original, col_norm in zip(colunas, colunas_norm):
            if any(alias.lower() in col_norm for alias in MAPEAMENTO_COLUNAS["valor_aliases"]):
                mapeamento["Valor"] = col_original
                break
        
        # Mapear Identificador (opcional)
        for col_original, col_norm in zip(colunas, colunas_norm):
            if any(alias.lower() in col_norm for alias in MAPEAMENTO_COLUNAS["id_aliases"]):
                mapeamento["Identificador"] = col_original
                break
        
        # Se não encontrou identificador, criar um
        if "Identificador" not in mapeamento:
            mapeamento["Identificador"] = None
        
        print(f"✅ Mapeamento criado: {mapeamento}")
        return mapeamento
    
    def detectar_formato_data(self, serie_data):
        """
        Detecta automaticamente o formato da data
        """
        # Pegar algumas amostras não-nulas
        amostras = serie_data.dropna().head(10)
        
        for formato in FORMATOS_DATA:
            try:
                # Tentar converter algumas amostras
                sucessos = 0
                for amostra in amostras:
                    try:
                        datetime.strptime(str(amostra), formato)
                        sucessos += 1
                    except:
                        continue
                
                # Se conseguiu converter a maioria, esse é o formato
                if sucessos >= len(amostras) * 0.8:
                    print(f"✅ Formato de data detectado: {formato}")
                    return formato
            except:
                continue
        
        print(f"⚠️ Formato de data não detectado. Usando padrão: %d/%m/%Y")
        return "%d/%m/%Y"
    
    def detectar_separador_decimal(self, serie_valor):
        """
        Detecta se usa vírgula ou ponto como separador decimal
        """
        # Pegar algumas amostras
        amostras = serie_valor.dropna().astype(str).head(20)
        
        tem_virgula = sum(1 for x in amostras if ',' in x and '.' not in x)
        tem_ponto = sum(1 for x in amostras if '.' in x and ',' not in x)
        tem_ambos = sum(1 for x in amostras if ',' in x and '.' in x)
        
        if tem_ambos > 0:
            # Formato brasileiro: 1.234,56
            print("✅ Formato brasileiro detectado (1.234,56)")
            return ","
        elif tem_virgula > tem_ponto:
            print("✅ Separador decimal: vírgula")
            return ","
        else:
            print("✅ Separador decimal: ponto")
            return "."
    
    def normalizar_valor(self, valor_str, separador_decimal):
        """
        Normaliza valor para formato float padrão
        """
        if pd.isna(valor_str):
            return 0.0
        
        valor_str = str(valor_str).strip()
        
        # Remover espaços e caracteres especiais
        valor_str = re.sub(r'[^\d,.\-+]', '', valor_str)
        
        if separador_decimal == ",":
            # Formato brasileiro: 1.234,56 -> 1234.56
            if '.' in valor_str and ',' in valor_str:
                # Tem milhares e decimais
                valor_str = valor_str.replace('.', '').replace(',', '.')
            elif ',' in valor_str:
                # Só decimais
                valor_str = valor_str.replace(',', '.')
        
        try:
            return float(valor_str)
        except:
            return 0.0
    
    def normalizar_data(self, data_str, formato_detectado):
        """
        Normaliza data para formato padrão dd/mm/yyyy
        """
        if pd.isna(data_str):
            return ""
        
        try:
            data_obj = datetime.strptime(str(data_str), formato_detectado)
            return data_obj.strftime("%d/%m/%Y")
        except:
            return str(data_str)
    
    def gerar_identificador(self, index):
        """
        Gera identificador único se não existir
        """
        import uuid
        return str(uuid.uuid4())
    
    def padronizar_csv(self, arquivo_entrada, arquivo_saida=None, banco=None):
        """
        Função principal para padronizar um CSV
        """
        print(f"🔄 Iniciando padronização de: {arquivo_entrada}")
        
        # 1. Detectar encoding e separador
        df = None
        config_leitura = None
        
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            for sep in [',', ';', '\t']:
                try:
                    df = pd.read_csv(arquivo_entrada, encoding=encoding, sep=sep)
                    config_leitura = {'encoding': encoding, 'sep': sep}
                    print(f"✅ Arquivo lido com encoding={encoding}, sep='{sep}'")
                    break
                except:
                    continue
            if df is not None:
                break
        
        if df is None:
            raise ValueError("Não foi possível ler o arquivo CSV")
        
        print(f"📊 Arquivo carregado: {len(df)} linhas, {len(df.columns)} colunas")
        
        # 2. Detectar banco se não especificado
        if banco is None:
            banco = self.detectar_banco(df=df)
        
        # 3. Mapear colunas
        mapeamento = self.mapear_colunas(df.columns, banco)
        
        # Verificar se temos as colunas essenciais
        if "Data" not in mapeamento or "Descrição" not in mapeamento or "Valor" not in mapeamento:
            raise ValueError(f"Colunas essenciais não encontradas. Mapeamento: {mapeamento}")
        
        # 4. Criar DataFrame padronizado
        df_padrao = pd.DataFrame()
        
        # Data
        if mapeamento["Data"]:
            formato_data = self.detectar_formato_data(df[mapeamento["Data"]])
            df_padrao["Data"] = df[mapeamento["Data"]].apply(
                lambda x: self.normalizar_data(x, formato_data)
            )
        
        # Valor
        if mapeamento["Valor"]:
            separador = self.detectar_separador_decimal(df[mapeamento["Valor"]])
            df_padrao["Valor"] = df[mapeamento["Valor"]].apply(
                lambda x: self.normalizar_valor(x, separador)
            )
        
        # Descrição
        if mapeamento["Descrição"]:
            df_padrao["Descrição"] = df[mapeamento["Descrição"]].fillna("Transação")
        
        # Identificador
        if mapeamento["Identificador"] and mapeamento["Identificador"] in df.columns:
            df_padrao["Identificador"] = df[mapeamento["Identificador"]]
        else:
            df_padrao["Identificador"] = [self.gerar_identificador(i) for i in range(len(df))]
        
        # 5. Salvar arquivo padronizado
        if arquivo_saida is None:
            arquivo_saida = arquivo_entrada.replace('.csv', '_padronizado.csv')
        
        df_padrao.to_csv(arquivo_saida, index=False, encoding='utf-8')
        
        print(f"✅ Arquivo padronizado salvo: {arquivo_saida}")
        print(f"📊 Resultado: {len(df_padrao)} transações padronizadas")
        
        # 6. Mostrar amostra
        print(f"\n📋 Amostra do resultado:")
        print(df_padrao.head().to_string(index=False))
        
        return df_padrao, arquivo_saida
    
    def listar_bancos_suportados(self):
        """Lista todos os bancos suportados"""
        print("🏦 Bancos suportados:")
        for i, banco in enumerate(self.bancos_suportados, 1):
            config = FORMATOS_BANCOS[banco]
            print(f"  {i:2d}. {banco.upper()}")
            print(f"      Colunas: {', '.join(config['colunas'])}")
            print(f"      Encoding: {config['encoding']}")
            print()

def exemplo_uso():
    """Exemplo de como usar o padronizador"""
    
    print("🧪 EXEMPLO DE USO DO PADRONIZADOR")
    print("=" * 50)
    
    padronizador = PadronizadorCSV()
    
    # Listar bancos suportados
    padronizador.listar_bancos_suportados()
    
    # Exemplo de detecção automática
    print("🔍 Exemplo de detecção automática:")
    
    # Simular colunas de diferentes bancos
    exemplos_colunas = {
        "Nubank": ["Data", "Valor", "Identificador", "Descrição"],
        "Itaú": ["data", "lancamento", "valor", "saldo"],
        "Bradesco": ["Data", "Histórico", "Valor", "Saldo"],
        "Santander": ["Data", "Descrição", "Valor", "Saldo"]
    }
    
    for banco_real, colunas in exemplos_colunas.items():
        banco_detectado = padronizador.detectar_banco(colunas=colunas)
        print(f"  {banco_real}: {colunas} → {banco_detectado}")
    
    print(f"\n✅ Padronizador pronto para uso!")

if __name__ == "__main__":
    padronizador = PadronizadorCSV()
    # Troque 'bb.csv' pelo nome do arquivo que deseja padronizar
    padronizador.padronizar_csv('bb.csv')


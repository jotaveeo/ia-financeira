import pandas as pd
import numpy as np
import joblib
from scipy.sparse import hstack
from padronizador_csv_universal import PadronizadorCSV
import warnings
warnings.filterwarnings('ignore')

class ClassificadorUniversal:
    """
    Classificador que funciona com CSVs de qualquer banco brasileiro
    Combina padronização automática + modelo de IA treinado
    """
    
    def __init__(self, 
                 modelo_path='modelo_final.pkl',
                 vectorizer_path='vectorizer_final.pkl', 
                 scaler_path='scaler_final.pkl',
                 processador_path='processador_final.pkl'):
        """Inicializa o classificador universal"""
        
        print("🚀 Inicializando Classificador Universal")
        print("=" * 50)
        
        # Carregar padronizador
        self.padronizador = PadronizadorCSV()
        print("✅ Padronizador carregado")
        
        # Carregar modelo de IA (com fallback para processador simples)
        try:
            self.modelo = joblib.load(modelo_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.scaler = joblib.load(scaler_path)
            print("✅ Modelo de IA carregado")
            
            # Tentar carregar processador, se falhar usar processador simples
            try:
                self.processador = joblib.load(processador_path)
                print("✅ Processador de texto carregado")
            except:
                print("⚠️ Processador salvo não encontrado, usando processador simples")
                self.processador = self._criar_processador_simples()
                
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            print("ℹ️ Execute o script de treinamento primeiro")
            raise
    
    def _criar_processador_simples(self):
        """Cria processador de texto simples como fallback"""
        class ProcessadorSimples:
            def __init__(self):
                self.stop_words = {
                    'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'por'
                }
            
            def processar_texto(self, texto):
                import re
                if pd.isna(texto):
                    return 'transacao'
                texto = str(texto).lower()
                texto = re.sub(r'[^a-záéíóúãõâêîôûç\s]', ' ', texto)
                tokens = [t for t in texto.split() if t not in self.stop_words and len(t) > 2]
                return ' '.join(tokens)
        
        return ProcessadorSimples()
    
    def classificar_arquivo(self, arquivo_csv, banco=None, salvar_resultado=True):
        """
        Classifica transações de qualquer banco automaticamente
        
        Args:
            arquivo_csv: Caminho para o arquivo CSV
            banco: Nome do banco (opcional, será detectado automaticamente)
            salvar_resultado: Se deve salvar o resultado em arquivo
            
        Returns:
            DataFrame com transações classificadas
        """
        
        print(f"🔄 Processando arquivo: {arquivo_csv}")
        print("=" * 50)
        
        # 1. Padronizar CSV para formato universal
        print("📋 Etapa 1: Padronização do CSV")
        try:
            df_padronizado, arquivo_padronizado = self.padronizador.padronizar_csv(
                arquivo_csv, banco=banco
            )
            print(f"✅ CSV padronizado com sucesso")
        except Exception as e:
            print(f"❌ Erro na padronização: {e}")
            raise
        
        # 2. Classificar transações com IA
        print(f"\n🤖 Etapa 2: Classificação com IA")
        try:
            df_classificado = self._classificar_transacoes(df_padronizado)
            print(f"✅ Transações classificadas com sucesso")
        except Exception as e:
            print(f"❌ Erro na classificação: {e}")
            raise
        
        # 3. Salvar resultado se solicitado
        if salvar_resultado:
            arquivo_final = arquivo_csv.replace('.csv', '_classificado_final.csv')
            df_classificado.to_csv(arquivo_final, index=False, encoding='utf-8')
            print(f"💾 Resultado salvo em: {arquivo_final}")
        
        # 4. Análise dos resultados
        self._analisar_resultados(df_classificado)
        
        return df_classificado
    
    def _classificar_transacoes(self, df_padronizado):
        """Classifica transações usando o modelo treinado"""
        
        resultados = []
        
        print(f"🔄 Classificando {len(df_padronizado)} transações...")
        
        for idx, row in df_padronizado.iterrows():
            try:
                # Processar texto
                descricao = row.get('Descrição', '')
                texto_processado = self.processador.processar_texto(descricao)
                X_texto = self.vectorizer.transform([texto_processado])
                
                # Features numéricas
                valor = row.get('Valor', 0)
                features_numericas = np.array([[
                    abs(valor),
                    np.log1p(abs(valor)),
                    1 if valor > 0 else 0
                ]])
                features_numericas_norm = self.scaler.transform(features_numericas)
                
                # Combinar features
                X_combined = hstack([X_texto, features_numericas_norm])
                
                # Predizer
                categoria = self.modelo.predict(X_combined)[0]
                
                # Obter confiança se disponível
                if hasattr(self.modelo, 'predict_proba'):
                    probabilidades = self.modelo.predict_proba(X_combined)[0]
                    confianca = max(probabilidades)
                    
                    # Top 3 categorias
                    classes = self.modelo.classes_
                    top_indices = np.argsort(probabilidades)[-3:][::-1]
                    top_categorias = [(classes[i], probabilidades[i]) for i in top_indices]
                else:
                    confianca = 1.0
                    top_categorias = [(categoria, 1.0)]
                
                resultados.append({
                    'categoria': categoria,
                    'confianca': confianca,
                    'top_1': top_categorias[0][0],
                    'top_2': top_categorias[1][0] if len(top_categorias) > 1 else '',
                    'top_3': top_categorias[2][0] if len(top_categorias) > 2 else ''
                })
                
            except Exception as e:
                print(f"⚠️ Erro ao classificar linha {idx}: {e}")
                resultados.append({
                    'categoria': 'Outros',
                    'confianca': 0.0,
                    'top_1': 'Outros',
                    'top_2': '',
                    'top_3': ''
                })
        
        # Adicionar resultados ao DataFrame
        df_resultado = df_padronizado.copy()
        df_resultado['Categoria_IA'] = [r['categoria'] for r in resultados]
        df_resultado['Confianca'] = [r['confianca'] for r in resultados]
        df_resultado['Top_2'] = [r['top_2'] for r in resultados]
        df_resultado['Top_3'] = [r['top_3'] for r in resultados]
        
        return df_resultado
    
    def _analisar_resultados(self, df_resultado):
        """Analisa e apresenta estatísticas dos resultados"""
        
        print(f"\n📊 ANÁLISE DOS RESULTADOS")
        print("=" * 30)
        
        total = len(df_resultado)
        print(f"Total de transações: {total}")
        
        # Análise de confiança
        if 'Confianca' in df_resultado.columns:
            confiancas = df_resultado['Confianca']
            print(f"\n🎯 Análise de Confiança:")
            print(f"  Confiança média: {confiancas.mean():.3f}")
            print(f"  Confiança mediana: {confiancas.median():.3f}")
            
            # Distribuição por faixas
            alta_confianca = (confiancas >= 0.8).sum()
            media_confianca = ((confiancas >= 0.5) & (confiancas < 0.8)).sum()
            baixa_confianca = (confiancas < 0.5).sum()
            
            print(f"  Alta confiança (≥0.8): {alta_confianca} ({alta_confianca/total*100:.1f}%)")
            print(f"  Média confiança (0.5-0.8): {media_confianca} ({media_confianca/total*100:.1f}%)")
            print(f"  Baixa confiança (<0.5): {baixa_confianca} ({baixa_confianca/total*100:.1f}%)")
        
        # Top categorias
        print(f"\n🏆 Top 10 Categorias:")
        top_categorias = df_resultado['Categoria_IA'].value_counts().head(10)
        for categoria, count in top_categorias.items():
            print(f"  {categoria}: {count} ({count/total*100:.1f}%)")
        
        # Transações com baixa confiança
        if 'Confianca' in df_resultado.columns:
            baixa_conf = df_resultado[df_resultado['Confianca'] < 0.5]
            if len(baixa_conf) > 0:
                print(f"\n⚠️ Transações com baixa confiança ({len(baixa_conf)}):")
                print(baixa_conf[['Descrição', 'Valor', 'Categoria_IA', 'Confianca']].head().to_string(index=False))
        
        # Resumo por tipo (receita/despesa)
        receitas = df_resultado[df_resultado['Valor'] > 0]
        despesas = df_resultado[df_resultado['Valor'] < 0]
        
        print(f"\n💰 Resumo Financeiro:")
        print(f"  Receitas: {len(receitas)} transações (R$ {receitas['Valor'].sum():.2f})")
        print(f"  Despesas: {len(despesas)} transações (R$ {abs(despesas['Valor'].sum()):.2f})")
    
    def classificar_transacao_individual(self, descricao, valor=0):
        """Classifica uma transação individual"""
        
        # Criar DataFrame temporário
        df_temp = pd.DataFrame([{
            'Data': '01/01/2025',
            'Valor': valor,
            'Identificador': 'temp',
            'Descrição': descricao
        }])
        
        # Classificar
        df_resultado = self._classificar_transacoes(df_temp)
        
        return {
            'categoria': df_resultado.iloc[0]['Categoria_IA'],
            'confianca': df_resultado.iloc[0]['Confianca'],
            'top_2': df_resultado.iloc[0]['Top_2'],
            'top_3': df_resultado.iloc[0]['Top_3']
        }
    
    def listar_bancos_suportados(self):
        """Lista bancos suportados"""
        return self.padronizador.listar_bancos_suportados()

def exemplo_uso():
    """Exemplo de uso do classificador universal"""
    
    print("🧪 EXEMPLO DE USO - CLASSIFICADOR UNIVERSAL")
    print("=" * 60)
    
    try:
        # Inicializar classificador
        classificador = ClassificadorUniversal()
        
        # Listar bancos suportados
        print("\n🏦 Bancos suportados:")
        classificador.listar_bancos_suportados()
        
        # Exemplo de classificação individual
        print("\n🔍 Exemplo de classificação individual:")
        exemplos = [
            ("Compra no débito - iFood", -45.50),
            ("Transferência recebida - Salário", 3500.00),
            ("Conta de luz Enel", -180.75),
            ("Supermercado Extra", -120.30),
            ("PIX enviado - Uber", -15.90)
        ]
        
        for descricao, valor in exemplos:
            resultado = classificador.classificar_transacao_individual(descricao, valor)
            print(f"  '{descricao}' (R$ {valor})")
            print(f"    → {resultado['categoria']} (confiança: {resultado['confianca']:.3f})")
            print(f"    Alternativas: {resultado['top_2']}, {resultado['top_3']}")
            print()
        
        print("✅ Classificador universal pronto para uso!")
        print("\nPara usar com arquivo CSV:")
        print("  classificador.classificar_arquivo('meu_extrato.csv')")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("ℹ️ Certifique-se de que o modelo foi treinado primeiro")

if __name__ == "__main__":
    exemplo_uso()


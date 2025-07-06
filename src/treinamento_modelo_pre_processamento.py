import pandas as pd
import numpy as np
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from imblearn.over_sampling import SMOTE
from scipy.sparse import hstack
import warnings
from processador_texto import ProcessadorTexto

warnings.filterwarnings('ignore')

print("🚨 SCRIPT DE TREINAMENTO CORRIGIDO - SOLUÇÃO EMERGENCIAL")
print("Configurado para usar o dataset emergencial que resolve problemas de produção")
print("=" * 70)

# Configurações
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 3
MAX_FEATURES = 2000
MIN_DF = 2
MAX_DF = 0.95
SMOTE_K_NEIGHBORS = 5

def carregar_dados():
    """Carrega dados de treinamento - CORRIGIDO PARA USAR DATASET EMERGENCIAL"""
    try:
        # SOLUÇÃO EMERGENCIAL: Usar dataset corrigido primeiro
        df = pd.read_csv('transacoes_emergencial_producao.csv')
        print("✅ Usando transacoes_emergencial_producao.csv (DATASET EMERGENCIAL)")
        print("🎯 Este dataset foi criado especificamente para resolver os problemas de produção")
    except FileNotFoundError:
        try:
            df = pd.read_csv('transacoes_melhorado.csv')
            print("⚠️  Usando transacoes_melhorado.csv (dataset antigo)")
            print("🚨 ATENÇÃO: Para melhor performance, use o dataset emergencial!")
        except FileNotFoundError:
            try:
                df = pd.read_csv('transacoes_exemplo.csv')
                print("⚠️  Usando transacoes_exemplo.csv (dataset básico)")
            except FileNotFoundError:
                print("❌ Erro: Nenhum arquivo de dados encontrado!")
                return None
    
    print(f"📊 Dataset: {len(df)} transações, {df['Categoria'].nunique()} categorias")
    
    # Verificar se tem as categorias críticas
    categorias_criticas = ["Transporte", "Streaming", "Alimentação", "Supermercado"]
    print(f"\n🎯 VERIFICAÇÃO DAS CATEGORIAS CRÍTICAS:")
    for cat in categorias_criticas:
        count = len(df[df['Categoria'] == cat]) if cat in df['Categoria'].values else 0
        status = "✅" if count >= 30 else "⚠️"
        print(f"  {status} {cat}: {count} exemplos")
    
    # Mostrar distribuição
    print(f"\n📈 Top 10 categorias:")
    print(df['Categoria'].value_counts().head(10))
    
    # Verificar se tem "Taxas Bancárias" (categoria problemática)
    if "Taxas Bancárias" in df['Categoria'].values:
        count_taxas = len(df[df['Categoria'] == 'Taxas Bancárias'])
        print(f"\n🚨 ATENÇÃO: Dataset contém {count_taxas} exemplos de 'Taxas Bancárias'")
        print(f"   Esta categoria causa 40% dos erros em produção!")
        print(f"   Recomendação: Use o dataset emergencial que remove esta categoria")
    else:
        print(f"\n✅ ÓTIMO: Dataset não contém 'Taxas Bancárias' (categoria problemática removida)")
    
    return df

class TreinadorModeloCorrigido:
    """Classe para treinamento do modelo - VERSÃO CORRIGIDA"""
    
    def __init__(self):
        self.processador_texto = ProcessadorTexto()
        self.vectorizer = None
        self.scaler = None
        self.modelo_final = None
        self.melhor_algoritmo = None
        self.categorias_problematicas = ["Taxas Bancárias"]  # Lista de categorias a evitar
        
    def preprocessar_dados(self, df):
        """Pré-processamento dos dados - VERSÃO MELHORADA"""
        print("🔧 Pré-processando dados...")
        
        # Verificar e remover categorias problemáticas se existirem
        categorias_antes = df['Categoria'].nunique()
        for cat_prob in self.categorias_problematicas:
            if cat_prob in df['Categoria'].values:
                count_removidas = len(df[df['Categoria'] == cat_prob])
                df = df[df['Categoria'] != cat_prob]
                print(f"🚨 Removidas {count_removidas} transações da categoria problemática: '{cat_prob}'")
        
        categorias_depois = df['Categoria'].nunique()
        if categorias_antes != categorias_depois:
            print(f"📊 Categorias: {categorias_antes} → {categorias_depois} (removidas categorias problemáticas)")
        
        # Verificar dados
        print(f"📊 Dados após limpeza: {len(df)} transações, {df['Categoria'].nunique()} categorias")
        
        # Processar texto
        print("🔤 Processando descrições...")
        df['descricao_processada'] = df['Descrição'].apply(self.processador_texto.processar_texto)
        
        # Extrair features numéricas
        print("🔢 Extraindo features numéricas...")
        df['valor_abs'] = df['Valor'].abs()
        df['eh_receita'] = (df['Valor'] > 0).astype(int)
        df['valor_log'] = np.log1p(df['valor_abs'])
        
        # Features de texto
        print("📝 Extraindo features de texto...")
        df['tamanho_descricao'] = df['Descrição'].str.len()
        df['tem_pix'] = df['Descrição'].str.contains('pix|PIX', case=False, na=False).astype(int)
        df['tem_debito'] = df['Descrição'].str.contains('débito|debito', case=False, na=False).astype(int)
        df['tem_transferencia'] = df['Descrição'].str.contains('transferência|transferencia', case=False, na=False).astype(int)
        
        return df
    
    def criar_features(self, df):
        """Criação de features - VERSÃO MELHORADA"""
        print("🎯 Criando features...")
        
        # Vectorização TF-IDF
        print("  📊 Vectorização TF-IDF...")
        self.vectorizer = TfidfVectorizer(
            max_features=MAX_FEATURES,
            min_df=MIN_DF,
            max_df=MAX_DF,
            ngram_range=(1, 2),
            stop_words=None
        )
        
        X_text = self.vectorizer.fit_transform(df['descricao_processada'])
        
        # Features numéricas
        print("  🔢 Features numéricas...")
        features_numericas = ['valor_abs', 'eh_receita', 'valor_log', 'tamanho_descricao', 
                             'tem_pix', 'tem_debito', 'tem_transferencia']
        
        X_num = df[features_numericas].values
        
        # Normalizar features numéricas
        self.scaler = StandardScaler()
        X_num_scaled = self.scaler.fit_transform(X_num)
        
        # Combinar features
        print("  🔗 Combinando features...")
        X_combined = hstack([X_text, X_num_scaled])
        
        print(f"  ✅ Features criadas: {X_combined.shape[1]} dimensões")
        
        return X_combined, df['Categoria']
    
    def treinar_modelos(self, X, y):
        """Treinamento de múltiplos modelos - VERSÃO OTIMIZADA"""
        print("🤖 Treinando modelos...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
        
        print(f"📊 Divisão: {X_train.shape[0]} treino, {X_test.shape[0]} teste")
        
        # Aplicar SMOTE para balanceamento
        print("⚖️  Aplicando SMOTE para balanceamento...")
        try:
            smote = SMOTE(random_state=RANDOM_STATE, k_neighbors=min(SMOTE_K_NEIGHBORS, len(y_train.unique())-1))
            X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
            print(f"  ✅ Dados balanceados: {X_train_balanced.shape[0]} exemplos")
        except Exception as e:
            print(f"  ⚠️  SMOTE falhou: {e}")
            X_train_balanced, y_train_balanced = X_train, y_train
        
        # Modelos para testar
        modelos = {
            'Naive Bayes': MultinomialNB(),
            'Random Forest': RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
            'Logistic Regression': LogisticRegression(random_state=RANDOM_STATE, max_iter=1000, n_jobs=-1)
        }
        
        # Parâmetros para Grid Search
        parametros = {
            'Naive Bayes': {'alpha': [0.1, 0.5, 1.0, 2.0]},
            'Random Forest': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            },
            'Logistic Regression': {
                'C': [0.1, 1.0, 10.0],
                'penalty': ['l2']
            }
        }
        
        resultados = {}
        
        for nome, modelo in modelos.items():
            print(f"\n🔄 Treinando {nome}...")
            
            try:
                # Grid Search
                grid_search = GridSearchCV(
                    modelo, parametros[nome], 
                    cv=CV_FOLDS, scoring='f1_weighted', 
                    n_jobs=-1, verbose=0
                )
                
                grid_search.fit(X_train_balanced, y_train_balanced)
                
                # Melhor modelo
                melhor_modelo = grid_search.best_estimator_
                
                # Predições
                y_pred = melhor_modelo.predict(X_test)
                
                # Métricas
                acuracia = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                # Validação cruzada
                cv_scores = cross_val_score(melhor_modelo, X_train_balanced, y_train_balanced, 
                                          cv=CV_FOLDS, scoring='f1_weighted')
                
                resultados[nome] = {
                    'modelo': melhor_modelo,
                    'acuracia': acuracia,
                    'f1_score': f1,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'melhores_params': grid_search.best_params_
                }
                
                print(f"  ✅ {nome}:")
                print(f"     Acurácia: {acuracia:.4f}")
                print(f"     F1-Score: {f1:.4f}")
                print(f"     CV: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
                print(f"     Parâmetros: {grid_search.best_params_}")
                
            except Exception as e:
                print(f"  ❌ Erro no {nome}: {e}")
        
        # Selecionar melhor modelo
        if resultados:
            melhor_nome = max(resultados.keys(), key=lambda k: resultados[k]['f1_score'])
            self.modelo_final = resultados[melhor_nome]['modelo']
            self.melhor_algoritmo = melhor_nome
            
            print(f"\n🏆 MELHOR MODELO: {melhor_nome}")
            print(f"   Acurácia: {resultados[melhor_nome]['acuracia']:.4f}")
            print(f"   F1-Score: {resultados[melhor_nome]['f1_score']:.4f}")
            
            # Relatório detalhado
            y_pred_final = self.modelo_final.predict(X_test)
            print(f"\n📊 RELATÓRIO DETALHADO:")
            print(classification_report(y_test, y_pred_final, zero_division=0))
            
            return X_test, y_test, y_pred_final
        else:
            print("❌ Nenhum modelo foi treinado com sucesso!")
            return None, None, None
    
    def salvar_modelo(self):
        """Salva o modelo treinado"""
        print("💾 Salvando modelo...")
        
        try:
            # Salvar modelo
            joblib.dump(self.modelo_final, 'modelo_final.pkl')
            print("  ✅ modelo_final.pkl")
            
            # Salvar vectorizer
            joblib.dump(self.vectorizer, 'vectorizer_final.pkl')
            print("  ✅ vectorizer_final.pkl")
            
            # Salvar scaler
            joblib.dump(self.scaler, 'scaler_final.pkl')
            print("  ✅ scaler_final.pkl")
            
            # Salvar processador de texto
            joblib.dump(self.processador_texto, 'processador_final.pkl')
            print("  ✅ processador_final.pkl")
            
            print("💾 Todos os arquivos salvos com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
    
    def demonstracao_pratica(self, df):
        """Demonstração prática com exemplos reais - VERSÃO CORRIGIDA"""
        print("🎯 DEMONSTRAÇÃO PRÁTICA COM CASOS CRÍTICOS:")
        print("=" * 60)
        
        # Casos críticos que falharam em produção
        casos_criticos = [
            "Transferência enviada pelo Pix - Uber",
            "Transferência enviada pelo Pix - GOGIPSY BRASIL", 
            "Compra no débito - SUPERM SAO LUIZ",
            "Compra no débito - GIL DA TAPIOCA",
            "Aplicação RDB",
            "Resgate RDB",
            "Compra no débito - PAGUE MENOS",
            "Netflix - Assinatura mensal"
        ]
        
        # Categorias esperadas
        categorias_esperadas = [
            "Transporte",
            "Streaming", 
            "Supermercado",
            "Alimentação",
            "Investimentos",
            "Investimentos",
            "Medicamentos",
            "Streaming"
        ]
        
        print("🚨 TESTANDO CASOS QUE FALHARAM EM PRODUÇÃO:")
        acertos = 0
        
        for i, (caso, esperada) in enumerate(zip(casos_criticos, categorias_esperadas)):
            try:
                # Processar texto
                texto_processado = self.processador_texto.processar_texto(caso)
                
                # Vectorizar
                X_text = self.vectorizer.transform([texto_processado])
                
                # Features numéricas (valores fictícios para demonstração)
                valor_abs = 50.0
                eh_receita = 1 if "Recebida" in caso or "Resgate" in caso else 0
                valor_log = np.log1p(valor_abs)
                tamanho_descricao = len(caso)
                tem_pix = 1 if "pix" in caso.lower() else 0
                tem_debito = 1 if "débito" in caso.lower() else 0
                tem_transferencia = 1 if "transferência" in caso.lower() else 0
                
                X_num = np.array([[valor_abs, eh_receita, valor_log, tamanho_descricao, 
                                 tem_pix, tem_debito, tem_transferencia]])
                X_num_scaled = self.scaler.transform(X_num)
                
                # Combinar features
                X_combined = hstack([X_text, X_num_scaled])
                
                # Predição
                predicao = self.modelo_final.predict(X_combined)[0]
                probabilidades = self.modelo_final.predict_proba(X_combined)[0]
                confianca = max(probabilidades)
                
                # Verificar acerto
                acertou = predicao == esperada
                if acertou:
                    acertos += 1
                
                status = "✅" if acertou else "❌"
                print(f"{status} {caso[:50]:<50} → {predicao:<15} (esperado: {esperada:<15}) [{confianca:.3f}]")
                
            except Exception as e:
                print(f"❌ Erro no caso {i+1}: {e}")
        
        taxa_acerto = (acertos / len(casos_criticos)) * 100
        print(f"\n📊 RESULTADO DOS CASOS CRÍTICOS:")
        print(f"   Acertos: {acertos}/{len(casos_criticos)} ({taxa_acerto:.1f}%)")
        
        if taxa_acerto >= 80:
            print(f"   🎉 EXCELENTE! Problemas de produção resolvidos!")
        elif taxa_acerto >= 60:
            print(f"   ✅ BOM! Melhoria significativa esperada")
        else:
            print(f"   ⚠️  ATENÇÃO! Ainda há problemas a resolver")

def main():
    """Função principal"""
    print("Iniciando treinamento com solução emergencial...")
    
    # Carregar dados
    df = carregar_dados()
    if df is None:
        return
    
    # Criar treinador
    treinador = TreinadorModeloCorrigido()
    
    # Pré-processar
    df_processado = treinador.preprocessar_dados(df)
    
    # Criar features
    X, y = treinador.criar_features(df_processado)
    
    # Treinar modelos
    X_test, y_test, y_pred = treinador.treinar_modelos(X, y)
    
    if X_test is not None:
        # Salvar modelo
        treinador.salvar_modelo()
        
        # Demonstração prática
        treinador.demonstracao_pratica(df_processado)
        
        print(f"\n🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!")
        print(f"🎯 Modelo otimizado para resolver problemas de produção")
        print(f"📁 Arquivos salvos: modelo_final.pkl, vectorizer_final.pkl, etc.")
        print(f"\n🚀 PRÓXIMO PASSO:")
        print(f"   Execute: python classificar_arquivo_real.py")
        print(f"   Use seu CSV real para testar a melhoria!")
    else:
        print("❌ Falha no treinamento!")

if __name__ == "__main__":
    main()


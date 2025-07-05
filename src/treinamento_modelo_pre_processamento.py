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

print("=== SCRIPT DE TREINAMENTO MELHORADO ===\n")

# Configurações
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 3
MAX_FEATURES = 2000
MIN_DF = 2
MAX_DF = 0.95
SMOTE_K_NEIGHBORS = 5

def carregar_dados():
    """Carrega dados de treinamento"""
    try:
        df = pd.read_csv('transacoes_melhorado.csv')
        print("✓ Usando transacoes_melhorado.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv('transacoes_exemplo.csv')
            print("✓ Usando transacoes_exemplo.csv")
        except FileNotFoundError:
            print("❌ Erro: Nenhum arquivo de dados encontrado!")
            return None
    
    print(f"📊 Dataset: {len(df)} transações, {df['Categoria'].nunique()} categorias")
    
    # Mostrar distribuição
    print("\n📈 Top 10 categorias:")
    print(df['Categoria'].value_counts().head(10))
    
    return df

def validar_dados(df):
    """Valida e corrige dados"""
    print("\n🔍 Validando dados...")
    
    # Exemplo de validação: garantir que 'Valor' seja numérico
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    
    # Preencher valores ausentes em 'Valor' com a mediana
    mediana_valor = df['Valor'].median()
    df['Valor'].fillna(mediana_valor, inplace=True)
    
    # Remover transações sem categoria
    transacoes_antes = len(df)
    df = df[df['Categoria'].notna()]
    transacoes_depois = len(df)
    
    print(f"✓ Transações removidas (sem categoria): {transacoes_antes - transacoes_depois}")
    
    return df

def extrair_features(df, processador):
    """Extrai features textuais e numéricas"""
    print("\n🔧 Extraindo features...")
    
    # Processar texto
    df['Descrição_Processada'] = df['Descrição'].apply(processador.processar_texto)
    
    # Features de texto com TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=(1, 2),
        min_df=MIN_DF,
        max_df=MAX_DF
    )
    X_texto = vectorizer.fit_transform(df['Descrição_Processada'])
    
    # Features numéricas (normalizadas para valores positivos)
    scaler = MinMaxScaler()  # Usar MinMaxScaler para garantir valores positivos
    features_numericas = np.column_stack([
        df['Valor'].abs(),
        np.log1p(df['Valor'].abs()),
        (df['Valor'] > 0).astype(int)  # É receita?
    ])
    features_numericas_norm = scaler.fit_transform(features_numericas)
    
    # Combinar features
    X_combined = hstack([X_texto, features_numericas_norm])
    
    print(f"✓ Features extraídas: {X_combined.shape}")
    print(f"  - Texto: {X_texto.shape[1]} features")
    print(f"  - Numéricas: {features_numericas_norm.shape[1]} features")
    
    return X_combined, vectorizer, scaler

def treinar_modelos(X_train, y_train, X_test, y_test):
    """Treina e compara modelos"""
    print("\n🤖 TREINANDO MODELOS")
    print("=" * 50)
    
    modelos = {
        'Naive Bayes': MultinomialNB(alpha=1.0),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1),
        'Logistic Regression': LogisticRegression(random_state=RANDOM_STATE, max_iter=1000, n_jobs=-1)
    }
    
    resultados = {}
    
    for nome, modelo in modelos.items():
        print(f"\n🔄 Treinando {nome}...")
        
        try:
            # Validação cruzada
            cv_scores = cross_val_score(modelo, X_train, y_train, cv=CV_FOLDS, scoring='f1_weighted')
            print(f"  📊 CV F1-Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
            # Treinar e avaliar
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_test)
            
            acuracia = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            print(f"  ✅ Acurácia: {acuracia:.4f}")
            print(f"  ✅ F1-Score: {f1:.4f}")
            
            resultados[nome] = {
                'modelo': modelo,
                'acuracia': acuracia,
                'f1': f1,
                'cv_mean': cv_scores.mean()
            }
            
        except Exception as e:
            print(f"  ❌ Erro no {nome}: {str(e)}")
            continue
    
    return resultados

def otimizar_modelo(melhor_modelo, X_train, y_train, nome_modelo):
    """Otimiza hiperparâmetros"""
    print(f"\n⚙️ OTIMIZANDO {nome_modelo}")
    print("=" * 30)
    
    try:
        if isinstance(melhor_modelo, MultinomialNB):
            param_grid = {'alpha': [0.1, 0.5, 1.0, 2.0]}
        elif isinstance(melhor_modelo, RandomForestClassifier):
            param_grid = {
                'n_estimators': [50, 100],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            }
        elif isinstance(melhor_modelo, LogisticRegression):
            param_grid = {'C': [0.1, 1.0, 10.0]}
        else:
            print("⚠️ Otimização não disponível para este modelo")
            return melhor_modelo
        
        grid_search = GridSearchCV(
            melhor_modelo, param_grid, cv=CV_FOLDS, scoring='f1_weighted', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        print(f"✅ Melhores parâmetros: {grid_search.best_params_}")
        print(f"✅ Melhor F1-Score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
        
    except Exception as e:
        print(f"❌ Erro na otimização: {str(e)}")
        return melhor_modelo

def avaliar_final(modelo, X_test, y_test, nome_modelo):
    """Avaliação final detalhada"""
    print(f"\n📋 AVALIAÇÃO FINAL - {nome_modelo}")
    print("=" * 50)
    
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"🎯 Acurácia Final: {acuracia:.4f}")
    print(f"🎯 F1-Score Final: {f1:.4f}")
    
    print(f"\n📊 Relatório Detalhado:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Performance por categoria (top 10)
    print(f"\n🏆 Performance por Categoria (Top 10):")
    categorias_freq = y_test.value_counts().head(10)
    for categoria in categorias_freq.index:
        mask = y_test == categoria
        if mask.sum() > 0:
            acc_cat = accuracy_score(y_test[mask], y_pred[mask])
            print(f"  {categoria}: {acc_cat:.3f} (n={mask.sum()})")

def demonstrar_classificacao(modelo, vectorizer, scaler, processador):
    """Demonstra classificação de exemplos"""
    print(f"\n🧪 DEMONSTRAÇÃO DE CLASSIFICAÇÃO")
    print("=" * 40)
    
    exemplos = [
        "Compra no débito via NuPay - iFood",
        "Transferência Recebida - Salário mensal",
        "Conta de energia elétrica Enel",
        "Supermercado Extra compra",
        "Transferência enviada pelo Pix - Uber",
        "Aplicação RDB",
        "Netflix mensal",
        "Farmácia Drogasil",
        "Posto de gasolina Shell"
    ]
    
    for exemplo in exemplos:
        try:
            # Processar
            texto_proc = processador.processar_texto(exemplo)
            X_texto = vectorizer.transform([texto_proc])
            
            # Features numéricas dummy
            features_num = scaler.transform([[50, np.log1p(50), 0]])
            
            # Combinar
            X_exemplo = hstack([X_texto, features_num])
            
            # Predizer
            categoria = modelo.predict(X_exemplo)[0]
            
            if hasattr(modelo, 'predict_proba'):
                proba = modelo.predict_proba(X_exemplo)[0]
                confianca = max(proba)
                print(f"  '{exemplo}' → {categoria} (confiança: {confianca:.3f})")
            else:
                print(f"  '{exemplo}' → {categoria}")
                
        except Exception as e:
            print(f"  ❌ Erro ao classificar '{exemplo}': {str(e)}")

def salvar_modelo_com_metadados(modelo, vectorizer, scaler, processador, resultados):
    """Salva o modelo e metadados associados"""
    print(f"\n💾 Salvando modelo e metadados...")
    try:
        joblib.dump(modelo, 'modelo_final.pkl')
        joblib.dump(vectorizer, 'vectorizer_final.pkl')
        joblib.dump(scaler, 'scaler_final.pkl')
        joblib.dump(processador, 'processador_final.pkl')
        
        # Salvar resultados de desempenho
        df_resultados = pd.DataFrame(resultados).T
        df_resultados.to_csv('resultados_modelos.csv', index=True)
        
        print("✅ Modelo e metadados salvos com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar modelo/metadados: {str(e)}")

def main():
    """Função principal"""
    
    # 1. Carregar dados
    df = carregar_dados()
    if df is None:
        return None
    
    # 2. Preprocessamento
    processador = ProcessadorTexto()
    X, vectorizer, scaler = extrair_features(df, processador)
    y = df['Categoria']
    
    # 3. Balanceamento
    print(f"\n⚖️ Aplicando SMOTE para balanceamento...")
    try:
        # Ajustar k_neighbors baseado no número mínimo de amostras por classe
        min_samples = y.value_counts().min()
        k_neighbors = min(SMOTE_K_NEIGHBORS, min_samples - 1) if min_samples > 1 else 1
        
        smote = SMOTE(random_state=RANDOM_STATE, k_neighbors=k_neighbors)
        X_balanced, y_balanced = smote.fit_resample(X, y)
        print(f"✅ Dados balanceados: {X_balanced.shape[0]} amostras")
    except Exception as e:
        print(f"⚠️ Erro no SMOTE: {str(e)}. Usando dados originais.")
        X_balanced, y_balanced = X, y
    
    # 4. Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X_balanced, y_balanced, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_balanced
    )
    
    print(f"📊 Divisão dos dados:")
    print(f"  - Treino: {X_train.shape[0]} amostras")
    print(f"  - Teste: {X_test.shape[0]} amostras")
    
    # 5. Treinar modelos
    resultados = treinar_modelos(X_train, y_train, X_test, y_test)
    
    if not resultados:
        print("❌ Nenhum modelo foi treinado com sucesso!")
        return None
    
    # 6. Selecionar melhor modelo
    melhor_nome = max(resultados.keys(), key=lambda k: resultados[k]['f1'])
    melhor_modelo = resultados[melhor_nome]['modelo']
    
    print(f"\n🏆 MELHOR MODELO: {melhor_nome}")
    print(f"  F1-Score: {resultados[melhor_nome]['f1']:.4f}")
    print(f"  Acurácia: {resultados[melhor_nome]['acuracia']:.4f}")
    
    # 7. Otimizar
    modelo_otimizado = otimizar_modelo(melhor_modelo, X_train, y_train, melhor_nome)
    
    # 8. Avaliação final
    avaliar_final(modelo_otimizado, X_test, y_test, melhor_nome)
    
    # 9. Salvar modelo
    salvar_modelo_com_metadados(modelo_otimizado, vectorizer, scaler, processador, resultados)
    
    # 10. Demonstração
    demonstrar_classificacao(modelo_otimizado, vectorizer, scaler, processador)
    
    print(f"\n🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    
    return modelo_otimizado, vectorizer, scaler, processador

if __name__ == "__main__":
    resultado = main()
    if resultado:
        modelo, vectorizer, scaler, processador = resultado
        print("\n✅ Todos os componentes foram salvos e estão prontos para uso!")


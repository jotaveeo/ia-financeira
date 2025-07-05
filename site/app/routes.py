# Arquivo de rotas para o Flask
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import joblib
from app.model import carregar_modelo, carregar_processador, carregar_scaler

main = Blueprint('main', __name__)

# Carregar o modelo e vectorizer
model, vectorizer = carregar_modelo()
processador = carregar_processador()  # Implemente essa função se ainda não existe
scaler = carregar_scaler()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/categorizar', methods=['POST'])
def categorizar():
    # Verificar se o arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    # Carregar o arquivo CSV
    df = pd.read_csv(file)

    # Verificar se a coluna 'Descrição' existe
    if 'Descrição' not in df.columns:
        return jsonify({'error': 'Arquivo não contém a coluna "Descrição"'}), 400

    # Processar as descrições e fazer as previsões
    df['Descrição Processada'] = df['Descrição'].apply(processador.processar_texto)
    X_texto = vectorizer.transform(df['Descrição Processada'])

    # Adicione as features numéricas igual ao treino
    import numpy as np
    features_numericas = np.column_stack([
        df['Valor'].abs(),
        np.log1p(df['Valor'].abs()),
        (df['Valor'] > 0).astype(int)
    ])
    features_numericas_norm = scaler.transform(features_numericas)
    from scipy.sparse import hstack
    X = hstack([X_texto, features_numericas_norm])

    categorias = model.predict(X)

    # Adicionar as categorias ao DataFrame
    df['Categoria Prevista'] = categorias

    return jsonify(df[['Descrição', 'Categoria Prevista']].to_dict(orient='records'))

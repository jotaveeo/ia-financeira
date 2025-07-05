# IA de Categorização de Transações Financeiras

## Visão Geral

Este projeto implementa um pipeline completo de categorização automática de transações financeiras, utilizando machine learning e processamento de linguagem natural (NLP) para classificar receitas e despesas em 72 categorias alinhadas com o frontend do sistema.

- **Geração de dataset sintético realista e balanceado**
- **Pré-processamento robusto de texto e valores**
- **Feature engineering com palavras-chave específicas**
- **Treinamento com modelos de ML (Naive Bayes, Random Forest, Logistic Regression)**
- **Balanceamento com SMOTE (ajustável)**
- **Validação, estatísticas e demonstração de classificação**
- **Pronto para integração com frontend e APIs**

## Estrutura do Projeto

```
IA Categorizacao/
├── src/
│   ├── gera_csv_para_treinamento.py   # Geração do dataset sintético
│   ├── treinamento_modelo_pre_processamento.py  # Pipeline de treino
│   ├── processador_texto.py           # Classe de pré-processamento de texto
│   └── ...                            # Outros utilitários
├── site/                              # App Flask para deploy
│   └── ...
├── transacoes_72_categorias_alinhadas.csv  # Dataset principal
├── resultados_modelos.csv             # Resultados de treino
└── README.md
```

## Como Usar

1. **Gerar o dataset sintético**
   ```bash
   python src/gera_csv_para_treinamento.py
   ```
   O arquivo `transacoes_72_categorias_alinhadas.csv` será criado.

2. **Treinar o modelo**
   - Edite o caminho do dataset em `treinamento_modelo_pre_processamento.py` se necessário.
   - Execute:
   ```bash
   python src/treinamento_modelo_pre_processamento.py
   ```
   Modelos, vetorizador, scaler e processador serão salvos como `.pkl`.

3. **Deploy e API**
   - O diretório `site/` contém um app Flask pronto para servir o modelo treinado.

## Principais Melhorias e Técnicas

- **Cobertura de 72 categorias (13 receitas, 59 despesas)**
- **Exemplos realistas e específicos para evitar confusão entre categorias**
- **Feature engineering: detecção de palavras-chave como 'uber', 'netflix', 'aplicação'**
- **Balanceamento ajustável com SMOTE (k_neighbors=3 recomendado)**
- **Validação e estatísticas detalhadas do dataset**
- **Pronto para expansão: basta adicionar novas categorias/exemplos**

## Dicas e Recomendações

- Sempre utilize o dataset `transacoes_72_categorias_alinhadas.csv` para o melhor desempenho.
- Ajuste o parâmetro `EXEMPLOS_POR_CATEGORIA` para controlar o tamanho do dataset.
- Para evitar overfitting, utilize `SMOTE(random_state=42, k_neighbors=3)`.
- Use a função `extrair_features_especificas` para enriquecer o pipeline com features customizadas.

## Créditos

Desenvolvido por Jotavee e colaboradores. Projeto open-source para automação financeira e IA aplicada.

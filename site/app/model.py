import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from processador_texto import ProcessadorTexto
import joblib

def carregar_modelo():
    model = joblib.load('modelo_final.pkl')
    vectorizer = joblib.load('vectorizer_final.pkl')
    return model, vectorizer

def carregar_processador():
    return joblib.load('processador_final.pkl')

def carregar_scaler():
    return joblib.load('scaler_final.pkl')

import re
import pandas as pd

class ProcessadorTexto:
    """Classe para processamento de texto"""
    def __init__(self):
        self.stop_words = {
            'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'por', 
            'na', 'no', 'ao', 'dos', 'das', 'se', 'que', 'ou', 'mas', 'como', 'mais',
            'muito', 'bem', 'já', 'só', 'ainda', 'também', 'até', 'quando', 'onde'
        }

    def limpar_texto(self, texto):
        if pd.isna(texto):
            return 'transacao'
        texto = str(texto).lower()
        texto = re.sub(r'pix', ' pix ', texto)
        texto = re.sub(r'débito|debito', ' debito ', texto)
        texto = re.sub(r'crédito|credito', ' credito ', texto)
        texto = re.sub(r'[^a-záéíóúãõâêîôûç\s]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()

    def processar_texto(self, texto):
        texto_limpo = self.limpar_texto(texto)
        tokens = texto_limpo.split()
        tokens_filtrados = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        return ' '.join(tokens_filtrados)
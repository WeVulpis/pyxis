from fastapi import FastAPI
import requests
import pandas as pd

app = FastAPI()

# Dataset inicial do Pysis

df = pd.read_csv("data/scores.csv")

# Rota principal
@app.get("/")
def home():
    return {"message": "Pyxis API Online"}

# Consulta de CEP
@app.get("/cep/{cep}")
def buscar_cep(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    return response.json()

# Healthcheck
@app.get("/health")
def health():
    return {"status": "online"}

# Consulta de cidade
@app.get("/cidade/{nome}")
def buscar_cidade(nome: str):
    return {
        "cidade": nome,
        "status": "Mapeamento iniciado"
    }

# Score inteligente usando pandas
@app.get("/score/{cidade}")
def score(cidade: str):

    resultado = df[
        df["cidade"].str.lower() == cidade.lower()
    ]

    if resultado.empty:
        return {"erro": "Cidade não encontrada"}

    score = int(resultado.iloc[0]["score"])

    categoria = "baixo potencial"

    if score >= 90:
        categoria = "altíssimo potencial"

    elif score >= 80:
        categoria = "alto potencial"

    elif score >= 70:
        categoria = "médio potencial"

    return {
        "cidade": cidade,
        "score": score,
        "categoria": categoria
    }
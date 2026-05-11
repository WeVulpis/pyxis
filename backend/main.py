from fastapi import FastAPI
import requests
import pandas as pd

app = FastAPI()

# Dataset inicial do Pyxis
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


# Ranking das cidades por score
@app.get("/ranking")
def ranking():
    df_ordenado = df.sort_values(by="score", ascending=False)

    return df_ordenado.to_dict(orient="records")

@app.get("/insights/{cidade}")
def insights(cidade: str):

    resultado = df[
        df["cidade"].str.lower() == cidade.lower()
    ]

    if resultado.empty:
        return {"erro": "Cidade não encontrada"}

    score = int(resultado.iloc[0]["score"])

    if score >= 90:
        insight = "Região com altíssimo potencial para expansão e operação comercial."
    elif score >= 80:
        insight = "Região com alto potencial e boas oportunidades estratégicas."
    elif score >= 70:
        insight = "Região com potencial intermediário, recomendada para análise complementar."
    else:
        insight = "Região com baixo potencial inicial, exigindo validação adicional."

    return {
        "cidade": cidade,
        "score": score,
        "insight": insight
    }
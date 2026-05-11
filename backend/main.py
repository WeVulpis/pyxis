from math import radians, sin, cos, sqrt, atan2
from fastapi import FastAPI
import requests
import pandas as pd

app = FastAPI()

# Dataset inicial do Pyxis
df = pd.read_csv("data/scores.csv")

pontos = []

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

@app.post("/pontos")
def criar_ponto(ponto: dict):
    novo_ponto = {
        "id": len(pontos) + 1,
        "nome": ponto.get("nome"),
        "tipo": ponto.get("tipo"),
        "endereco": ponto.get("endereco"),
        "latitude": ponto.get("latitude"),
        "longitude": ponto.get("longitude")
    }

    pontos.append(novo_ponto)

    return {
        "mensagem": "Ponto cadastrado com sucesso",
        "ponto": novo_ponto
    }


@app.get("/pontos")
def listar_pontos():
    return {
        "total": len(pontos),
        "pontos": pontos
    }
def calcular_distancia_km(lat1, lon1, lat2, lon2):
    raio_terra_km = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    diferenca_lat = lat2 - lat1
    diferenca_lon = lon2 - lon1

    a = sin(diferenca_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diferenca_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return raio_terra_km * c


@app.post("/distancia")
def calcular_distancia(dados: dict):
    origem = dados.get("origem")
    destino = dados.get("destino")

    distancia = calcular_distancia_km(
        origem["latitude"],
        origem["longitude"],
        destino["latitude"],
        destino["longitude"]
    )

    return {
        "origem": origem,
        "destino": destino,
        "distancia_km": round(distancia, 2)
    }

@app.post("/rota")
def calcular_rota(dados: dict):
    origem = dados.get("origem")

    pontos_calculados = []

    for ponto in pontos:
        distancia = calcular_distancia_km(
            origem["latitude"],
            origem["longitude"],
            ponto["latitude"],
            ponto["longitude"]
        )

        ponto_com_distancia = ponto.copy()
        ponto_com_distancia["distancia_km"] = round(distancia, 2)

        pontos_calculados.append(ponto_com_distancia)

    rota_ordenada = sorted(
        pontos_calculados,
        key=lambda ponto: ponto["distancia_km"]
    )

    return {
        "origem": origem,
        "total_pontos": len(rota_ordenada),
        "rota_sugerida": rota_ordenada
    }
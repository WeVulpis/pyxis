from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Pyxis API Online"}

@app.get("/cep/{cep}")
def buscar_cep(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    return response.json()

@app.get("/health")
def health():
    return {"status": "online"}

@app.get("/cidade/{nome}")
def buscar_cidade(nome: str):
    return {
        "cidade": nome,
        "status": "Mapeamento iniciado"
    }

@app.get("/score/{cidade}")
def score(cidade: str):

    score = 82

    return {
        "cidade": cidade,
        "score": score,
        "categoria": "alto potencial"
    }
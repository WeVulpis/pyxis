import pandas as pd

dados = {
    "cidade": [
        "Ribeirão Preto",
        "São Paulo",
        "Campinas",
        "Sertãozinho"
    ],

    "score": [
        82,
        95,
        88,
        75
    ]
}

df = pd.DataFrame(dados)

print(df)
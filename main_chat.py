import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("API_KEY_OPEN")

modelo = ChatOpenAI(
    model="pt-3.5-turbo",
    temperature=0.5,
    api_key=api_key
)

lista_de_perguntas = [
    "Sugira uma cidade para visitar dado o meu interesse por praias e cultura.",
    "Sugira restaurantes populares",
    "Sugira a melhor época do ano para visitar a cidade sugerida"
    ]

for pergunta in lista_de_perguntas:
    resposta = modelo.invoke(pergunta)
    print("User: ", pergunta)
    print("IA: ", resposta.content, "\n")
    
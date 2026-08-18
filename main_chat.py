import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
api_key = os.getenv("api_key_open_ai")

modelo = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=api_key
)

prompt_sugestao = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um guia de viagem especializado em destinos brasileiros. Apresente-se como Sr. Passeios"),
        ("placeholder", "{historico}"),
        ("human", "{query}")   
    ]
)

cadeia = prompt_sugestao | modelo | StrOutputParser()

lista_de_perguntas = [
    "Sugira uma cidade para visitar dado o meu interesse por praias e cultura.",
    "Qual melhor época do ano para ir?"
    ]

for pergunta in lista_de_perguntas:
    resposta = modelo.invoke(pergunta)
    print("User: ", pergunta, "\n")
    print("IA: ", resposta.content, "\n")
    
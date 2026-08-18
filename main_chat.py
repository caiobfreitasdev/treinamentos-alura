import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

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


memoria = {}
sessao = "aula_langchain_alura"

def historico_por_sessao(sessao : str):
    if sessao not in memoria:
        memoria[sessao] = InMemoryChatMessageHistory()
    return memoria[sessao]

lista_de_perguntas = [
    "Sugira uma cidade para visitar dado o meu interesse por praias e cultura.",
    "Qual melhor época do ano para ir?"
    ]

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,
    get_session_history=historico_por_sessao,
    input_messages_key="query",
    history_messages_key="historico"
)


for pergunta in lista_de_perguntas:
    resposta = cadeia_com_memoria.invoke(
        {
            "query": pergunta
        },
        config={"session_id":sessao}
    )
    print("User: ", pergunta, "\n")
    print("IA: ", resposta, "\n")
    
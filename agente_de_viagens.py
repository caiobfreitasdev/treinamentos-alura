from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import Field, BaseModel
from dotenv import load_dotenv
from langchain.globals import set_debug
import os

set_debug(True) #Faz o debug do langchain ficar ativo, mostrando o que está acontencedo.

load_dotenv()
api_key = os.getenv("API_KEY_OPEN")

class Destino(BaseModel):
    cidade:str = Field("A cidade recomendada para visitar")
    motivo:str = Field("Motivo pelo qual é interessante visitar essa cidade")

class Restaurantes(BaseModel):
    cidade:str = Field("A cidade recomendada para visitar")
    restaurantes:str = Field("Restauntes recomendados na cidade")

parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_restaurantes = JsonOutputParser(pydantic_object=Restaurantes)

prompt_cidade = PromptTemplate(
    template="""
     Sugira uma cidade dado o meu interesse por {interesse}.
    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}
)

prompt_restaurante = PromptTemplate(
    template="""
    Sugira restaurantes populares dado o meu interesse por {cidade}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_restaurantes.get_format_instructions()}
)

prompt_cultural = PromptTemplate(
    template= "Sugira atividades e locais culturais em {cidade}"
)

modelo = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=api_key
)

cadeia_1 = prompt_cidade | modelo | parseador_destino
cadeia_2 = prompt_restaurante | modelo | parseador_restaurantes
cadeia_3 = prompt_cultural | modelo | StrOutputParser()

cadeia = (cadeia_1 | cadeia_2 | cadeia_3)

resposta = cadeia.invoke(
    {
        "interesse" : "praias"
    }
)
print(resposta)

#por causa do STR -> String, não preciso usar o .content, pois já estamos informando que o formato vai ser em string
#invoke isola a construção, e orquestra as construções
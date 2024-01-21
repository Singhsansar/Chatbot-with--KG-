import os
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI

# Set up Neo4j connection
uri = os.getenv('neo4j_uri')
username = os.getenv('neo4j_username')
password = os.getenv('neo4j_password')
graph = Neo4jGraph(url=uri, username=username, password=password)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, top_k=10)

chain = GraphCypherQAChain.from_llm(
    cypher_llm=llm,
    qa_llm=llm,
    graph=graph,
    validate_cypher=True, 
    verbose=True,
)

def get_answer_from_text(question):
    try:
        answer = chain.run(question)
        return answer
    except Exception as e:
        return f"Sorry, I don't know the answer to that question."
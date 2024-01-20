import os 
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer

uri = os.getenv('neo4j_uri')
username = os.getenv('neo4j_username')
password = os.getenv('neo4j_password')

graph = Neo4jGraph(
    url=uri, username=username, password=password
)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0,top_k=5)

# graph = Neo4jGraph(url=uri, username=username, password=password)
# diffbot_api_key = "b90642c9037ee4cbb2959ff03f75d624"
# diffbot_nlp = DiffbotGraphTransformer(diffbot_api_key=diffbot_api_key)


chain = GraphCypherQAChain.from_llm(
    cypher_llm=llm,
    qa_llm=llm,
    graph=graph,
    validate_cypher=True,
    
    verbose=False,
)

 
def get_answer_from_text(question):
    try:  
        answer = chain.run(question)
    except Exception as e:
        answer = f"""Sorry, I don't know the answer to that question."""
    return answer
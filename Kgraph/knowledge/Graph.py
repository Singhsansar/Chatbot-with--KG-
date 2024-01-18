import os 
from neo4j import GraphDatabase
from dotenv import load_dotenv


load_dotenv('.env')
uri = os.getenv('neo4j_uri')
username = os.getenv('neo4j_username')
password = os.getenv('neo4j_password')

driver = GraphDatabase.driver(uri, auth=(username, password))

def insert_into_graph_database(source_id, source_label, target_id, target_label, relationship_type, relationship_weight=1):
    """Inserts nodes and a relationship into the graph database."""
    create_source_node_query = f"MERGE (n:`{source_label}` {{id: $id, label: $label}})"
    create_target_node_query = f"MERGE (n:`{target_label}` {{id: $id, label: $label}})"
    create_relationship_query = (
        f"MATCH (source:`{source_label}` {{id: $source_id}}), (target:`{target_label}` {{id: $target_id}}) "
        f"MERGE (source)-[r:`{relationship_type}` {{label: $label, weight: $weight}}]->(target)")
    
    try:
        with driver.session() as session:
            session.run(create_source_node_query, id=source_id, label=source_label)
            session.run(create_target_node_query, id=target_id, label=target_label)
            session.run(create_relationship_query, source_id=source_id, target_id=target_id, label=relationship_type, weight=relationship_weight)
        print("Nodes and relationship added successfully.")
    except Exception as e:
        print(f"Error during insertion: {e}")


        
def delete_nodes_and_relationships():
    with driver.session() as session:
          session.run("MATCH (n) DETACH DELETE n")
          
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def query_graph_for_answer(user_question):
    """Queries the graph for answers relevant to the user's question."""
    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Split the user's question into words
    question_words = user_question.lower().split()

    # Define a template for the Cypher query
    cypher_query_template = (
        "MATCH (source)-[r]->(target) "
        "WHERE {conditions} "
        "RETURN source.label AS source, type(r) AS relationship, target.label AS target"
    )
    conditions = " OR ".join([f"toLower(source.label) CONTAINS '{word}' OR toLower(target.label) CONTAINS '{word}'" for word in question_words])
    cypher_query = cypher_query_template.format(conditions=conditions)

    with driver.session() as session:
        result = session.run(cypher_query)
        answers = [f"{record['source']} - {record['relationship']} - {record['target']}" for record in result]

        return cypher_query, answers



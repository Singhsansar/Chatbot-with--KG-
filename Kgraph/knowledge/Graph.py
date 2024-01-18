from neo4j import GraphDatabase
uri = "bolt://3.87.189.181:7687"
username = "neo4j"
password = "women-armful-requirement"
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
    uri = "bolt://3.87.189.181:7687"
    username = "neo4j"
    password = "women-armful-requirement"
    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Define a generic Cypher query to match nodes based on labels
    cypher_query = (
        "MATCH (source)-[r]->(target) "
        "WHERE toLower(source.label) = $label OR toLower(target.label) = $label "
        "RETURN source.label AS source, type(r) AS relationship, target.label AS target"
    )

    with driver.session() as session:
        result = session.run(cypher_query, label=user_question.lower())
        answers = [f"{record['source']} - {record['relationship']} - {record['target']}" for record in result]

        return cypher_query, answers

# Example usage:
question = "Who is  also_known_as Siddartha Gautama?"
query, response = query_graph_for_answer(question)
print(f"Generated Cypher Query: {query}")
print(f"Response: {response}")


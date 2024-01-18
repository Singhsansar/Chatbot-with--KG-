from neo4j import GraphDatabase
uri = "bolt://3.87.189.181:7687"
username = "neo4j"
password = "women-armful-requirement"
driver = GraphDatabase.driver(uri, auth=(username, password))

def insert_into_graph_database(source, target, label):
    create_node_query = "CREATE (n:Node {id: $id, label: $label})"

    create_relationship_query = (
        "MATCH (source:Node {id: $source_id}), (target:Node {id: $target_id}) "
        "CREATE (source)-[:RELATIONSHIP {label: $label, weight: 1}]->(target)")
    try:
        with driver.session() as session:
            session.run(create_node_query, id=source, label=label)
            session.run(create_node_query, id=target, label=label)
            session.run(create_relationship_query, source_id=source, target_id=target, label=label)
        print("Nodes and relationship inserted successfully.")
    except Exception as e:
        print(f"Error during insertion: {e}")
   
        
def delete_nodes_and_relationships():
    with driver.session() as session:
          session.run("MATCH (n) DETACH DELETE n")
          
def query_graph_for_answer(user_question):
    cypher_query = (
        "MATCH (source)-[relationship]->(target) "
        "WHERE source.label CONTAINS $label OR target.label CONTAINS $label "
        "RETURN source.label AS source, relationship.label AS relationship, target.label AS target"
    )
    
    try:
        with driver.session() as session:
            result = session.run(cypher_query, label=user_question.lower())
            answers = [record for record in result]
            
            if not answers:
                return "No relevant information found."
            
            response = ""
            for answer in answers:
                response += f"{answer['source']} {answer['relationship']} {answer['target']}\n"
            
            return response.strip()
    except Exception as e:
        return f"Error during query: {e}"

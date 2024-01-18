import json 
from Kgraph.knowledge import Graph


def append_to_json_file(json_data,file='output.json'):
    file_path = file
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        existing_data = []
    new_data = json_data
    existing_data.append(new_data)
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=2)
        
        
def read_json_insert_graph(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        
    for relationships_list in json_data:
        for relationship in relationships_list:
            source = relationship['source']
            label = relationship['label']
            target = relationship['target']
            Graph.insert_into_graph_database(source, target, label)
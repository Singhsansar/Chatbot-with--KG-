import streamlit as st
import pathlib
import time
from Kgraph.knowledge import Graph
from Kgraph.pdfs import read_pdf
from Kgraph.cleaning import nlp_clean
from Kgraph.gemini import geminisetup
from Kgraph.cleaning import save_relation
from Kgraph.knowledge import Graph

def process_user_input(user_input):
    Graph.delete_nodes_and_relationships()
    text = nlp_clean.preprocess(user_input)
    response = geminisetup.get_relationship(text)
    json_data = nlp_clean.clean_text(response)
    save_relation.append_to_json_file(json_data)
    time.sleep(1)
    json_path = pathlib.Path.cwd() / "output.json"
    save_relation.read_json_insert_graph(json_path)
    
def user_input(user_question): 
    #querying the knowledge graph for the answer to the user's question
    answer = Graph.query_graph_for_answer(user_question)
    st.write("Graphs's Reply: ", answer)
    

def main():
    st.set_page_config(page_title="Chat with Knowledge Graph", page_icon="💬", layout="wide")
    st.title("Chat with Knowledge Graph 💬")
    user_question = st.text_input("Ask a Question:")
    if user_question:
        user_input(user_question)


    # Sidebar , for the text and pdfs embeddings 
    with st.sidebar:
        st.title("Menu:")
        st.subheader("User Input Options")
        input_type = st.radio("Choose Input Type:", ["Text Input", "Upload PDF"])
        if input_type == "Text Input":
            user_input_text = st.text_area("Enter your message:", height=200, max_chars=None, key=None)
        elif input_type == "Upload PDF":
            pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                if input_type == "Text Input":
                    process_user_input(user_input_text)  
                elif input_type == "Upload PDF":
                    st.write("PDF processing logic goes here")
                    text = read_pdf.get_pdf_text(pdf_file)
                    process_user_input(user_input_text)
                st.success("Done")

if __name__ == "__main__":
    main()

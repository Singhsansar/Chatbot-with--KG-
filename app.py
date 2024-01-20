import os 
import time
import pathlib
import streamlit as st
from Kgraph.chatbot import bot
from Kgraph.knowledge import Graph
from Kgraph.pdfs import read_pdf
from Kgraph.cleaning import nlp_clean
from Kgraph.gemini import geminisetup
from Kgraph.cleaning import save_relation
from Kgraph.knowledge import Graph

def process_user_input(user_input):
    Graph.delete_nodes_and_relationships()  
    temp = ''
    tokens = user_input.split()
    for i in range(0,len(tokens),500):
        temp = tokens[i:i+500]
        sentence = ' '.join(temp)
    text = nlp_clean.preprocess(sentence)
    response = geminisetup.get_relationship(text)
    json_data = nlp_clean.clean_text(response)
    save_relation.append_to_json_file(json_data)
    time.sleep(1)
    json_path = pathlib.Path.cwd() / "output.json"
    save_relation.read_json_insert_graph(json_path)
    if os.path.exists(json_path):
     os.remove(json_path)
    

def user_input(user_question): 
    answer = bot.get_answer_from_text(user_question)
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
                    st.write("PDF processing...")
                    text = read_pdf.get_pdf_text(pdf_file)
                    process_user_input(user_input_text)
                st.success("Done")

if __name__ == "__main__":
    main()

import streamlit as st

def make_and_train_knwoledge_graph():
    #make the knowledge graph
    #train the knowledge graph
    #return the knowledge graph
    return None
def make_query_to_knowledge_graph():
    #make query to knowledge graph
    #return the response from knowledge graph
    return None
def preprocess_user_input(user_input):
    #preprocess the user input
    #return the preprocessed user input
    return None


def main():
    st.set_page_config(page_title="Chat with Knowledge Graph", page_icon="💬", layout="wide")
    st.title("Chat with Knowledge Graph 💬")
    user_input = st.text_input("You:", "")
    if st.button("Submit"):
        
        #call the function to generate the resonse from knolewdge graph
        response = f"Knowledge Graph Response: {user_input}"
        st.text_area("Chat:", value=f"You: {user_input}\nKnowledge Graph: {response}", height=200, max_chars=None, key=None)

if __name__ == "__main__":
    main()

import os
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

load_dotenv('.env')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_relationship(processed_tokens):
    prompt = f"""
    Analyze the given information to extract relationships from the processed tokens. Your objective is to identify causal, semantic, and temporal connections \n
    between two objects and even dates. Generate the output in JSON format, specifying entities as source, target, and label for each relationship. Ensure that the \n 
    representations reflect causal connections, exhibit semantic coherence, and consider temporal aspects to avoid unnecessary repetition. \n
    Provide the output in JSON format for ease of constructing a knowledge graph. Focus on capturing relationships that form meaningful sentences when considering source + label + target. Feel free to introduce additional relationships if needed.\n
    All the captured relationships should be authentic, meaningful, and in the format of source, target, label. Ensure that all words returned are lemmatized.\n
    Do not capture incorrect or illegal relationships and make the proper use of the words to define relationship.\n
    \n\n
    Information:
    {processed_tokens}
    """
    response = model.generate_content(prompt,
                                  generation_config=genai.types.GenerationConfig(
                                  temperature=0.3))
    data = response.text
    return data
    
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
    prompt = f"""Given the provided information in processed tokens, your task is to analyze and extract relationships. Focus on identifying causal, semantic, and temporal connections between objects and dates. Present the output in JSON format, specifying entities as source, target, and label for each relationship. Emphasize meaningful sentences in the representation, ensuring lemmatization and coherence. Introduce additional relationships if necessary, but maintain authenticity and relevance. Avoid capturing incorrect or illegal relationships, and use underscores to connect multiple words in labels or node connections. Your final output should be a JSON format highlighting the source, target, and label of each captured relationship.\n
     make the Nodes as short as possible, don't use long sentences as nodes, unless very necessary , capture all possible relationship with repeatation\n
    \n\n
    Information:
    {processed_tokens}
    """
    response = model.generate_content(prompt,
                                  generation_config=genai.types.GenerationConfig(
                                  temperature=1))
    data = response.text
    return data
    
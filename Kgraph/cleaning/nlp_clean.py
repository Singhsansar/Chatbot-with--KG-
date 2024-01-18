import nltk
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def preprocess(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stemmed_tokens = [PorterStemmer().stem(token.lower()) for token in tokens if token.lower() not in stop_words]
    tokens =  stemmed_tokens
    sentence = ' '.join(tokens)
    return sentence

def clean_text(result):
    start_pos = result.find('[')
    end_pos = result.rfind(']')

    if start_pos != -1 and end_pos != -1:
        json_string = result[start_pos:end_pos + 1]

        try:
            json_data = json.loads(json_string)
            return json_data
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print("No valid JSON data found.")
        return None
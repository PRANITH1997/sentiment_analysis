from flask import Flask, request, render_template
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

nltk.download('wordnet')
nltk.download('stopwords')

app = Flask(__name__)

def remove_repetitive_emojis(x):
    emoji_pattern = re.compile(r"(\s*)([\U0001F600-\U0001F64F"
                               r"\U0001F300-\U0001F5FF"
                               r"\U0001F680-\U0001F6FF"
                               r"\U0001F1E0-\U0001F1FF"
                               r"\U00002500-\U00002BEF"
                               r"\U00002702-\U000027B0"
                               r"\U000024C2-\U0001F251"
                               r"\U0001f926-\U0001f937"
                               r"\U00010000-\U0010ffff"
                               r"\u2640-\u2642"
                               r"\u2600-\u2B55"
                               r"\u200d"
                               r"\u23cf"
                               r"\u23e9"
                               r"\u231a"
                               r"\ufe0f"
                               r"\u3030"
                               r"]{1,})", flags=re.UNICODE)
    cleaned_text = emoji_pattern.sub(r'\1', x)
    return cleaned_text

def preprocess_text(raw_text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    sentence = re.sub(r'[^\w\s]|[\d]', " ", raw_text)
    sentence = sentence.lower()
    tokens = sentence.split()
    clean_tokens = [t for t in tokens if t not in stop_words]
    clean_tokens = [lemmatizer.lemmatize(word) for word in clean_tokens]
    clean_tokens = " ".join(clean_tokens)
    return clean_tokens

model = joblib.load("model/best_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    cleaned_text = preprocess_text(text)
    cleaned_text = remove_repetitive_emojis(cleaned_text) 
    prediction = model.predict([cleaned_text])[0]
    sentiment = 'Positive' if prediction == 0 else 'Negative'

    return render_template('result.html', text=text, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
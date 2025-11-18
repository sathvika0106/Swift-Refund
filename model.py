import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Load the dataset
df = pd.read_csv('C:/Users/DELL/Desktop/Nlp/text_emotion_data.csv')

# Initialize the Sentiment Intensity Analyzer
sid = SentimentIntensityAnalyzer()

# Define a function to analyze text and determine refund eligibility
def analyze_text_for_refund(text):
    # Tokenize and clean the text
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Analyze sentiment
    sentiment_score = sid.polarity_scores(' '.join(filtered_tokens))
    compound_score = sentiment_score['compound']
    
    # Determine sentiment category based on compound score
    if compound_score >= 0.05:
        sentiment = 'happy'
    elif compound_score <= -0.05:
        sentiment = 'angry'
    elif compound_score < 0.05 and compound_score > -0.05:
        sentiment = 'disappointed'
    else:
        sentiment = 'unhappy'

    # Check if sentiment matches any refund-related sentiment in the dataset
    if sentiment in df['sentiment'].values:
        return sentiment
    else:
        return 'neutral'  # or some default value


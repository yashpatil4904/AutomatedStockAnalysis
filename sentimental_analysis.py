import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon (only needed once)
nltk.download('vader_lexicon')

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Load CSV file
df = pd.read_csv(r"C:\Users\Asawari\PycharmProjects\venv310\stockTracker\merged_x.csv")

# Print column names to debug issues
print("Columns in CSV:", df.columns)

# Try different possible column names
tweet_column = None
for col in df.columns:
    if "tweet" in col.lower():  # Case-insensitive check for "tweet"
        tweet_column = col
        break

if not tweet_column:
    raise KeyError("No column related to 'Tweet' found in the CSV!")

# Function to classify sentiment
def get_sentiment(text):
    sentiment_score = sia.polarity_scores(str(text))["compound"]
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
df["Sentiment"] = df[tweet_column].apply(get_sentiment)

# Save the new CSV
df.to_csv("stock_sentiment.csv", index=False)

print("Sentiment analysis complete! Check 'stock_sentiment.csv'.")



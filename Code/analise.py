import pandas as pd
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer




df = pd.read_csv('/Users/naveenbighan/Desktop/Googlemaps/Master/Master_file.csv')

print(df.head())



df['Review'] = df['Review'].astype(str)  
df['Review'] = df['Review'].fillna(' ')


def get_sentiment(review):
    analysis = TextBlob(review)
    
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    
    else:
        return 'Negative'
    
    
df['Sentiment'] = df['Review'].apply(get_sentiment)

print(df[['Company name', 'Review', 'Sentiment']].head())
sentiment_by_company = df.groupby('Company name')['Sentiment'].value_counts(normalize=True).unstack()*100


print(sentiment_by_company)
sentiment_by_company.plot(kind='bar', stacked=True, figsize=(10, 7))

plt.title('Sentiment Analysis by Company')
plt.xlabel('Company Name')
plt.ylabel('Percentage of Reviews')
plt.legend(title='Sentiment')
plt.tight_layout()
plt.show()


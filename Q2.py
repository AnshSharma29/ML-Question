import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import matplotlib.pyplot as plt
from IPython.display import display
import plotly.graph_objects as go



# Load the JSON file
with open('news.article.json', encoding='utf-8') as f:
    articles = json.load(f)

# Preprocessing
stop_words = set(stopwords.words('english'))
for article in articles:
    if 'text' in article:
        article['text'] = ' '.join([word for word in word_tokenize(article['text'].lower()) if word not in stop_words])

# Event Extraction
relevant_articles = []
for article in articles:
    if 'text' in article and 'Israel-Hamas war' in article['text']:
        relevant_articles.append(article)

print(f"Number of relevant articles: {len(relevant_articles)}")

# Extract Dates and Events
dates_events = {}
for article in relevant_articles:
    if 'text' in article:
        for sentence in article['text'].split('.'):
            if 'date' in sentence:
                try:
                    date = datetime.strptime(sentence.split(' ')[0], '%d %B %Y')
                    event = ' '.join(sentence.split(' ')[1:])
                    if date not in dates_events:
                        dates_events[date] = []
                    dates_events[date].append(event)
                    print(f"Extracted date: {date}, event: {event}")
                except ValueError:
                    print(f"Invalid date format in sentence: {sentence}")

print(f"Dates and events: {dates_events}")

# Timeline Creation
timeline = {}
for date, events in dates_events.items():
    timeline[date] = events

print(f"Timeline: {timeline}")

# Plot the Timeline
plt.figure(figsize=(10, 6))
plt.plot(list(timeline.keys()), [len(events) for events in timeline.values()])
plt.xlabel('Date')
plt.ylabel('Number of Events')
plt.title('Israel-Hamas War Timeline')
plt.show()

# Create a timeline
fig = go.Figure(data=[go.Scatter(x=list(timeline.keys()), y=[len(events) for events in timeline.values()])])
fig.update_layout(title='Israel-Hamas War Timeline', xaxis_title='Date', yaxis_title='Number of Events')
fig.show()

# Print the timeline
with open('timeline.txt', 'w') as f:
    for date, events in timeline.items():
        f.write(f'{date}: {", ".join(events)}\n')
from flask import Flask, jsonify, request, render_template
import json
import numpy as np
import pickle
import urllib.request
import os

# Load the datasets
with open('user_topics.json', 'r') as f:
    user_topics = json.load(f)

with open('content.json', 'r') as f:
    content = json.load(f)

# Convert user_topics list to a dictionary, converting user_id to a string
user_topics_dict = {str(user["user_id"]): user["last_topics"] for user in user_topics}

# Load the pre-trained model from the pickle file

model_path = "sentence_transformer_model.pkl"
if not os.path.exists(model_path):
    print("Downloading model...")
    url = "YOUR_DIRECT_DOWNLOAD_LINK"  # Replace with your Google Drive direct link
    urllib.request.urlretrieve(url, model_path)

with open(model_path, 'rb') as f:
    model = pickle.load(f)


app = Flask(__name__)

# Custom cosine similarity function
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# Pre-compute embeddings for content
content_embeddings = []
for card in content:
    combined_text = f"{card['category']} {card['title']} {card['description']}"
    embedding = model.encode(combined_text)  # Assuming encode outputs a numpy array
    content_embeddings.append((embedding, card))

@app.route('/')
def home():
    return render_template('index.html', users=user_topics_dict.keys())

@app.route('/recommend/<user_id>')
def recommend(user_id):
    last_topics = user_topics_dict.get(user_id)  # No need to convert user_id here; it's already a string
    if not last_topics:
        return jsonify({'error': f'No topics found for user {user_id}'})

    # Compute embedding for user's last topics
    user_embedding = model.encode(' '.join(last_topics))  # Assuming encode outputs a numpy array

    # Compute similarities
    similarities = [
        (cosine_similarity(user_embedding, content_embedding), card)
        for content_embedding, card in content_embeddings
    ]

    # Sort by similarity
    similarities = sorted(similarities, key=lambda x: x[0], reverse=True)

    # Select top 5 cards
    top_cards = [card for _, card in similarities[:5]]
    return jsonify(top_cards)

if __name__ == '__main__':
    app.run(debug=True)

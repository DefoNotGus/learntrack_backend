from flask import Flask, jsonify, request, render_template
import json
import numpy as np
import pickle
import urllib.request
import os

# Load the pre-trained model
model_path = "sentence_transformer_model.pkl"
if not os.path.exists(model_path):
    print("Downloading model...")
    url = "https://drive.google.com/uc?id=1MoC1dGshzHVuiNE1Bdo_JJzoJzvkW9JM" 
    urllib.request.urlretrieve(url, model_path)

with open(model_path, 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def home():
    # Check if the user requested JSON response
    if request.args.get('json') == 'true':
        return jsonify({"message": "Welcome to the LearnTrack API!"})

    # Otherwise, serve the HTML file
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Retrieve JSON data from the request
        data = request.json
        user_topics = data.get('user_topics')  # List of user's last studied topics
        content = data.get('content')  # List of content to recommend from

        if not user_topics or not content:
            return jsonify({"error": "Missing user_topics or content in the request"}), 400

        # Compute embedding for user's topics
        user_embedding = model.encode(' '.join(user_topics), convert_to_tensor=True)

        # Pre-compute embeddings for the content
        content_embeddings = [
            (model.encode(f"{card['category']} {card['title']} {card['description']}", convert_to_tensor=True), card)
            for card in content
        ]

        # Compute similarities and sort by relevance
        similarities = [
            (np.inner(user_embedding, content_embedding).item(), card)
            for content_embedding, card in content_embeddings
        ]
        similarities = sorted(similarities, key=lambda x: x[0], reverse=True)

        # Return the top 5 recommendations
        top_recommendations = [card for _, card in similarities[:5]]
        return jsonify(top_recommendations)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

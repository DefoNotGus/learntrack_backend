# create_model.py
from sentence_transformers import SentenceTransformer
import pickle

# Create the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Save the model as a pickle file
with open('sentence_transformer_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as sentence_transformer_model.pkl")

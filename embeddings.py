# embeddings.py
import pickle
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Create a directory for caching embeddings if it doesn't exist.
EMBEDDINGS_DIR = Path("embeddings_cache")
EMBEDDINGS_DIR.mkdir(exist_ok=True)

# Load the pre-trained model (this might take a moment on first load).
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')


def cache_embedding(email, resume_text):
    """
    Caches and returns the embedding for a given resume text based on the candidate's email.
    If the embedding exists, it is loaded from disk.
    """
    embedding_file = EMBEDDINGS_DIR / f"{email}.pkl"
    if embedding_file.exists():
        with open(embedding_file, "rb") as f:
            return pickle.load(f)
    else:
        embedding = model.encode(resume_text, convert_to_tensor=True)
        with open(embedding_file, "wb") as f:
            pickle.dump(embedding, f)
        return embedding


def get_cached_embeddings(resumes_df):
    """
    Iterates over a DataFrame of resumes and returns a list of cached embeddings.
    Assumes the DataFrame has 'email' and 'resume_text' columns.
    """
    embeddings = []
    for idx, row in resumes_df.iterrows():
        embedding = cache_embedding(row['email'], row['resume_text'])
        embeddings.append(embedding)
    return embeddings


def match_job_description(filtered_resumes, job_description, threshold=0.3):
    """
    Matches the job description with stored resume texts by computing cosine similarity.
    Returns a DataFrame of candidates with a similarity score above the threshold.
    """
    if filtered_resumes.empty:
        return pd.DataFrame()

    # Compute the embedding for the job description once.
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    cached_embeddings = get_cached_embeddings(filtered_resumes)

    cosine_scores = []
    for emb in cached_embeddings:
        score = util.cos_sim(job_embedding, emb).item()
        cosine_scores.append(score)

    filtered_resumes['Similarity Score'] = cosine_scores
    return filtered_resumes[filtered_resumes['Similarity Score'] >= threshold][
        ['name', 'email', 'Similarity Score', 'resume_link', 'location']]

"""
Handles model inference by using the trained model to generate chatbot responses.
"""

import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def run_inference(pickled_model: bytes, input_text: str) -> str:
    """
    Runs inference on the input text using the provided pickled model.
    
    The function calculates the cosine similarity between the input and the pre-trained
    questions, returning the answer corresponding to the most similar question.
    
    Args:
        pickled_model (bytes): The pickled model containing the vectorizer and FAQ data.
        input_text (str): The user's input text.
    
    Returns:
        str: The chatbot's response.
    
    Raises:
        Exception: If inference fails.
    """
    try:
        model = pickle.loads(pickled_model)
        vectorizer = model["vectorizer"]
        questions = model["questions"]
        answers = model["answers"]
        
        input_vector = vectorizer.transform([input_text])
        questions_vector = vectorizer.transform(questions)
        similarities = cosine_similarity(input_vector, questions_vector)
        
        max_index = int(np.argmax(similarities))
        return answers[max_index]
    except Exception as e:
        raise Exception(f"Inference error: {e}")

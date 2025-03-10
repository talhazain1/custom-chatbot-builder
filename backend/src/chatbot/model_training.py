"""
Trains a simple chatbot model using the provided knowledge base data and configuration.
For demonstration purposes, this example uses a TF-IDF vectorizer.
"""

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def train_model(knowledge_base: dict, configuration: dict) -> bytes:
    """
    Trains a model based on the FAQs in the knowledge base and dynamic configuration.

    The function expects the knowledge base to have a key "faqs" which is a list of
    dictionaries containing "question" and "answer" keys.
    
    The configuration dictionary can include keys like 'purpose', 'goal', and 'role'
    which you can use to adjust the training process.
    
    Args:
        knowledge_base (dict): The preprocessed knowledge base.
        configuration (dict): Chatbot configuration containing keys such as 'purpose',
                              'goal', and 'role' to influence training.
    
    Returns:
        bytes: A pickled model containing the vectorizer, training data, and configuration.
    
    Raises:
        Exception: If training fails due to missing data or other errors.
    """
    try:
        # Extract dynamic parameters
        purpose = configuration.get("purpose", "default")
        goal = configuration.get("goal", "default")
        role = configuration.get("role", "default")
        
        # Log the configuration details for debugging/training purposes
        print(f"Training chatbot for purpose: {purpose}, goal: {goal}, role: {role}")
        
        # Extract FAQs from the knowledge base
        faqs = knowledge_base.get("faqs", [])
        if not faqs:
            raise ValueError("Knowledge base must contain a 'faqs' list with at least one FAQ.")
        
        questions = [faq['question'] for faq in faqs if 'question' in faq and 'answer' in faq]
        answers = [faq['answer'] for faq in faqs if 'question' in faq and 'answer' in faq]
        
        if not questions or not answers:
            raise ValueError("FAQs must include both 'question' and 'answer' entries.")
        
        # Create and fit a TF-IDF vectorizer on the FAQ questions
        vectorizer = TfidfVectorizer()
        vectorizer.fit(questions)
        
        # Create a simple model structure including dynamic parameters
        model = {
            "vectorizer": vectorizer,
            "questions": questions,
            "answers": answers,
            "purpose": purpose,
            "goal": goal,
            "role": role
        }
        pickled_model = pickle.dumps(model)
        return pickled_model
    except Exception as e:
        raise Exception(f"Error training model: {e}")

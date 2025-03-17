# model_inference_openai.py

import os
import json
import openai

# Ensure your OpenAI API key is set in the environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

def run_inference_openai(chatbot_config, query):
    """
    Runs inference using the OpenAI API by constructing a prompt that includes
    dynamic parameters and a few-shot example based on the FAQ knowledge base.

    Args:
        chatbot_config: A ChatbotConfig model instance containing attributes such as
                        purpose, goal, role, configuration, and knowledge_base.
        query (str): The user's input question.
    
    Returns:
        str: The generated chatbot response.
    """
    # Retrieve dynamic parameters from the chatbot configuration
    purpose = chatbot_config.purpose or "general customer support"
    goal = chatbot_config.goal or "provide accurate and helpful answers"
    role = chatbot_config.role or "assistant"
    configuration = chatbot_config.configuration or {}
    knowledge_base = chatbot_config.knowledge_base or {}

    # Build few-shot examples from the FAQ knowledge base (if available)
    few_shot_examples = ""
    if "faqs" in knowledge_base and isinstance(knowledge_base["faqs"], list):
        # Pick the first 3 examples for brevity
        examples = knowledge_base["faqs"][:3]
        few_shot_examples = "\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in examples])
        few_shot_examples = "Here are some examples from your knowledge base:\n" + few_shot_examples + "\n\n"

    # Construct the system prompt
    system_prompt = (
        f"You are a chatbot designed for {purpose}. "
        f"Your goal is to {goal}, and you act as a {role}. "
        "Use the following context to answer user questions accurately:\n\n"
        f"{few_shot_examples}"
    )

    # Combine the user query into the conversation
    user_message = f"User question: {query}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].message["content"].strip()
        return answer
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")

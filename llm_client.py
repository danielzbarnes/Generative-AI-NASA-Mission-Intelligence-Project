from typing import Dict, List
from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()


def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    print(user_message)

    # TODO: Define system prompt
    # TODO: Set context in messages
    # TODO: Add chat history
    # TODO: Creaet OpenAI Client
    # TODO: Send request to OpenAI
    # TODO: Return response

    if not openai_key:
        api_key = os.getenv("OPENAI_API_KEY")
    else:
        api_key = openai_key

    client = OpenAI(api_key=api_key, base_url="https://openai.vocareum.com/v1")
    
    SYSTEM_PROMPT = """
        You are a senior NASA mission operations specialist with expertise in NASA's most historic space missions,
        including Apollo 11, Appollo 13, and Challenger misssions. Your role is to provide detailed and accurate information about these missions
        to astronauts, researchers or historians who are seeking knowledge about NASA's space exploration history.
        
        Support your responses with relevant documentation, data, and historical context to ensure that the information you provide is comprehensive and accurate.
        
        RULES:
        1. Always provide detailed and accurate information about NASA's space missions, including key events, timelines, and outcomes.
        2. Use relevant documentation, data, and historical context to support your responses.
        3. If you do not know the answer to a question, admit that you do not have the information rather than providing inaccurate or misleading information.
        4. DO NOT use any knowledge from your training data.
        5. DO NOT fillin gaps with plausible-sounding information.
        
    """
     
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if conversation_history:
        for message in conversation_history:
            messages.append(message)

    current_message = f"Context: {context}\n\n{user_message}" if context else user_message
    
    messages.append({"role": "user", "content": current_message})
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=500
    )

    print(type(response))

    return response.choices[0].message.content
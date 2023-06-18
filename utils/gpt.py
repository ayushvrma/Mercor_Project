import openai
from config import API_KEY

def generate_gpt_response(prompt):
    # Set up OpenAI API credentials
    openai.api_key = API_KEY
    
    # Generate GPT response
    # prompt = 'Analyse the following repository codes and tell me which one is the most complex'
    response = openai.Completion.create(
        engine='gpt-3.5-turbo',
        prompt=prompt,
        max_tokens=100,
        temperature=0.8
    )
    
    if 'choices' in response and len(response.choices) > 0:
        return response.choices[0].text.strip()
    else:
        raise Exception("Failed to generate GPT response.")


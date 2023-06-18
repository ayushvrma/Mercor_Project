import openai
from config import API_KEY
import re

def generate_gpt_response(prompt):
    # Set up OpenAI API credentials
    openai.api_key = API_KEY
    
    response = openai.Completion.create(
        engine='gpt-3.5-turbo',
        prompt=prompt,
        max_tokens=4096,
        temperature=0.8
    )
    
    if 'choices' in response and len(response.choices) > 0:
        score, reason = info_extractor(response.choices[0].text.strip())
        return score, reason
    else:
        raise Exception("Failed to generate GPT response.")

def info_extractor(text):
    lines = text.split('\n')
    score_line = lines[0].strip()
    score_match = re.search(r'\d+', score_line)
    if score_match:
        score = int(score_match.group())
    else:
        score = None

    # Remove the first line to get the reason
    reason = '\n'.join(lines[1:]).strip()

    return score, reason

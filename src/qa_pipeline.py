import openai
import yaml
import logging
import time
from openai import OpenAI


logger = logging.getLogger(__name__)

def get_openai_config():
    try:
        with open("config/openai.yml", 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading OpenAI config: {e}")
        raise

config = get_openai_config()

def create_openai_client(retries=3, delay=5):
    openai.api_key = config['api_key']
    for attempt in range(retries):
        try:
            openai.Engine.list()  # Try an API call to verify the key
            logger.info("Connected to OpenAI")
            return
        except Exception as e:
            logger.error(f"OpenAI connection attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("All attempts to connect to OpenAI failed")

#create_openai_client()

def answer_question(question, context):
    try:
        '''response = openai.Completion.create(
            engine="davinci",
            prompt=f"Context: {context}\nQuestion: {question}\nAnswer:",
            max_tokens=150
        )
        return response.choices[0].text.strip()'''
        client_instance = OpenAI(api_key=config['api_key'])
        
        response = client_instance.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide the answer of the question from the documents you are trained on. Try to generate the detailed answer"},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
  
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {e}")
        raise


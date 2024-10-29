import requests
import json
import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not found. Please set GEMINI_API_KEY in your .env file.")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

logging.basicConfig(filename='gemini_api.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def send_prompt(prompt, max_tokens=50, temperature=0.7, top_p=1.0):
    conf = {
        'max_output_tokens': max_tokens,
        'temperature': temperature,
        'top_p': top_p
    }
    try:
        response = model.generate_content(
            prompt,
            generation_config=conf
        )
        return response.text if response else None
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None


def main():
    while True:
        prompt = input("Enter your prompt (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        max_tokens = input("Enter max tokens (default 50): ")
        max_tokens = int(max_tokens) if max_tokens else 50

        temperature = input("Enter temperature (default 0.7): ")
        temperature = float(temperature) if temperature else 0.7

        top_p = input("Enter top_p (default 1.0): ")
        top_p = float(top_p) if top_p else 1.0

        response = send_prompt(prompt, max_tokens, temperature, top_p)
        if response:
            print("Response from Gemini LLM:")
            print(response)
        else:
            print("Failed to get a response. Check the logs for more details.")


if __name__ == "__main__":
    main()

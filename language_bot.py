import os
import openai


# TODO later remove and replace with key from UI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

class LanguageBot:

    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.model = "gpt-3.5-turbo"

    def get_prompt(self, language, level):
        return f'''
        Act as an expert {language} language teacher. Use friendly tone.
        You will be having conversation with user who knows {language} in {level} level.
        Ask him various questions in {language}. 
        When he respondes with errors, add comment in english with correct sentence.
        Write your response and corrections in following format:
        *In first line: write your responses in {language}
        *In second line: write dashed lines
        *In third line: write your comments and error corrections in english or mention that all is correct

        Now start conversation by saying hello in {language} and ask first question.
        '''
    

    def get_answer(self, conversation):
        messages = [{"role": m["role"], "content": m["content"]} for m in conversation]
        gpt_respone= self.client.chat.completions.create(
            model= self.model, 
            messages=messages, 
            stream=True
        )

        full_response = ""
        for response in gpt_respone:
            full_response += (response.choices[0].delta.content or "")

        return full_response

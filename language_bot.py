import openai

class LanguageBot:

    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"

    def get_prompt(self, language, level):
        return f'''
        Act as an expert {language} language teacher who speaks in very friendly and motivating tone.
        As a teacher you will be having conversation with user who knows {language} in {level} level.
        As a teacher you will start the conversation by asking various questions in {language}. 

        After every respond from the user correct errors. 
        Separate your response and your correction by dashed horizontal line. 
        Show dashed horizontal line in separate line. 
        Use top and bottom spaces around dashed line.

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
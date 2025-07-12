
import openai                    # to use chatGPT llm (it is a product of the openai company)
import os
from dotenv import load_dotenv   # to read environment params
import json


class ChatGPT_llm:
    def __init__(self):
        load_dotenv()
        self.openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_weather_intent(self, user_input: str) -> dict:
        """
        This method sends a messages to GPT and asks: “Please turn user's question into a structured JSON.”
        Then we will send this structured json to the open weather site

        This is called prompt engineering - teaching the model how to respond
        I tell the model that the response must be in this format
        by indicating the format I help GPT to avoid adding of the text like: "sure, here is the result ...."

        :param user_input: str
        :return: an answer in json format
        """

        prompt = """
                    You are a smart weather assistant. Extract information from user input and return JSON like:
                    {
                      "city": "City Name",
                      "intent": "current_weather" or "forecast",
                      "range": "today", "tomorrow", "week"
                    }
                    Respond with ONLY the JSON.
                """
        # list messages contain 2 items, each one is dict

        # 'messages' define a conversation between user and chatGPT.
        # In conversation each line is said by user / chatGPT and has content
        # system message - defines chatGPT role - what to do with user's question (defined by 'prompt')
        # user message - defines user's request (what user actually asks chatGPT to do)

        # by using method .create(...) we call openAI
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                temperature=0, # 0 means: "Be very exact. Do not be creative. Just give me exactly what I asked." Dont be friendly and tell me stories
                                                           # format - in which i wish to get the users's request (user_input)
                                                messages=[{"role":   "system",
                                                           "content": prompt},
                                                           # user's question (in plain text, this is actually what we ask) - that i ask to structure according to given format
                                                          {"role":   "user",
                                                           "content": user_input}
                                                         ]
                                               )

        content = response.choices[0].message.content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("⚠️ Couldn't understand GPT response.")
            return {}
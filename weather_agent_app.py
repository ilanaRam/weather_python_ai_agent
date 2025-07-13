from src.voice import Voice
from src.weather_agent import Weather_Agent
from src.llm import ChatGPT_llm

def weather_agent():
    voice_obj = Voice()
    weather_obj = Weather_Agent()
    gpt_obj = ChatGPT_llm()

    # get user's plain text request about the weather
    voice_obj.produce_voice(my_text="Enter your question about the weather: ")
    user_plain_input_text = input("Enter your question about the weather: ")

    # get user's formated text request about the weather
    formated_user_weather_intent = gpt_obj.get_user_intent_about_weather(user_plain_input_text)
    if not formated_user_weather_intent:
        print("❌ Sorry, I didn’t understand your request.")
        return

    # extract city & intent, from the user's formated request text
    city = formated_user_weather_intent.get("city")
    weather_intent = formated_user_weather_intent.get("intent")

    if not city or not weather_intent:
        print("❌ Sorry, I didn’t understand city / intent")
        return
    # apply weather obj to get weather for city
    if weather_intent == "current_weather":
        print(weather_obj.get_current_weather(city))
    # apply weather obj to get forcast for city
    elif weather_intent == "forcast":
        print(weather_obj.get_forcast(city))
    else:
        print("❌ Sorry, I couldn't determine what you want.")





if __name__ == "__main__":
    weather_agent()
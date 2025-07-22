from src.voice import Voice
from src.weather_agent import Weather_Agent
from src.llm import ChatGPT_llm

def weather_agent():
    voice_obj = Voice()
    weather_obj = Weather_Agent()
    gpt_obj = ChatGPT_llm()

    # get user's plain text request about the weather
    voice_obj.produce_voice(my_text="Enter your question about the weather ")
    user_plain_input_text = voice_obj.get_voice()

    # get user's formated text request about the weather
    user_formated_weather_intent = gpt_obj.get_user_intent_about_weather(user_plain_input_text)
    if not user_formated_weather_intent:
        print("❌ Sorry, I didn’t understand your request, I finish.")
        return

    # extract city & intent, from the user's formated request text
    city = user_formated_weather_intent.get("city")
    weather_intent = user_formated_weather_intent.get("intent")

    if not city:
        voice_obj.produce_voice(my_text="❌ Sorry, I didn’t understand the city, I quit")
        return
    if not weather_intent:
        voice_obj.produce_voice(my_text="❌ Sorry, I didn’t understand the intent, I quit")
        return

    print(f"Both city ({city}) and weather_intent ({weather_intent} were received from user")
    # apply weather obj to get weather for city
    if weather_intent == "current_weather":
        current_weather_res = weather_obj.get_current_weather(city)
        voice_obj.produce_voice(my_text=f"The current weather for city {city}. is: {current_weather_res}")
    # apply weather obj to get forcast for city
    elif weather_intent == "forcast":
        forcast = weather_obj.get_forcast(city)
        voice_obj.produce_voice(my_text=f"The forcast for city {city} is: {forcast}")
    else:
        print("❌ Sorry, I couldn't understand your weather intent")





if __name__ == "__main__":
    weather_agent()
from src.voice import Voice
from src.weather_agent import Weather_Agent


def main():
    voice_obj = Voice()
    weather_obj = Weather_Agent()

    voice_obj.produce_voice(my_text="Enter your question about the weather: ")
    request = input("Enter your question about the weather: ")

    # add here LLM model to extract the name of the city
    # if city is  part of the request call the weather method
    city = request
    weather_obj.get_weather(city)


if __name__ == "__main__":
    main()
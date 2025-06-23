from src.voice import Voice
from src.weather_agent import Weather_Agent


def main():
    voice_obj = Voice()
    weather_obj = Weather_Agent()

    voice_obj.set_voice(True)
    voice_obj.make_voice(my_text="Enter the city")
    city = input("Enter a city name: ")
    weather_obj.get_weather(city, voice_obj)


if __name__ == "__main__":
    main()
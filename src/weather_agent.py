import requests # for using API and by api GET to read a weather per city from the site
import pyttsx3  # for voice answering
from pathlib import Path
import os
import yaml

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def speak(text, if_to_speak = False):
    if if_to_speak:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

def get_weather_params_by_city(city_name, key):
    params = {
        "q": city_name,
        "appid": key,
        "units": "metric"
    }
    return params

def get_api_key(key_file):
    with open(key_file, "r") as key_yaml_file:
        content = yaml.safe_load(key_yaml_file)
        key = content["API_KEY"]
        print(f"API_Key is: {key}")
    return key

def _find_full_file_path(my_curr_path, desired_file):
    for dirpath, _, filenames in os.walk(my_curr_path):  #
        if desired_file in filenames:
            full_file_path = Path(str(os.path.join(dirpath, desired_file)))  # Return full path if found
            return full_file_path
    return None  # Return None if not found

def main():
    speak("Enter the city",True)
    city = input("Enter a city name: ")

    key_file = _find_full_file_path(Path.cwd().parent, "key.yaml")
    if not key_file:
        raise FileExistsError
    print(f"Loading key file from: {key_file}")

    key = get_api_key(key_file)
    params = get_weather_params_by_city(city,key)

    # here I use simply the REST API: GET to request a data from a site, using api this site supplies
    response = requests.get(BASE_URL,
                            params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        text = f"\n🌤️ Weather in {city}:"  # this Sun behind clouds is emojy: \U0001F324
        print(text)
        speak(text, True)

        text = f"   Temperature: {temperature}°C"
        print(text)
        speak(text)

        text = f"   Description: {description}"
        print(text)
        speak(text)
    else:
        text = "\n❌ Couldn't find the city. Please check the name and try again."
        print(text)
        speak("\n❌ Couldn't find the city. Please check the name and try again.")

if __name__ == "__main__":
    main()
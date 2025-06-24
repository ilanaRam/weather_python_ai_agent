import requests # for using API and by api GET to read a weather per city from the site
from pathlib import Path
import os
import yaml
from src.voice import Voice # to convert text to speach



class Weather_Agent:
    def __init__(self):
        self.base_url = None
        self.api_key = None
        self.init()

    def init(self):
        configs_file = self._find_full_file_path(Path.cwd().parent, "configs.yaml")
        if not configs_file:
            raise FileExistsError
        print(f"\nLoading configs file from: {configs_file}")
        with open(configs_file, "r") as configs_yaml_file:
            content = yaml.safe_load(configs_yaml_file)
            self.base_url = content["BASE_URL"]
            print(f"Base URL is: {self.base_url}")

        key_file = self._find_full_file_path(Path.cwd().parent, "key.yaml")
        if not key_file:
            raise FileExistsError
        print(f"\nLoading key file from: {key_file}\n")
        with open(key_file, "r") as key_yaml_file:
            content = yaml.safe_load(key_yaml_file)
            self.api_key = content["API_KEY"]
            print(f"API_Key is: {self.api_key}")

    def _get_weather_params_by_city(self, city_name):
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }
        return params

    def _find_full_file_path(self, my_curr_path, desired_file):
        for dirpath, _, filenames in os.walk(my_curr_path):  #
            if desired_file in filenames:
                full_file_path = Path(str(os.path.join(dirpath, desired_file)))  # Return full path if found
                return full_file_path
        return None  # Return None if not found

    def get_weather(self,desired_city):
        voice_obj = Voice()
        params = self._get_weather_params_by_city(city_name=desired_city)
        # here I use simply the REST API: GET to request a data from a site, using api this site supplies
        response = requests.get(self.base_url,
                                params=params)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]

            text = f"\nWeather in {desired_city}:"  # this Sun behind clouds is emojy: \U0001F324
            print(text)
            voice_obj.produce_voice(my_text=text)

            text = f"   Temperature: {temperature}°C"
            print(text)
            voice_obj.produce_voice(my_text=text)

            text = f"   Description: {description}"
            print(text)
            voice_obj.produce_voice(my_text=text)
        else:
            text = "\n❌ Couldn't find the city. Please enter correct name and try again."
            print(text)
            voice_obj.produce_voice(my_text="\n❌ Couldn't find the city. Please check the name and try again.")
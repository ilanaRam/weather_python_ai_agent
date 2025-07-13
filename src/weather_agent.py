import requests # for using API and by api GET to read a weather per city from the site
from pathlib import Path
import os
import yaml
from src.voice import Voice # to convert text to speach



class Weather_Agent:
    def __init__(self):
        self.open_weather_url = None
        self.open_weather_forcast_url = None
        self.open_weather_api_key = None
        self.init()

    def init(self):
        configs_file = self._find_full_file_path(Path.cwd().parent, "configs.yaml")
        if not configs_file:
            raise FileExistsError
        print(f"\nLoading configs file from: {configs_file}")
        with open(configs_file, "r") as configs_yaml_file:
            content = yaml.safe_load(configs_yaml_file)

            self.open_weather_url = content["OPEN_WEATHER_URL"]
            print(f"Weather URL is: {self.open_weather_url}")

            self.open_weather_forcast_url = content["OPEN_WEATHER_FORCAST_URL"]
            print(f"Forcasr URL is: {self.open_weather_forcast_url}")

        key_file = self._find_full_file_path(Path.cwd().parent, "key.yaml")
        if not key_file:
            raise FileExistsError
        print(f"\nLoading key file from: {key_file}\n")
        with open(key_file, "r") as key_yaml_file:
            content = yaml.safe_load(key_yaml_file)
            self.open_weather_api_key = content["OPEN_WEATHER_API_KEY"]
            print(f"API_Key is: {self.open_weather_api_key}")

    def _get_weather_params_by_city(self, city_name):
        params = {
            "q": city_name,
            "appid": self.open_weather_api_key,
            "units": "metric"
        }
        return params

    def _find_full_file_path(self, my_curr_path, desired_file):
        for dirpath, _, filenames in os.walk(my_curr_path):  #
            if desired_file in filenames:
                full_file_path = Path(str(os.path.join(dirpath, desired_file)))  # Return full path if found
                return full_file_path
        return None  # Return None if not found

    def get_current_weather(self, desired_city) -> str:
        voice_obj = Voice()
        params = self._get_weather_params_by_city(city_name=desired_city)

        # here I use simply the REST API: GET to request a data from a site, using api this site supplies
        response = requests.get(self.open_weather_url,
                                params=params)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]

            reply = f"\nCurrent weather in {desired_city} is TEMPERATURE: {temperature}, DESCRIPTION: {description}"  # this Sun behind clouds is emojy: \U0001F324
            return reply
        else:
            reply = "\n❌ Couldn't find the city. Please enter correct name and try again."
            return reply

    def get_forcast(self, desired_city: str) -> str:
        params = self._get_weather_params_by_city(city_name=desired_city)

        res = requests.get(self.open_weather_forcast_url,
                           params=params)
        if res.status_code == 200:
            data = res.json()
            forecasts = data["list"][:3]  # Show 3 upcoming entries
            reply = f"📅 Forecast for {desired_city}:\n"
            for entry in forecasts:
                time = entry["dt_txt"]
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]
                reply += f"{time}: {temp}°C, {desc}\n"
            return reply
        else:
            return f"❌ Could not find forecast for {desired_city}."
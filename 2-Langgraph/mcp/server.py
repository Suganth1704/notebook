import json
import requests
import langcodes
from mcp.server.fastmcp import FastMCP

import os
from dotenv import load_dotenv
load_dotenv()

DEEPL_API_KEY=os.getenv("DEEPL_API_KEY")

mcp = FastMCP("Utility server")

@mcp.tool()
def hello(name:str) -> str:
    """Say hello."""
    return f"Hello {name}"

@mcp.tool()
def add(expression:str) -> int:
    """Evaluate mathematical expressions"""
    return str(eval(expression))

def get_coordinates(city:str) -> dict:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    resp = requests.get(url=url)
    resp_dict = json.loads(resp.text)
    for d in resp_dict.get("results"):
        if d.get('name').lower() == city.lower():
            print("City found..")
            return d

@mcp.tool(name="weather_tool", description="Gives the weather details of the city")
def get_weather_details(city:str) -> str:
    geocoding_dict = get_coordinates(city=city)
    url = "https://api.open-meteo.com/v1/forecast"
    if geocoding_dict:
        params = {
            "latitude": geocoding_dict["latitude"],
            "longitude": geocoding_dict["longitude"],
            "current": "temperature_2m,wind_speed_10m"
            }
        data = requests.get(url, params=params).json()
        return f"Weather data: {data['current']}"

def get_lang_code(target_lang:str) -> str | None:
    '''Sometime the Model it passing the target_lang as fullname of 
    language (Tamil) sometimes it passes shotform (ta) we want only shortfrom
    for the API payload'''
    try:
        print(f"Passed Arg : {target_lang}")
        target_lang = langcodes.find(target_lang).language.upper()
        print(target_lang)
        return target_lang
    except Exception as ex:
        return None

@mcp.tool(name="translator", description="Translate the given text")
def translate(text:str, target_lang:str) -> str:
    try:
        print(text)
        print(type(text))
        target_lang_code = get_lang_code(target_lang=target_lang)
        target_lang = target_lang_code if  target_lang_code else target_lang
        url = "https://api-free.deepl.com/v2/translate"
        headers = {"Content-Type":"application/json", 
                "Authorization":f"DeepL-Auth-Key {DEEPL_API_KEY}"}
        payload = {"text":[text], "target_lang":target_lang}
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            resp_dict = json.loads(resp.text)
            print(resp)
            return resp_dict['translations'][0]['text']
        else:
            raise Exception(f'Request was not successful {resp._content}')
    except Exception as ex:
        print(ex)

   

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http")
import json
import requests
import langcodes
from mcp.server.fastmcp import FastMCP

import pandas as pd

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

BASE_DIR = os.getcwd()
LANG_DIR = os.path.dirname(BASE_DIR)
PARENT_DIR = os.path.dirname(LANG_DIR)
DATA_CLN_DIR = os.path.join(PARENT_DIR, 'data', 'data_cleaning')

def read_csv(csv_file_name:str):
    csv_file = os.path.join(DATA_CLN_DIR, csv_file_name)
    df = pd.read_csv(csv_file)
    return df

@mcp.tool(name="data_profiler", description="Reads a CSV file from the specified file path, loads its contents into a pandas DataFrame, and generates a data quality report containing key profiling metrics and potential data quality issues.")
def profile_data(csv_file_name:str) -> dict:
    df = read_csv(csv_file_name)
    quality_report = {
        "total_records" : len(df),
        "duplicate_rows": df.duplicated().sum(),
        "missing_values" : df.isnull().sum().to_dict(),
        "schema" : df.dtypes.astype(str).to_dict()
    }
    return quality_report

   

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http")
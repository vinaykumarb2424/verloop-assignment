"""
You have to create an API endpoint, which returns Weather data
related corresponding to a city name

When a city is passed in the body, the corresponding current weather, latitude and longitude
are returned in the response. The format in which the response is returned is dictated by the
`output_format` flag, the options for this flag are “json” or “xml”.

If the output flag is set to json the response from the API should be in json format and if the flag is
set to xml the response should be in xml format.


Response JSON
{
“Weather” : “20 C”,
“Latitude” : “12.9716”,
“Longitude” : “77.5946”,
“City” : “Bangalore India”
}

Response XML:
<?xml version="1.0" encoding="UTF-8" ?>
<root>
<Temperature>24.0</Temperature>
<City>Bangalore</City>
<Latitude>12.98</Latitude>
<Longitude>77.58</Longitude>
</root>



You can use this API key to access the API
`31371bc5c3msh34f399b07961d46p192883jsn2ba7562e3194`
"""
import os

from flask import Flask, request, Response, jsonify
import requests
import dicttoxml
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/get_current_weather', methods=['POST'])
def get_current_weather():
    try:
        requested_data = request.get_json()
        # print(requested_data)
        querystring = {'q': requested_data['city']}
        key = os.environ.get("API_KEY")
        # print(key)
        headers = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        response = requests.get(url, headers=headers, params=querystring)
        response_data = {}
        response_keys = ("Weather", "Latitude", "Longitude", "City")
        if response.status_code == 200:
            data = response.json()
            location = data['location']
            response_data.setdefault('Weather', data['current']['temp_c'])
            response_data.setdefault('Latitude', location['lat'])
            response_data.setdefault('Longitude', location['lon'])
            response_data.setdefault('City', f"{location['name']} {location['country']}")
            if requested_data['output_format'] == 'json':
                return response_data
            elif requested_data['output_format'] == 'xml':
                xml_string = dicttoxml.dicttoxml(response_data, custom_root='root', ids=False)
                xml_string = xml_string.decode('utf-8')
                return xml_string
    except Exception as ex:
        return {"status_code": response.status_code, "error": ex}


if __name__ == '__main__':
    app.run(debug=True)

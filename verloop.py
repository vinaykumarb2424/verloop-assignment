
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

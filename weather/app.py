from flask import Flask, render_template, request
from weather import main as get_weather, get_five_day_forecast
from weather import api_key

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error_message = None
    forecast_data = None
    city = ""
    state = ""
    country = "US"

    if request.method == 'POST':
        city = request.form.get('cityName', "")
        state = request.form.get('stateName', "")
        country = request.form.get('countryName', "US").upper()

        if city and country:
            data, forecast_data = get_weather(city, state, country)
            if data is None:
                error_message = "Location not found. Please check your input."

    return render_template('index.html', data=data, error_message=error_message, forecast_data=forecast_data, city_name=city, state_name=state, country_name=country)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
from auth import auth_bp
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.register_blueprint(auth_bp)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["crop_recommendation"]
collection = db["crops"]

# Home after login
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect('/login')

# Root -> main form
@app.route('/')
def homes():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html')

# Predict crop from form input
@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect('/login')

    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        pH = float(request.form['pH'])
        rainfall = float(request.form['rainfall'])

        print(f"User Inputs: N={N}, P={P}, K={K}, Temp={temperature}, Humidity={humidity}, pH={pH}, Rainfall={rainfall}")

        # Find a matching crop in MongoDB
        crop_data = collection.find_one({
            "N": {"$gte": N - 10, "$lte": N + 10},
            "P": {"$gte": P - 10, "$lte": P + 10},
            "K": {"$gte": K - 10, "$lte": K + 10},
            "temperature": {"$gte": temperature - 5, "$lte": temperature + 5},
            "humidity": {"$gte": humidity - 5, "$lte": humidity + 5},
            "ph": {"$gte": pH - 1, "$lte": pH + 1},
            "rainfall": {"$gte": rainfall - 50, "$lte": rainfall + 50}
        })

        predicted_crop = crop_data["label"] if crop_data else "No matching crop found"

        # Fetch weather and recommend based on that
        city = "Mumbai"  # Default city or get from user input if needed
        weather_data = get_weather(city)
        recommended_crops = recommend_crops_based_on_weather(weather_data) if weather_data else []

        return render_template('result.html',
                               predicted_crop=predicted_crop,
                               N=N, P=P, K=K,
                               weather_data=weather_data,
                               recommended_crops=recommended_crops,
                               city=city)
    except Exception as e:
        return render_template('result.html', error=str(e))

# Real-time weather crop prediction form
@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return render_template('weather_form.html', error="Please enter a city")

    weather_data = get_weather(city)

    if weather_data:
        # MongoDB-driven recommendations
        recommended_crops = recommend_crops_based_on_weather(weather_data)
        return render_template('weather_form.html',
                               weather_data=weather_data,
                               recommended_crops=recommended_crops,
                               city=city)
    else:
        return render_template('weather_form.html',
                               error="Weather data not available for this location.")

# Fetch weather data using OpenWeatherMap API
def get_weather(city):
    api_key = 'b490b7f6e8225ba54750a81eb6a8f7f1'  # Replace with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
            return weather_data
    except Exception as e:
        print(f"Error fetching weather: {e}")
    return None

# Suggest crops based on current weather
def recommend_crops_based_on_weather(weather_data):
    temperature = weather_data['temperature']
    humidity = weather_data['humidity']
    description = weather_data['description'].lower()

    crops = []
    if temperature > 20 and humidity > 50:
        crops.append("Rice")
    if temperature > 30 and humidity < 60:
        crops.append("Wheat")
    if "clear sky" in description:
        crops.append("Tomato")
    elif "rain" in description:
        crops.append("Potato")

    return crops

if __name__ == '__main__':
    app.run(debug=True, port=5001)

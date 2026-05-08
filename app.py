from flask import Flask, request, jsonify
import pickle
import requests
import numpy as np
from sklearn.preprocessing import LabelEncoder
import datetime

# =============================================
#   SMART IoT WEATHER STATION - Flask Server
# =============================================

app = Flask(__name__)

# ── Load ML model once at startup ──
with open("weather_model.pkl", "rb") as f:
    model = pickle.load(f)

# ── Config ──
API_KEY = "YOUR_API_KEY_HERE"
CITY    = "Bhavnagar"

# ── Label Encoder for weather conditions ──
le = LabelEncoder()
le.fit([
    "clear sky",
    "light rain",
    "broken clouds",
    "few clouds",
    "scattered clouds",
    "overcast clouds",
    "moderate rain"
])

# ── DHT11 data storage (updated by NodeMCU) ──
dht_data = {
    "temp":       None,
    "humidity":   None,
    "updated_at": None
}

# ==============================================
#   ROUTE 1: NodeMCU sends DHT11 data here
# ==============================================
@app.route("/update", methods=["POST"])
def update():
    global dht_data
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    dht_data["temp"]       = data.get("temperature")
    dht_data["humidity"]   = data.get("humidity")
    dht_data["updated_at"] = datetime.datetime.now().strftime("%H:%M:%S")

    print(f"✅ DHT11 → Temp: {dht_data['temp']}°C  |  Humidity: {dht_data['humidity']}%")
    return jsonify({"status": "ok"})


# ==============================================
#   ROUTE 2: Get raw DHT11 data as JSON
# ==============================================
@app.route("/dht")
def dht():
    return jsonify(dht_data)


# ==============================================
#   ROUTE 3: Main Dashboard
# ==============================================
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        data        = requests.get(url, timeout=5).json()
        temp        = data["main"]["temp"]
        humidity    = data["main"]["humidity"]
        windspeed   = data["wind"]["speed"]
        description = data["weather"][0]["description"]
        hour        = datetime.datetime.now().hour
        return temp, humidity, windspeed, description, hour
    except Exception as e:
        print("API Error:", e)
        return None


@app.route("/")
def home():
    result = get_weather()

    if result is None:
        return "<h1>⚠️ Weather API Error! Check internet connection.</h1>"

    temp, humidity, windspeed, description, hour = result

    # Encode weather description safely
    try:
        desc_encoded = le.transform([description])[0]
    except:
        desc_encoded = 0  # unknown condition → default

    # ML Prediction
    features       = np.array([[temp, humidity, windspeed, hour, desc_encoded]])
    predicted_temp = model.predict(features)[0]

    # Weather emoji
    if temp >= 37:   emoji = "🔥"
    elif temp <= 24: emoji = "❄️"
    else:            emoji = "🌤️"

    # DHT11 section HTML
    if dht_data["temp"] is not None:
        dht_section = f"""
            <div class="dht-box">
                <p class="dht-title">🌡️ DHT11 — Real Sensor</p>
                <p>🌡️ Real Temp: <strong>{dht_data['temp']}°C</strong></p>
                <p>💧 Real Humidity: <strong>{dht_data['humidity']}%</strong></p>
                <p class="last-update">Last update: {dht_data['updated_at']}</p>
            </div>
        """
    else:
        dht_section = """
            <div class="dht-box waiting">
                <p>⏳ Waiting for NodeMCU...</p>
                <p class="last-update">Make sure NodeMCU is powered and on same WiFi</p>
            </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="15">
        <title>Smart Weather Station</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}

            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background: #1a1a2e;
                color: white;
                padding: 40px 20px;
            }}

            .card {{
                background: #16213e;
                padding: 30px 25px;
                border-radius: 18px;
                display: inline-block;
                min-width: 320px;
                max-width: 420px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            }}

            h1 {{ color: #e94560; font-size: 24px; margin-bottom: 20px; }}

            .temp {{ font-size: 56px; font-weight: bold; margin: 10px 0 5px; }}

            .label {{ color: #888; font-size: 13px; margin-bottom: 15px; }}

            .info p {{ margin: 7px 0; font-size: 16px; }}

            hr {{ border: none; border-top: 1px solid #2a2a4a; margin: 20px 0; }}

            .dht-box {{
                background: #0f3460;
                border-radius: 12px;
                padding: 15px;
                margin: 10px 0;
            }}

            .dht-box.waiting {{ background: #1a1a3e; }}

            .dht-title {{
                color: #00d4aa;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }}

            .dht-box p {{ margin: 6px 0; font-size: 15px; }}

            .last-update {{ color: #888; font-size: 12px; margin-top: 8px !important; }}

            .predict {{
                color: #f5a623;
                font-size: 20px;
                margin-top: 5px;
            }}

            .refresh-note {{
                color: #555;
                font-size: 11px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{emoji} Bhavnagar Weather</h1>

            <p class="temp">{temp}°C</p>
            <p class="label">OpenWeatherMap — Live</p>

            <div class="info">
                <p>💧 Humidity: {humidity}%</p>
                <p>💨 Wind: {windspeed} m/s</p>
                <p>🌥️ Condition: {description}</p>
                <p>🕐 Hour: {hour}:00</p>
            </div>

            <hr>

            {dht_section}

            <hr>

            <p class="predict">
                🔮 Predicted Temp (6hrs later):<br>
                <strong>{predicted_temp:.1f}°C</strong>
            </p>

            <p class="refresh-note">⟳ Page refreshes every 15 seconds</p>
        </div>
    </body>
    </html>
    """
    return html


# ==============================================
#   START SERVER
# ==============================================
if __name__ == "__main__":
    print("🚀 Weather Station Server starting...")
    print("📱 Open on phone: http://<your-pc-ip>:5000")
    print("💻 Open on PC:    http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

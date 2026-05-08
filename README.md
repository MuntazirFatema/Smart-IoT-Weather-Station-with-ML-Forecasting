# 🌤️ Smart IoT Weather Station with ML Forecasting

> Live DHT11 sensor + OpenWeatherMap API + Machine Learning — all in one Flask dashboard

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Flask-Web-green) ![ML](https://img.shields.io/badge/ML-RandomForest-orange) ![IoT](https://img.shields.io/badge/IoT-NodeMCU%20ESP8266-red)

---

## 📌 Project Overview

This project combines **IoT hardware**, **REST API integration**, and **Machine Learning** into a single live web dashboard that:

- Reads real-time temperature & humidity from a **DHT11 sensor** via **NodeMCU ESP8266**
- Fetches live weather data from **OpenWeatherMap API**
- Predicts **temperature 6 hours ahead** using a trained **RandomForestRegressor** model
- Displays everything on a clean **Flask web dashboard**

---

## 🏗️ System Architecture

```
DHT11 Sensor → NodeMCU ESP8266 → HTTP POST → Flask Server → Web Dashboard
                                                    ↑
                               OpenWeatherMap API → ML Model (RandomForest)
```

---

## 🚀 Features

- 🌡️ **Live sensor data** from DHT11 (temp + humidity) via NodeMCU
- 🌤️ **Real-time weather** from OpenWeatherMap API (Bhavnagar)
- 🤖 **ML prediction** — temperature 6 hours ahead (MAE: 0.74°C)
- 💡 **RGB LED indicators** on hardware (Red = Hot, Blue = Cold, Green = Normal)
- 🌐 **Flask web dashboard** auto-refreshes every 15 seconds
- 📊 **Data collection** — forecast data saved to CSV for model retraining

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Hardware | NodeMCU ESP8266, DHT11, RGB LED |
| Firmware | Arduino IDE (C++) |
| Backend | Python, Flask |
| ML | scikit-learn (RandomForestRegressor) |
| API | OpenWeatherMap REST API |
| Data | Pandas, NumPy |
| Serialization | Pickle |

---

## 📁 Project Structure

```
smart-weather-station/
├── app.py                          # Flask server
├── weather_model.pkl               # Trained ML model
├── weather_data.csv                # Collected forecast data
├── whetherstationpythonml.ipynb    # ML training notebook
├── nodemcu_code/
│   └── onlinewhetherstation.ino    # NodeMCU Arduino code
└── README.md
```

---

## 🤖 ML Model Details

| Parameter | Value |
|---|---|
| Model | RandomForestRegressor |
| Features | temp, humidity, windspeed, hour, description_encoded |
| Target | Temperature 6 hours later |
| MAE | 0.74°C |
| RMSE | 0.87°C |
| Training Data | 40 OpenWeatherMap forecast readings |

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/MuntazirFatema/smart-weather-station
cd smart-weather-station
```

### 2. Install dependencies
```bash
pip install flask scikit-learn pandas numpy requests pickle5
```

### 3. Add your API key
In `app.py`, replace:
```python
API_KEY = "your_openweathermap_api_key"
```

### 4. Run Flask server
```bash
python app.py
```

### 5. Open dashboard
```
http://localhost:5000
```

### 6. NodeMCU Setup
- Open `nodemcu_code/onlinewhetherstation.ino` in Arduino IDE
- Update WiFi credentials and Flask server IP
- Upload to NodeMCU ESP8266

---



## 👩‍💻 Author

**Muntazir Fatema Panjwani**
- GitHub: [@MuntazirFatema](https://github.com/MuntazirFatema)
- LinkedIn: [Muntazir Fatema](https://www.linkedin.com/in/muntazir-fatema)
- B.E. ECE Student @ GEC Bhavnagar

---


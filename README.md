# 🌦️ Weather Dashboard (Django) 
    A simple Django web application that allows users to check real-time weather information for any city using the OpenWeatherMap API.

## 🚀 Quick Setup

**Clone Repository**
    git clone https://github.com/YOUR_USERNAME/weather-dashboard.git
    cd weather-dashboard

1.Create & Activate Virtual Environment
    python -m venv venv
    venv\Scripts\activate

2.Install Dependencies

    pip install -r requirements.txt

3.Configure Environment Variables

4.Create a .env file in the project root:

    DJANGO_SECRET_KEY=your_secret_key
    DEBUG=True
    OPENWEATHER_API_KEY=your_openweather_api_key

5.Run the Server

    python manage.py migrate
    python manage.py runserver
    
    Open http://127.0.0.1:8000/ in your browser.

⚡ Features

    Search current weather by city
    Displays temperature, humidity, and conditions
    Secure API key management via .env

🔒 Security Notes

    Never commit .env or sensitive keys to GitHub.
    Virtual environments and local DB files are excluded via .gitignore.

📦 Dependencies

    Django
    python-dotenv
    requests

All dependencies installable via pip install -r requirements.txt



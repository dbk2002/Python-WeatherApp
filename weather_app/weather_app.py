import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = "dc599b6c6d664a24b1550152251009"

def get_weather(city):
    """Fetch current + 3-day forecast for a city using WeatherAPI.com"""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&aqi=no&alerts=no"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        location = data["location"]["name"]
        print(f"\nWeather for {location}:")

        forecast_data = []
        for day in data["forecast"]["forecastday"]:
            date = day["date"]
            condition = day["day"]["condition"]["text"]
            max_temp = day["day"]["maxtemp_c"]
            min_temp = day["day"]["mintemp_c"]
            avg_humidity = day["day"]["avghumidity"]

            print(f"{date}: {condition}, Max: {max_temp}°C, Min: {min_temp}°C, Humidity: {avg_humidity}%")
            forecast_data.append({
                "Date": date,
                "Condition": condition,
                "Max Temp (°C)": max_temp,
                "Min Temp (°C)": min_temp,
                "Humidity (%)": avg_humidity
            })

        return forecast_data

    except requests.RequestException as e:
        print(f"❌ Error fetching data for {city}: {e}")
        return []

def save_to_csv(city, forecast_data):
    """Save forecast data to CSV"""
    if forecast_data:
        df = pd.DataFrame(forecast_data)
        filename = f"{city}_forecast.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Forecast saved to {filename}")
        return df
    return None

def plot_temperature(city, df):
    """Plot Max & Min Temperature"""
    if df is not None:
        plt.figure(figsize=(8,5))
        plt.plot(df["Date"], df["Max Temp (°C)"], marker='o', label="Max Temp")
        plt.plot(df["Date"], df["Min Temp (°C)"], marker='o', label="Min Temp")
        plt.title(f"{city} 3-Day Temperature Forecast")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    cities_input = input("Enter city names (comma-separated): ")
    cities = [city.strip() for city in cities_input.split(",") if city.strip()]

    for city in cities:
        forecast = get_weather(city)
        df = save_to_csv(city, forecast)
        plot_temperature(city, df)

"""# weather.py
import requests
from datetime import datetime

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            # Create URL with parameters
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # For Celsius
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse response
            data = response.json()
            
            # Extract relevant information
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert to km/h
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
            }
            
            # Format weather message
            weather_message = (
                f"Weather in {weather_info['city']}, {weather_info['country']}:\n"
                f"Temperature: {weather_info['temperature']}°C (Feels like {weather_info['feels_like']}°C)\n"
                f"Condition: {weather_info['description']}\n"
                f"Humidity: {weather_info['humidity']}%\n"
                f"Wind Speed: {weather_info['wind_speed']} km/h\n"
                f"Sunrise: {weather_info['sunrise']}\n"
                f"Sunset: {weather_info['sunset']}"
            )
            
            return weather_message
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
        except (KeyError, ValueError) as e:
            return f"Error processing weather data: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"""
# weather.py
import requests
from datetime import datetime
import os

class WeatherService:
    def __init__(self, api_key=None):
        # Use provided API key or fall back to environment variable
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY', '6aa40bf5df7c3531c2cb9abdc1f3c2c3')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        if not city or city.isspace():
            return "Please provide a valid city name"
            
        try:
            # Clean up city input
            city = city.strip()
            
            # Create URL with parameters
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # For Celsius
            }
            
            # Make API request with timeout
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Handle city not found
            if response.status_code == 404:
                return f"City '{city}' not found. Please check the spelling and try again."
                
            # Handle other HTTP errors
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Extract relevant information with safer data access
            weather_info = {
                'city': data.get('name', city),
                'country': data.get('sys', {}).get('country', ''),
                'temperature': round(data.get('main', {}).get('temp', 0)),
                'feels_like': round(data.get('main', {}).get('feels_like', 0)),
                'description': data.get('weather', [{}])[0].get('description', '').capitalize(),
                'humidity': data.get('main', {}).get('humidity', 0),
                'wind_speed': round(data.get('wind', {}).get('speed', 0) * 3.6, 1),  # Convert to km/h
                'sunrise': datetime.fromtimestamp(data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data.get('sys', {}).get('sunset', 0)).strftime('%H:%M')
            }
            
            # Format weather message
            weather_message = (
                f"Weather in {weather_info['city']}, {weather_info['country']}:\n"
                f"Temperature: {weather_info['temperature']}°C (Feels like {weather_info['feels_like']}°C)\n"
                f"Condition: {weather_info['description']}\n"
                f"Humidity: {weather_info['humidity']}%\n"
                f"Wind Speed: {weather_info['wind_speed']} km/h\n"
                f"Sunrise: {weather_info['sunrise']}\n"
                f"Sunset: {weather_info['sunset']}"
            )
            
            return weather_message
            
        except requests.exceptions.Timeout:
            return "Weather service timeout. Please try again."
        except requests.exceptions.ConnectionError:
            return "Cannot connect to weather service. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: Please try again later"
        except (KeyError, ValueError, IndexError) as e:
            return f"Error processing weather data: Invalid response from weather service"
        except Exception as e:
            return f"An unexpected error occurred: Please try again later"
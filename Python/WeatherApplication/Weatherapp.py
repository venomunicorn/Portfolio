import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.api_key = "your_api_key_here"  # Replace with your OpenWeatherMap API key
        self.setup_ui()
        self.refresh_weather()

    def setup_ui(self):
        """Set up the user interface components"""
        self.root.title('Local Weather Application')
        self.root.geometry('400x300')
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Local Weather", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Location display
        self.location_label = ttk.Label(main_frame, text="Detecting location...", 
                                       font=('Arial', 12))
        self.location_label.pack(pady=(0, 10))
        
        # Weather information frame
        weather_frame = ttk.Frame(main_frame)
        weather_frame.pack(pady=(0, 20), fill=tk.X)
        
        # Temperature
        self.temp_label = ttk.Label(weather_frame, text="Temperature: --°C", 
                                   font=('Arial', 14, 'bold'))
        self.temp_label.pack(anchor=tk.W)
        
        # Weather description
        self.desc_label = ttk.Label(weather_frame, text="Condition: --", 
                                   font=('Arial', 12))
        self.desc_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Humidity
        self.humidity_label = ttk.Label(weather_frame, text="Humidity: --%", 
                                       font=('Arial', 12))
        self.humidity_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Pressure
        self.pressure_label = ttk.Label(weather_frame, text="Pressure: -- hPa", 
                                       font=('Arial', 12))
        self.pressure_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Refresh button
        self.refresh_button = ttk.Button(main_frame, text="Refresh Weather", 
                                        command=self.refresh_weather_threaded)
        self.refresh_button.pack(pady=(20, 0))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                     font=('Arial', 10), foreground="green")
        self.status_label.pack(pady=(10, 0))

    def get_current_location(self):
        """Get current location based on IP address"""
        try:
            # Using ipapi.co for free IP geolocation
            response = requests.get('https://ipapi.co/json/', timeout=10)
            response.raise_for_status()
            location_data = response.json()
            
            city = location_data.get('city', 'Unknown')
            region = location_data.get('region', 'Unknown')
            country = location_data.get('country_name', 'Unknown')
            latitude = location_data.get('latitude')
            longitude = location_data.get('longitude')
            
            return {
                'city': city,
                'region': region,
                'country': country,
                'lat': latitude,
                'lon': longitude
            }
        except requests.RequestException as e:
            print(f"Error getting location: {e}")
            return None

    def get_weather_data(self, lat, lon):
        """Fetch weather data from OpenWeatherMap API"""
        if not lat or not lon:
            return None
            
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            
            if weather_data.get('cod') == 200:
                return weather_data
            else:
                print(f"Weather API error: {weather_data.get('message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def update_ui(self, location_data, weather_data):
        """Update the UI with location and weather information"""
        if location_data:
            location_text = f"{location_data['city']}, {location_data['region']}, {location_data['country']}"
            self.location_label.config(text=f"Location: {location_text}")
        else:
            self.location_label.config(text="Location: Unable to detect")
        
        if weather_data:
            # Extract weather information
            temp = round(weather_data['main']['temp'], 1)
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            description = weather_data['weather'][0]['description'].title()
            
            # Update labels
            self.temp_label.config(text=f"Temperature: {temp}°C")
            self.desc_label.config(text=f"Condition: {description}")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.pressure_label.config(text=f"Pressure: {pressure} hPa")
            self.status_label.config(text="Weather updated successfully", 
                                   foreground="green")
        else:
            self.temp_label.config(text="Temperature: Unable to fetch")
            self.desc_label.config(text="Condition: --")
            self.humidity_label.config(text="Humidity: --%")
            self.pressure_label.config(text="Pressure: -- hPa")
            self.status_label.config(text="Failed to fetch weather data", 
                                   foreground="red")

    def refresh_weather(self):
        """Main function to refresh weather data"""
        self.status_label.config(text="Fetching data...", foreground="blue")
        self.refresh_button.config(state="disabled")
        
        # Get current location
        location_data = self.get_current_location()
        
        # Get weather data if location is available
        weather_data = None
        if location_data and location_data['lat'] and location_data['lon']:
            weather_data = self.get_weather_data(location_data['lat'], location_data['lon'])
        
        # Update UI
        self.update_ui(location_data, weather_data)
        self.refresh_button.config(state="normal")

    def refresh_weather_threaded(self):
        """Run refresh_weather in a separate thread to prevent UI freezing"""
        thread = threading.Thread(target=self.refresh_weather)
        thread.daemon = True
        thread.start()

def main():
    # Check if API key is set
    app_instance = None
    
    root = tk.Tk()
    app_instance = WeatherApp(root)
    
    # Check if API key needs to be set
    if app_instance.api_key == "your_api_key_here":
        messagebox.showwarning(
            "API Key Required", 
            "Please replace 'your_api_key_here' with your OpenWeatherMap API key.\n\n"
            "Get a free API key at: https://openweathermap.org/api"
        )
    
    root.mainloop()

if __name__ == "__main__":
    main()

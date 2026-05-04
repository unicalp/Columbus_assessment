import json
import urllib.request
import urllib.parse
import urllib.error

# 1. External API Communication
class OpenMeteoClient:
    """Handles communication with the Open-Meteo API."""
    
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def get_coordinates(self, city: str):
        """Converts a city name to latitude and longitude using Geocoding API."""
        encoded_city = urllib.parse.quote(city)
        url = f"{self.GEOCODE_URL}?name={encoded_city}&count=1"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                if "results" not in data or not data["results"]:
                    raise ValueError(f"City '{city}' not found.")
                
                # Return latitude, longitude, and the properly formatted city name
                return data["results"][0]["latitude"], data["results"][0]["longitude"], data["results"][0]["name"]
        except urllib.error.URLError as e:
            raise Exception(f"Geocoding failed: {str(e)}")

    def get_current_temperature(self, latitude: float, longitude: float) -> float:
        """Fetches the current temperature for given coordinates."""
        url = f"{self.WEATHER_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                return data['current_weather']['temperature']
        except urllib.error.URLError as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")

# 2. Business Logic
class TemperatureCategorizer:
    """Handles business rules for temperature classification."""
    
    @staticmethod
    def get_category(temperature: float) -> str:
        """Categorizes temperature based on business requirements."""
        if temperature < 0:
            return "Freezing"
        elif 0 <= temperature < 10:
            return "Cold"
        elif 10 <= temperature < 20:
            return "Mild"
        elif 20 <= temperature < 30:
            return "Warm"
        else:
            return "Hot"

# 3. Lambda Orchestrator
def lambda_handler(event, context):
    """
    AWS Lambda entry point. 
    Now supports both direct invocation and HTTP GET requests.
    """
    city = "Wrocław" 
    
    if event.get("queryStringParameters") and "city" in event["queryStringParameters"]:
        city = event["queryStringParameters"]["city"]
    elif event.get("city"):
        city = event["city"]
        
    weather_client = OpenMeteoClient()
    categorizer = TemperatureCategorizer()

    try:
        # Step 1: Geocode the city to get coordinates
        lat, lon, resolved_city_name = weather_client.get_coordinates(city)
        
        # Step 2: Fetch weather data
        current_temp = weather_client.get_current_temperature(lat, lon)
        
        # Step 3: Apply business logic
        temp_category = categorizer.get_category(current_temp)
        
        # Step 4: Return structured JSON
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "city": resolved_city_name,
                "temperature": current_temp,
                "unit": "Celsius",
                "category": temp_category
            })
        }
        
    except ValueError as ve:
        return {"statusCode": 404, "body": json.dumps({"error": str(ve)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
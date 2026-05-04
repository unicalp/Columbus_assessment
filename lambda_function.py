import json
import urllib.request
import urllib.error


# 1. External API Communication
class OpenMeteoClient:
    """Handles communication with the Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Coordinates for Wrocław
    LATITUDE = 51.10
    LONGITUDE = 17.03

    def get_current_temperature(self) -> float:
        """Fetches the current temperature for Wrocław."""
        url = f"{self.BASE_URL}?latitude={self.LATITUDE}&longitude={self.LONGITUDE}&current_weather=true"
        
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
    Strictly responsible for orchestration and formatting the response.
    """
    weather_client = OpenMeteoClient()
    categorizer = TemperatureCategorizer()

    try:
        # Step 1: Fetch data
        current_temp = weather_client.get_current_temperature()
        
        # Step 2: Apply business logic
        temp_category = categorizer.get_category(current_temp)
        
        # Step 3: Return structured JSON
        return {
            "statusCode": 200,
            "body": json.dumps({
                "city": "Wrocław",
                "temperature": current_temp,
                "unit": "Celsius",
                "category": temp_category
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
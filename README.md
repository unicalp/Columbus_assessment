# Weather Temperature Service (AWS Lambda)

## Brief Description
This is an AWS Lambda function that retrieves the current temperature for a specific location using the Open-Meteo API. Along with the numeric temperature, it returns a temperature category (e.g., Freezing, Cold, Mild, Warm, Hot) in a structured JSON format. 

## Key Design Decisions
To fulfill the object-oriented design requirements and separation of concerns, the code is structured into three distinct parts:
1. **`OpenMeteoClient`**: A class strictly dedicated to communicating with the external Open-Meteo API. It handles HTTP requests and JSON parsing.
2. **`TemperatureCategorizer`**: A class containing the business logic for classifying the temperature into categories based on predefined ranges.
3. **`lambda_handler`**: The main entry point. Its responsibility is limited to pure orchestration—it instantiates the classes, coordinates the data flow, and formats the final JSON response without holding any business logic itself.

## Unit Testing Approach (Without Real API Calls)
To unit test this solution without hitting the real Open-Meteo API, we can use **Mocking** (e.g., `unittest.mock.patch` in Python). 
By patching the `urllib.request.urlopen` method or mocking the `OpenMeteoClient.get_current_temperature` method directly, we can simulate different API responses (like simulating a response of -5°C or 35°C). This allows us to test if our `TemperatureCategorizer` business logic and our `lambda_handler` orchestration work correctly under various conditions without relying on network connectivity or the external service's uptime.

## Task 3: Endpoint Exposure

The Lambda function has been publicly exposed via an AWS Function URL. It accepts HTTP GET requests.

* **Publicly Accessible URL:** `https://4pkejwl4tiptcab2zejnwtdtby0byhzi.lambda-url.eu-north-1.on.aws/`
* **GET Parameter Name:** `city`

### Example Request & Response
**Request:**
`GET https://4pkejwl4tiptcab2zejnwtdtby0byhzi.lambda-url.eu-north-1.on.aws/?city=Paris`

**Response:**
```json
{
  "city": "Paris",
  "temperature": 18.5,
  "unit": "Celsius",
  "category": "Mild"
}
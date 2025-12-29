# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    """Get request with detailed debugging"""
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            if value:  # Only add if value is not None/empty
                params = params + str(key) + "=" + str(value) + "&"

    # Construct URL
    if params:
        request_url = backend_url + endpoint + "?" + params.rstrip('&')
    else:
        request_url = backend_url + endpoint

    print("=== DEBUG get_request ===")
    print(f"Full URL: {request_url}")

    try:
        # Add headers
        headers = {
            'User-Agent': 'Django-App/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        print(f"Making request to: {request_url}")
        response = requests.get(request_url, headers=headers, timeout=10)

        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response text (first 500 chars): {response.text[:500]}")

        # Check if response is successful
        response.raise_for_status()

        # Try to parse JSON
        data = response.json()
        print(f"Parsed JSON type: {type(data)}")
        if isinstance(data, list):
            print(f"List length: {len(data)}")
            if len(data) > 0:
                print(f"First item: {data[0]}")
        elif isinstance(data, dict):
            print(f"Dict keys: {list(data.keys())}")

        return data

    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        return {"error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response text: {e.response.text[:500]}")
        return {"error": str(e)}
    except ValueError as e:  # JSON decode error
        print(f"ERROR: JSON decode error: {e}")
        print(f"Raw response: {response.text if response else 'No response'}")
        return {"error": "Invalid JSON response"}
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return {"error": str(e)}
    finally:
        print("=== END get_request ===")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except BaseException:
        print("Network exception occurred")

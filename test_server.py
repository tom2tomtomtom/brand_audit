import requests
import time

def test_server():
    try:
        response = requests.get("http://localhost:8080")
        print(f"Server status: {response.status_code}")
        print(f"Response content: {response.text[:100]}...")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not running or not accessible")
        return False

if __name__ == "__main__":
    max_attempts = 5
    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1}/{max_attempts}")
        if test_server():
            break
        time.sleep(2)
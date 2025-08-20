import requests
import json

BASE_URL = "http://localhost:8000"


def test_api():
    print("Testing User Logs API...")

    print("\n1. Getting all logs:")
    response = requests.get(f"{BASE_URL}/logs")
    print(f"Status: {response.status_code}")
    logs = response.json()
    for log in logs:
        print(f"  - User {log['user_id']}: {log['action']} - {log['message']}")

    print("\n2. Creating new log entry:")
    new_log = {
        "user_id": 5,
        "action": "api_test",
        "message": "Testing API from Python script",
    }
    response = requests.post(f"{BASE_URL}/log", json=new_log)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\n3. Getting logs for user 1:")
    response = requests.get(f"{BASE_URL}/logs/1")
    print(f"Status: {response.status_code}")
    user_logs = response.json()
    for log in user_logs:
        print(f"  - {log['action']}: {log['message']} at {log['created_at']}")

    print("\n✅ API test completed!")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: API server not running. Start it with 'python main_sqlite.py'")
    except Exception as e:
        print(f"❌ Error: {e}")

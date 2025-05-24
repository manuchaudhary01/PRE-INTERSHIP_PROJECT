import time
import requests

CRM_API_URL = "http://localhost:5000/customers"
INVENTORY_API_URL = "http://localhost:5001/welcome-package"

processed_customers = set()

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def fetch_customers_with_retry():
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(CRM_API_URL, timeout=5)
            if response.status_code == 200:
                return response.json()  # Should be a list
            else:
                print(f"⚠️  Attempt {attempt+1}: Failed to fetch customers (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Attempt {attempt+1}: Exception occurred - {e}")
        time.sleep(RETRY_DELAY)
    print("❌ Failed to fetch customers after multiple attempts.")
    return []

def send_package_request_with_retry(customer_name):
    payload = {"customer_name": customer_name}
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(INVENTORY_API_URL, json=payload, timeout=5)
            if response.status_code == 201:
                return True
            else:
                print(f"⚠️  Attempt {attempt+1}: Failed to send package (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Attempt {attempt+1}: Exception during package request - {e}")
        time.sleep(RETRY_DELAY)
    print(f"❌ Failed to send welcome package for {customer_name} after multiple attempts.")
    return False

def poll_and_integrate():
    print("🔁 Integration Service started. Polling every 5 seconds...\n")
    while True:
        try:
            customers = fetch_customers_with_retry()
            for customer in customers:
                if customer["id"] not in processed_customers:
                    success = send_package_request_with_retry(customer["name"])
                    if success:
                        print(f"✅ Sent package request for {customer['name']}")
                    processed_customers.add(customer["id"])
        except Exception as e:
            print(f"❌ Unexpected error during integration loop: {e}")
        time.sleep(5)

if __name__ == "__main__":
    poll_and_integrate()

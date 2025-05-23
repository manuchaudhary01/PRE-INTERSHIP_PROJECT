import time
import requests

CRM_API_URL = "http://localhost:5000/customers"
INVENTORY_API_URL = "http://localhost:5001/welcome-package"

processed_customers = set()

def poll_and_integrate():
    print("🔁 Integration Service started. Polling every 5 seconds...\n")
    while True:
        try:
            response = requests.get(CRM_API_URL)
            if response.status_code == 200:
                customers = response.json()  # Fixed here!
                for customer in customers:
                    if customer["id"] not in processed_customers:
                        inventory_payload = {"customer_name": customer["name"]}
                        res = requests.post(INVENTORY_API_URL, json=inventory_payload)
                        if res.status_code == 201:
                            print(f"✅ Sent package request for {customer['name']}")
                        else:
                            print(f"⚠️  Failed to send package request: {res.status_code} - {res.text}")
                        processed_customers.add(customer["id"])
            else:
                print(f"❌ Failed to fetch customers from CRM. Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error during integration: {e}")

        time.sleep(5)

if __name__ == "__main__":
    poll_and_integrate()

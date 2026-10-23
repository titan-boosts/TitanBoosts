import requests
URL = "http://localhost:8000/sellauth-webhook"
payload = {
    "event": "order.completed",
    "data": {
        "custom_fields": {
            "Guild ID": "123456789012345678",
            "Channel ID": "987654321098765432",
            "Bot Type": "online",
            "Quantity": "2"
        }
    }
}
print("🚀 Sending test payload...")
try:
    r = requests.post(URL, json=payload)
    print("Status:", r.status_code)
    print("Data:", r.json())
except Exception as e:
    print("Error details:", e)

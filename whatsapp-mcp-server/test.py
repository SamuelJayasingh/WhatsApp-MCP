import requests

url = "http://localhost:5000/send-file"

payload = {
    "phone_number": "919789820475",
    "file_path": "../whatsapp-mcp-server/main.py"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
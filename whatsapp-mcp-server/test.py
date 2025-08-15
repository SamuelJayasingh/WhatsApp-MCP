import requests

url = "https://your-ngrok-url-here/send-file"  # Replace with your ngrok URL or server URL

payload = {
    "phone_number": "YOUR_PHONE_NUMBER",  # Replace with the desired phone number
    "file_path": "https://images.pexels.com/photos/236047/pexels-photo-236047.jpeg?cs=srgb&dl=clouds-cloudy-countryside-236047.jpg"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())

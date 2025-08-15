import requests

url = " https://08e595a9ced9.ngrok-free.app/send-file"

payload = {
    "phone_number": "917358303352",
    "file_path": "https://images.pexels.com/photos/236047/pexels-photo-236047.jpeg?cs=srgb&dl=clouds-cloudy-countryside-236047.jpg"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
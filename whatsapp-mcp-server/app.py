from flask import Flask, request, jsonify
from whatsapp import (
    send_file as whatsapp_send_file,
)
import os
import requests
import tempfile

app = Flask(__name__)

@app.route("/send-file", methods=["POST"])
def send_file():
    data = request.json
    phone_number = data.get("phone_number")
    file_path = data.get("file_path")

    if not phone_number or not file_path:
        return jsonify({"error": "phone_number and file_path are required"}), 400

    # Check if the file_path is a URL
    if file_path.startswith("http://") or file_path.startswith("https://"):
        try:
            # Download the file from the URL to a temporary location
            response = requests.get(file_path, stream=True)
            response.raise_for_status()
            
            # Create a temporary file with the correct extension
            temp_file_ext = os.path.splitext(file_path.split('?')[0])[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=temp_file_ext) as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Send the temporary file
            whatsapp_send_file(phone_number, temp_file_path)
            
            # Clean up the temporary file
            os.remove(temp_file_path)
            
            return jsonify({"status": "success", "message": f"File from URL sent to {phone_number}"})
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "error", "message": f"Failed to download file from URL: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    # Handle local file paths
    elif os.path.exists(file_path):
        try:
            whatsapp_send_file(phone_number, file_path)
            return jsonify({"status": "success", "message": f"Local file sent to {phone_number}"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({
            "status": "error",
            "message": f"File not found: {file_path}",
            "current_directory": os.getcwd(),
            "files_in_directory": os.listdir(".")
        }), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
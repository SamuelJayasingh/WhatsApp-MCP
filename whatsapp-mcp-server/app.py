from flask import Flask, request, jsonify
from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)
import os

app = Flask(__name__)

@app.route("/send-file", methods=["POST"])
def send_file():
    data = request.json
    phone_number = data.get("phone_number")
    file_path = data.get("file_path")

    if not phone_number or not file_path:
        return jsonify({"error": "phone_number and file_path are required"}), 400

    if os.path.exists(file_path):
        try:
            whatsapp_send_file(phone_number, file_path)
            return jsonify({"status": "success", "message": f"File sent to {phone_number}"})
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
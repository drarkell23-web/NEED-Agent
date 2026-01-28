import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='public')

# --- SENIOR CEO HARDCODED CONFIG ---
TELEGRAM_TOKEN = "8322173594:AAGB7-XKdq3OSih_semZ5dcttN_PPqL7_AA"
CHAT_ID = "8187670531"

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        # Capture data from ANY source (Form or JSON)
        data = request.form if request.form else request.get_json()
        
        name = data.get('name', 'N/A')
        phone = data.get('phone', 'N/A')
        p_type = data.get('property_type', 'N/A')
        intent = data.get('intent', 'N/A')
        msg = data.get('description', 'No details.')

        # Build the HTML Message
        caption = (
            f"🏰 <b>NEW SA LEAD</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 <b>Name:</b> {name}\n"
            f"📞 <b>Phone:</b> {phone}\n"
            f"🏠 <b>Type:</b> {p_type}\n"
            f"🔑 <b>Intent:</b> {intent}\n\n"
            f"📝 <b>Details:</b> {msg}\n"
            f"━━━━━━━━━━━━━━"
        )

        # Immediate Telegram Push
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': caption, 'parse_mode': 'HTML'}
        
        # Send it
        res = requests.post(url, data=payload, timeout=8)
        
        if res.status_code == 200:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "info": res.text}), 400

    except Exception as e:
        return jsonify({"status": "crash", "error": str(e)}), 500

# This is for local testing. Netlify uses the 'app' object directly.
if __name__ == "__main__":
    app.run(debug=True)

import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='public')

# --- DEFINITIVE CONFIG (Hardcoded to bypass Netlify Setting errors) ---
TELEGRAM_TOKEN = "8322173594:AAGB7-XKdq3OSih_semZ5dcttN_PPqL7_AA"
CHAT_ID = "8187670531"

@app.route('/')
def index():
    # Serves your frontend
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        # CEO Logic: Handle both Form-data AND JSON data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Extracting fields (with fallbacks so it never crashes)
        name = data.get('name', 'Not Provided')
        phone = data.get('phone', 'Not Provided')
        prop_type = data.get('property_type', 'Not Provided')
        intent = data.get('intent', 'Not Provided')
        description = data.get('description', 'No details provided.')
        savings = data.get('savings_amount', 'N/A')

        # 1. Build the Message (HTML is safer than Markdown)
        caption = (
            f"🏰 <b>NEED a AGENT: NEW LEAD</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Client:</b> {name}\n"
            f"📞 <b>Phone:</b> {phone}\n"
            f"🏢 <b>Type:</b> {prop_type}\n"
            f"🔑 <b>Intent:</b> {intent}\n"
            f"💰 <b>Savings:</b> {savings}\n\n"
            f"📝 <b>Details:</b> {description}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        # 2. Execute the Telegram Call
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': caption,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        # 3. Check Result
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Lead sent!"}), 200
        else:
            # If Telegram rejects it, we return the error from them
            return jsonify({"status": "error", "details": response.text}), 400

    except Exception as e:
        # If the code crashes, we return the exact error
        return jsonify({"status": "crash", "error": str(e)}), 500

if __name__ == "__main__":
    # Standard Flask start
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

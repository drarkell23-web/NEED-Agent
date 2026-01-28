import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='public')

# --- DEFINITIVE CONFIGURATION ---
# This pulls from the Netlify Environment Variables you just set
TELEGRAM_TOKEN = os.getenv("8322173594:AAGB7-XKdq3OSih_semZ5dcttN_PPqL7_AA")
CHAT_ID = os.getenv("8187670531")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    # 1. Check if keys exist
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ ERROR: Environment Variables NOT FOUND in Netlify Settings!")
        return jsonify({"error": "Server configuration error"}), 500

    try:
        # Extract Data
        data = request.form
        name = data.get('name', 'Unknown')
        phone = data.get('phone', 'N/A')
        
        # 2. Build Message (Using HTML mode for maximum stability)
        caption = (
            f"🏰 <b>NEW LEAD: {name}</b>\n"
            f"📞 <b>Phone:</b> {phone}\n"
            f"📝 <b>Details:</b> {data.get('description', 'N/A')}"
        )

        # 3. Execution
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': caption, 'parse_mode': 'HTML'}
        
        # We use a timeout to prevent the app from hanging
        response = requests.post(url, data=payload, timeout=10)
        
        # 4. The "Senior CEO" Audit
        if response.status_code == 200:
            print(f"✅ SUCCESS: Lead for {name} sent.")
            return jsonify({"success": True}), 200
        else:
            print(f"❌ TELEGRAM REJECTED: {response.status_code} - {response.text}")
            return jsonify({"error": f"Telegram error: {response.status_code}"}), 500

    except Exception as e:
        print(f"🔥 SYSTEM CRASH: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

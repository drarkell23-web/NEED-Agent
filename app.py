import os
import requests
from flask import Flask, request, jsonify, send_from_directory

# --- DIRECTORY CONFIGURATION ---
base_dir = os.path.abspath(os.path.dirname(__file__))
public_dir = os.path.join(base_dir, 'public')

app = Flask(__name__, static_folder=public_dir)

# --- CONFIGURATION (Use Environment Variables on Render!) ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8322173594:AAGB7-XKdq3OSih_semZ5dcttN_PPqL7_AA")
CHAT_ID = os.environ.get("CHAT_ID", "8187670531")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        # Extract Data from Form
        name = request.form.get('name', 'N/A')
        phone = request.form.get('phone', 'N/A')
        prop_type = request.form.get('property_type', 'N/A')
        intent = request.form.get('intent', 'N/A')
        description = request.form.get('description', 'No description provided')
        savings = request.form.get('savings_amount', 'N/A')
        off_market = request.form.get('off_market_request', 'false')

        # CEO Logic: Use HTML mode to prevent message crashes
        # <b> = Bold, <i> = Italic
        caption = (
            f"🏰 <b>NEED a AGENT: NEW LEAD</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Client:</b> {name}\n"
            f"📞 <b>Phone:</b> {phone}\n"
            f"🏢 <b>Type:</b> {prop_type}\n"
            f"🔑 <b>Intent:</b> {intent}\n"
            f"💰 <b>Savings:</b> {savings}\n"
            f"🕵️ <b>Off-Market:</b> {'✅ YES' if off_market == 'true' else '❌ NO'}\n\n"
            f"📝 <b>Details:</b> <i>{description}</i>\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        # Send to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID, 
            'text': caption, 
            'parse_mode': 'HTML'  # Changed to HTML for reliability
        }
        
        response = requests.post(url, data=payload)
        
        # Log the result for debugging in Render logs
        if response.status_code == 200:
            print(f"✅ Lead from {name} sent to Telegram.")
            return jsonify({"success": True}), 200
        else:
            print(f"❌ Telegram Error {response.status_code}: {response.text}")
            return jsonify({"error": "Telegram Delivery Failed"}), 500

    except Exception as e:
        print(f"🔥 Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

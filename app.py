import os
import requests
from flask import Flask, request, jsonify, send_from_directory

# --- DIRECTORY CONFIGURATION ---
# This ensures the app works on Render (Linux) and Local (Windows/Mac)
base_dir = os.path.abspath(os.path.dirname(__file__))
public_dir = os.path.join(base_dir, 'public')

app = Flask(__name__, static_folder=public_dir)

# --- TELEGRAM CONFIG ---
TELEGRAM_TOKEN = "8595813958:AAFpKSuq9j_qny2DlIgP2rJwHe1Mu_xTsDU"
CHAT_ID = "8187670531"

@app.route('/')
def index():
    # Explicitly serving index.html from the public folder
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        # Extract Data
        name = request.form.get('name')
        phone = request.form.get('phone')
        prop_type = request.form.get('property_type')
        intent = request.form.get('intent')
        description = request.form.get('description')
        savings = request.form.get('savings_amount')
        off_market = request.form.get('off_market_request')

        # Construct High-Value Message
        caption = (
            f"🏰 *NEED a AGENT: NEW LEAD*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Client:* {name}\n"
            f"📞 *Phone:* {phone}\n"
            f"🏢 *Type:* {prop_type}\n"
            f"🔑 *Intent:* {intent}\n"
            f"💰 *Savings:* {savings}\n"
            f"🕵️ *Off-Market:* {'YES' if off_market == 'true' else 'NO'}\n\n"
            f"📝 *Details:* {description}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        # Send to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': caption, 'parse_mode': 'Markdown'}
        requests.post(url, data=payload)

        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server Error"}), 500

if __name__ == "__main__":
    # Binding to 0.0.0.0 is mandatory for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

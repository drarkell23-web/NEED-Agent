from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='public')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛠️ NEED a AGENT CONFIGURATION
TELEGRAM_TOKEN = "8595813958:AAFpKSuq9j_qny2DlIgP2rJwHe1Mu_xTsDU"
CHAT_ID = "8187670531"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        prop_type = request.form.get('property_type') # Commercial/Industrial/House
        intent = request.form.get('intent') # Buy/Rent/Sell Private
        description = request.form.get('description')
        popi_consent = request.form.get('popi_consent')

        if popi_consent != 'true':
            return jsonify({"error": "POPI Consent Required"}), 400

        caption = (
            f"🏠 *NEW REAL ESTATE LEAD: NEED a AGENT*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Client:* {name}\n"
            f"📞 *Phone:* {phone}\n"
            f"🏢 *Type:* {prop_type}\n"
            f"🔑 *Action:* {intent}\n\n"
            f"📝 *Details:*\n{description}\n"
            f"⚖️ *POPI Act:* Consent Granted\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        image = request.files.get('image')

        if image:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': (image.filename, image.read(), image.content_type)}
            data = {'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
            requests.post(url, data=data, files=files)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {'chat_id': CHAT_ID, 'text': caption, 'parse_mode': 'Markdown'}
            requests.post(url, data=data)

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
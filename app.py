const axios = require('axios');
const FormData = require('form-data');
const busboy = require('busboy');

exports.handler = async (event) => {
    if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method Not Allowed" };

    const TELEGRAM_TOKEN = "8322173594:AAGB7-XKdq3OSih_semZ5dcttN_PPqL7_AA"; 
    const CHAT_ID = "8187670531";

    return new Promise((resolve) => {
        const bb = busboy({ headers: event.headers });
        let fields = {};
        let fileData = null;

        bb.on('file', (name, file, info) => {
            const chunks = [];
            file.on('data', (data) => chunks.push(data));
            file.on('end', () => { fileData = { buffer: Buffer.concat(chunks), filename: info.filename }; });
        });

        bb.on('field', (name, val) => { fields[name] = val; });

        bb.on('finish', async () => {
            const caption = `🚀 *NEW LEAD* \n👤 Name: ${fields.name}\n📞 Phone: ${fields.phone}\n🛠 Service: ${fields.service}\n📝 Details: ${fields.description}`;
            try {
                if (fileData) {
                    const form = new FormData();
                    form.append('chat_id', CHAT_ID);
                    form.append('photo', fileData.buffer, { filename: fileData.filename });
                    form.append('caption', caption);
                    form.append('parse_mode', 'Markdown');
                    await axios.post(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendPhoto`, form, { headers: form.getHeaders() });
                } else {
                    await axios.post(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, { chat_id: CHAT_ID, text: caption, parse_mode: 'Markdown' });
                }
                resolve({ statusCode: 200, body: JSON.stringify({ success: true }) });
            } catch (err) {
                resolve({ statusCode: 500, body: "Error sending to Telegram" });
            }
        });

        bb.end(Buffer.from(event.body, event.isBase64Encoded ? 'base64' : 'utf8'));
    });
};

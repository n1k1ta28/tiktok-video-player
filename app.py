from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def mobile_to_desktop_tiktok(mobile_url):
    response = requests.get(mobile_url)
    if response.status_code == 200:
        redirected_url = response.url
        match = re.search(r'@(.*?)\/video\/(\d+)|\/video\/(\d+)', redirected_url)
        if match:
            username = match.group(1)
            video_id = match.group(2) or match.group(3)
            return f"https://www.tiktok.com/@{username}/video/{video_id}" if username else f"https://www.tiktok.com/video/{video_id}"
        else:
            return None
    else:
        return None

@app.route('/convert', methods=['POST'])
def convert_link():
    try:
        data = request.json
        mobile_link = data.get('url')

        # Ensure the URL is provided
        if not mobile_link:
            return jsonify({'error': 'No URL provided'}), 400

        desktop_link = mobile_to_desktop_tiktok(mobile_link)
        if desktop_link:
            return jsonify({'desktop_link': desktop_link})
        else:
            return jsonify({'error': 'Invalid mobile TikTok URL'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message as JSON

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()

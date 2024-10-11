from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

def mobile_to_desktop_tiktok(mobile_url):
    try:
        response = requests.get(mobile_url)
        print(f"Response Code: {response.status_code}")  # Log the response code
        print(f"Response URL: {response.url}")  # Log the redirected URL
        if response.status_code == 200:
            redirected_url = response.url
            match = re.search(r'@(.*?)\/(?:video|photo)\/(\d+)', redirected_url)
            if match:
                username = match.group(1)
                video_id = match.group(2)
                if 'video' in redirected_url:
                    return f"https://www.tiktok.com/@{username}/video/{video_id}", "video"
                elif 'photo' in redirected_url:
                    return f"https://www.tiktok.com/@{username}/photo/{video_id}", "photo"
            else:
                return None, None
        else:
            print(f"Failed to fetch TikTok URL, Status Code: {response.status_code}, Response: {response.text}")  # Log failure
            return None, None
    except Exception as e:
        print(f"Error fetching URL: {e}")  # Print any errors encountered
        return None, None

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    mobile_link = data.get('url')
    print("Mobile Link Received:", mobile_link)  # Debugging line
    desktop_link, content_type = mobile_to_desktop_tiktok(mobile_link)
    
    if desktop_link:
        return jsonify({'desktop_link': desktop_link, 'content_type': content_type})
    else:
        return jsonify({'error': 'Could not convert the mobile link.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

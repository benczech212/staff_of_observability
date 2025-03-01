from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

# HTML template with placeholders for dynamic data
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Device Status</title>
    <style>
        .key-state { margin: 10px 0; }
        .encoder { margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Device Status</h1>
    <div id="neokey">
        <h2>NeoKey1</h2>
        <div id="keys"></div>
    </div>
    <div id="encoder">
        <h2>RotaryEncoder1</h2>
        <p id="button">Button Pressed: <span id="button-status">false</span></p>
        <p id="position">Position: <span id="position-value">0</span></p>
    </div>
    <script>
        async function fetchDataAndUpdateUI() {
            try {
                // Fetch JSON data from the Flask endpoint
                const response = await fetch('/fetch-data');
                const data = await response.json();

                // Update NeoKey1 keys
                const keysContainer = document.getElementById('keys');
                keysContainer.innerHTML = ''; // Clear existing keys
                for (const [key, value] of Object.entries(data.NeoKey1.keys)) {
                    const keyState = document.createElement('div');
                    keyState.className = 'key-state';
                    keyState.textContent = `Key ${key}: ${value}`;
                    keysContainer.appendChild(keyState);
                }

                // Update RotaryEncoder1
                document.getElementById('button-status').textContent = data.RotoryEncoder1.button_pressed;
                document.getElementById('position-value').textContent = data.RotoryEncoder1.position;

            } catch (error) {
                console.error('Error fetching or updating data:', error);
            }
        }

        // Poll the Flask endpoint every 1 second
        setInterval(fetchDataAndUpdateUI, 1000);

        // Initial call to populate data immediately
        fetchDataAndUpdateUI();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Serve the HTML page
    return render_template_string(HTML_TEMPLATE)

@app.route('/fetch-data')
def fetch_data():
    try:
        # Fetch data from the remote endpoint
        response = requests.get('http://192.168.4.99:8000/io')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

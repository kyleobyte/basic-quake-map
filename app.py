from flask import Flask, render_template
import urllib.request
import ssl
import json
import requests
import traceback

app = Flask(__name__)


@app.route("/")
def index():
    url = "https://stream.kyleobyte.com/quake-list/quake-list.json"

    # Disable SSL verification for urllib
    context = ssl._create_unverified_context()

    quake_data = {}
    try:
        # First try urllib
        with urllib.request.urlopen(url, context=context) as response:
            quake_data = json.loads(response.read().decode())
    except Exception as e:
        print("🔥 urllib failed:")
        traceback.print_exc()

        try:
            # Fallback to requests with SSL verify disabled
            r = requests.get(url, timeout=5, verify=False)
            r.raise_for_status()
            quake_data = r.json()
        except Exception as e2:
            print("🔥 requests failed too:")
            traceback.print_exc()
            quake_data = {"error": f"urllib: {str(e)} | requests: {str(e2)}"}

    quake_data_json = json.dumps(quake_data)
    return render_template("index.html", quake_data_json=quake_data_json)


if __name__ == "__main__":
    app.run(debug=True)

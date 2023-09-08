from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_title(url):
    try:
        # Define a User-Agent header to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Send an HTTP GET request with the User-Agent header
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title
            title = soup.title.string if soup.title else "No title found"

            return title
        else:
            return f"Failed to retrieve page: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urls = request.form.get("urls")
        urls = urls.strip().split("\n")

        return render_template("index.html", urls=urls)

    return render_template("index.html", urls=[])

@app.route("/fetch_title", methods=["POST"])
def fetch_title():
    url = request.form.get("url")
    title = get_title(url)
    return jsonify(title)

if __name__ == "__main__":
    app.run(debug=True)
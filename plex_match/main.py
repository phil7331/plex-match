from flask import Flask, render_template
import requests

app = Flask(__name__)

# Define the route for the homepage
@app.route('/')
def index():
    # Replace this with the API you're calling
    api_url = 'https://api.example.com/data'
    response = requests.get(api_url)
    data = response.json()

    # Pass the data to the frontend
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

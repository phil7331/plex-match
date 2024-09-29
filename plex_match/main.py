from flask import Flask, render_template
import requests

app = Flask(__name__)


# Define the route for the homepage
@app.route('/')
def index():
    # Replace this with the API you're calling
    # api_url = 'https://api.example.com/data'
    # response = requests.get(api_url)
    context = [1, 2, 3]

    # Pass the data to the frontend
    return render_template(template_name_or_list='index.html', context=context)


if __name__ == '__main__':
    print("HELLO")
    app.run(debug=True)

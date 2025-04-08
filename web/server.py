
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "DogteaMinerBot Web Server (MiniApp)"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

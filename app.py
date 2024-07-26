from backend import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

if __name__ == '__main__':
    app.run(debug=True)

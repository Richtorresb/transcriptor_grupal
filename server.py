from flask_app import app
from flask_app.controllers import core, transcript, home

if __name__ == "__main__":
    app.run(debug=True)
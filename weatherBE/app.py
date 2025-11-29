# MAIN FLASK APP (Weather API)

from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints
from blueprints.auth.auth import auth_bp
from blueprints.weather.weather import weather_bp
from blueprints.comments.comments import comments_bp
from blueprints.readings.readings import readings_bp  

# Create Flask app
app = Flask(__name__)
CORS(app)

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(readings_bp)  


# HOME ROUTE (for quick testing)
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Weather API ",
        "available_routes": {
            "auth": ["/register", "/login", "/logout"],
            "weather": ["/weather", "/weather/<id>"],
            "comments": ["/weather/<id>/comments"],
            "readings": ["/weather/<id>/readings"]
        }
    }), 200


# ERROR HANDLERS 
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)


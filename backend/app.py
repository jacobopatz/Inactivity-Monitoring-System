from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bed_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Database Model
class BedEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    duration_seconds = db.Column(db.Float, default=0.0)

# Initialize Database
with app.app_context():
    db.create_all()

# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_data():
    """Receives data from Raspberry Pi and stores it in the database."""
    data = request.json
    if not data or "start_time" not in data or "duration_seconds" not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    try:
        start_time = datetime.fromisoformat(data["start_time"])
        duration = float(data["duration_seconds"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400

    entry = BedEntry(start_time=start_time, duration_seconds=duration)
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({"message": "Data received"}), 200

# Retrieve endpoint
@app.route('/data', methods=['GET'])
def get_data():
    """Returns all stored bed-tracking data."""
    entries = BedEntry.query.all()
    return jsonify([
        {
            "start_time": entry.start_time.isoformat(),
            "duration_seconds": entry.duration_seconds
        }
        for entry in entries
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

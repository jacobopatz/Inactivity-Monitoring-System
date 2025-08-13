from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bed_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Database Model
class BedEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    timestamp = db.Column(db.DateTime, nullable=False)
    person_detected = db.Column(db.Boolean, default= False)


# Initialize Database
with app.app_context():
    db.create_all()


def parse_timestamp_to_date(timestamp_str):
    """Parse ISO timestamp string to date object"""
    return datetime.fromisoformat(timestamp_str).date()



@app.route('/upload', methods=['POST'])
def upload_data():
    """Receives session data from Raspberry Pi and stores it as minute entries."""
    data = request.json
    if not data or "start_time" not in data or "duration_minutes" not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    try:
        start_time = datetime.fromisoformat(data["start_time"])
        duration_minutes = float(data["duration_minutes"])
        person_detected=bool(data['person_detected'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400

    # Expand into minute-by-minute entries
    time_to_enter = start_time
    end_time = start_time + timedelta(minutes=duration_minutes)

    while time_to_enter < end_time:
        entry = BedEntry(timestamp=time_to_enter, person_detected=person_detected)
        db.session.add(entry)
        time_to_enter += timedelta(minutes=1)
    entry = BedEntry(timestamp=time_to_enter, person_detected=False)
    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Data received and expanded into minute entries"}), 200



# Retrieve endpoint
@app.route('/data', methods=['GET'])
def get_data():
    """Returns all stored bed-tracking data."""
    entries = BedEntry.query.all()
    return jsonify([
        {
            "timestamp": entry.timestamp.isoformat(),
            "person_detected":entry.person_detected
        }
        for entry in entries
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

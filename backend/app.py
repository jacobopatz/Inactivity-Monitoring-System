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
    timestamp = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Float, nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

@app.route('/upload', methods=['POST'])
def upload_data():
    """Receives data from Raspberry Pi and stores it in the database."""
    data = request.json
    if not data or "timestamp" not in data or "duration" not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    entry = BedEntry(timestamp=data["timestamp"], duration=data["duration"])
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({"message": "Data received"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    """Returns all stored bed-tracking data."""
    entries = BedEntry.query.all()
    return jsonify([
        {"timestamp": entry.timestamp, "duration": entry.duration} 
        for entry in entries
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

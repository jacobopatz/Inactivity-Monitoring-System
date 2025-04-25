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

    start_time = db.Column(db.DateTime, nullable=False)
    duration_seconds = db.Column(db.Float, default=0.0)


# Initialize Database
with app.app_context():
    db.create_all()


def parse_timestamp_to_date(timestamp_str):
    """Parse ISO timestamp string to date object"""
    return datetime.fromisoformat(timestamp_str).date()


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

@app.route('/summary/daily', methods=['GET'])
def get_daily_summary():
    """Returns a summary of today's bed occupancy data."""
    today = date.today().isoformat()
    entries = BedEntry.query.all()
    
    today_entries = [
        entry for entry in entries 
        if parse_timestamp_to_date(entry.timestamp) == date.today()
    ]
    
    return jsonify(calculate_summary(today_entries, "Today"))

@app.route('/summary/weekly', methods=['GET'])
def get_weekly_summary():
    """Returns a summary of the past 7 days of bed occupancy data."""
    entries = BedEntry.query.all()
    
    # Group entries by date
    daily_entries = defaultdict(list)
    for entry in entries:
        entry_date = parse_timestamp_to_date(entry.timestamp)
        if entry_date >= date.today() - timedelta(days=6):
            daily_entries[entry_date].append(entry)
    
    # Create summary for each of the last 7 days
    summary = []
    for day_offset in range(6, -1, -1):  # From 6 days ago to today
        day = date.today() - timedelta(days=day_offset)
        day_entries = daily_entries.get(day, [])
        day_name = day.strftime("%A")
        
        if day_offset == 0:
            day_display = "Today"
        elif day_offset == 1:
            day_display = "Yesterday"
        else:
            day_display = day_name
            
        summary.append(calculate_summary(day_entries, day_display))
    
    return jsonify(summary)

def calculate_summary(entries, period_name):
    """Calculate summary statistics for a set of entries."""
    if not entries:
        return {
            "period": period_name,
            "date": date.today().isoformat(),
            "total_entries": 0,
            "occupied_entries": 0,
            "occupancy_percentage": 0,
            "occupancy_trend": []
        }
    
    # Sort entries by timestamp
    sorted_entries = sorted(entries, key=lambda x: x.timestamp)
    
    # Calculate basic stats
    total_entries = len(sorted_entries)
    occupied_entries = sum(1 for entry in sorted_entries if entry.person_detected)
    occupancy_percentage = (occupied_entries / total_entries) * 100 if total_entries > 0 else 0
    
    # Calculate hourly trend (simplified)
    hourly_trend = []
    for hour in range(24):
        hour_entries = [
            entry for entry in sorted_entries
            if datetime.fromisoformat(entry.timestamp).hour == hour
        ]
        hour_occupied = sum(1 for entry in hour_entries if entry.person_detected)
        hour_total = len(hour_entries)
        hour_percentage = (hour_occupied / hour_total * 100) if hour_total > 0 else 0
        hourly_trend.append({
            "hour": hour,
            "occupancy_percentage": round(hour_percentage, 1)
        })
    
    return {
        "period": period_name,
        "date": parse_timestamp_to_date(sorted_entries[0].timestamp).isoformat(),
        "total_entries": total_entries,
        "occupied_entries": occupied_entries,
        "occupancy_percentage": round(occupancy_percentage, 1),
        "occupancy_trend": hourly_trend
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

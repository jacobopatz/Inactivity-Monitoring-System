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

# @app.route('/summary/daily', methods=['GET'])
# def get_daily_summary():
#     """Returns a summary of today's bed occupancy data."""
#     today = date.today()
#     entries = BedEntry.query.all()
#     print("yikes")
#     today_entries = [
#         entry for entry in entries 
#         if entry.start_time.date() == date.today()
#     ]
    
#     return jsonify(calculate_summary(today_entries, "Today"))

# @app.route('/summary/weekly', methods=['GET'])
# def get_weekly_summary():
#     """Returns a summary of the past 7 days of bed occupancy data."""
#     entries = BedEntry.query.all()
    
#     # Group entries by date
#     daily_entries = defaultdict(list)
#     for entry in entries:
#         entry_date = entry.start_time.date()
#         if entry_date >= date.today() - timedelta(days=6):
#             daily_entries[entry_date].append(entry)
    
#     # Create summary for each of the last 7 days
#     summary = []
#     for day_offset in range(6, -1, -1):  # From 6 days ago to today
#         day = date.today() - timedelta(days=day_offset)
#         day_entries = daily_entries.get(day, [])
#         day_name = day.strftime("%A")
        
#         if day_offset == 0:
#             day_display = "Today"
#         elif day_offset == 1:
#             day_display = "Yesterday"
#         else:
#             day_display = day_name
            
#         summary.append(calculate_summary(day_entries, day_display))
    
#     return jsonify(summary)
# # get graphable minutes in bed for given day
# def  build_daily_bed_minutes(entries):
#     total_minutes_occupied = 0
#     bed_occupancy_by_minute = [0] * 1440
#     day_start = datetime(target_day.year, target_day.month, target_day.day)
#     day_end = day_start + timedelta(days=1)

#     for entry in entries:
#         entry_start = entry['start_time']
#         entry_end = entry_start + timedelta(seconds=entry['duration_seconds'])
        
#         if entry_end <= day_start or entry_start >= day_end:
#             continue  # no overlap
        
#         effective_start = max(entry_start, day_start)
#         effective_end = min(entry_end, day_end)
        
#         start_minute = int((effective_start - day_start).total_seconds() // 60)
#         end_minute = int((effective_end - day_start).total_seconds() // 60)
        
#         for minute in range(start_minute, end_minute + 1):
#             if 0 <= minute < 1440:
#                 bed_occupancy_by_minute[minute] = 1
#                 total_minutes_occupied += 1
#     occupancy_percentage = total_minutes_occupied/len(bed_occupancy_by_minute)
#     return (bed_occupancy_by_minute,occupancy_percentage)
# def calculate_summary(entries, period_name):
#     """Calculate summary statistics for a set of entries."""
#     if not entries:
#         return {
#             "period": period_name,
#             "date": date.today().isoformat(),
#             "total_entries": 0,
#             "occupied_entries": 0,
#             "occupancy_percentage": 0,
#             "occupancy_trend": []
#         }
    
#     # Sort entries by start_time
#     sorted_entries = sorted(entries, key=lambda x: x.start_time)
    
#     # Calculate basic stats
#     target_day = sorted_entries[0].start_time,date()
#     bed_occupancy_by_minute, occupancy_percentage = build_daily_bed_minutes(sorted_entries,target_day)
#     total_entries = len(sorted_entries)
#     occupied_total_seconds = sum(entry.duration_seconds for entry in sorted_entries)
#     occupied_hours = int(seconds // 3600)
#     occupied_minutes= int((seconds % 3600) // 60)
#     occupied_seconds = int(seconds % 60)
#     # occupancy_percentage = (occupied_entries / total_entries) * 100 if total_entries > 0 else 0
    
#     # # Calculate hourly trend (simplified)
#     # hourly_trend = []
#     # for hour in range(24):
#     #     hour_entries = [
#     #         entry for entry in sorted_entries
#     #         if datetime.fromisoformat(entry.start_time).hour == hour
#     #     ]
#     #     hour_occupied = sum(1 for entry in hour_entries if entry.person_detected)
#     #     hour_total = len(hour_entries)
#     #     hour_percentage = (hour_occupied / hour_total * 100) if hour_total > 0 else 0
#     #     hourly_trend.append({
#     #         "hour": hour,
#     #         "occupancy_percentage": round(hour_percentage, 1)
#     #     })
    
#     return {
#         "period": period_name,
#         "date": target_day,
#         "total_entries": total_entries,
#         "occupied_entries": occupied_entries,
#         "occupancy_percentage": occupancy_percentage,
#         'bed_occupancy_by_minute': bed_occupancy_by_minute
#     }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

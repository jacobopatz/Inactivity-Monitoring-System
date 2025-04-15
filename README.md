# BedRotTracker
# Bed Rot Tracker

## Overview
Bed Rot Tracker is a full-stack application that uses a **Flask** backend and a **React** frontend to track how long a person stays in bed using a camera connected to a Raspberry Pi. The collected data is sent wirelessly and displayed in a React dashboard.

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** React (JavaScript)
- **Database:** SQLite
- **Server Deployment:** Raspberry Pi
- **Visualization:** Recharts

---

## Installation & Setup
### **Backend (Flask API)**
#### **1. Install Python dependencies**
Ensure you have Python installed (3.8+ recommended). Install the required libraries:

```bash
cd backend
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate (Linux/macOS)
venv\Scripts\activate  # Activate (Windows)

pip install -r requirements.txt  # Install dependencies
```

#### **2. Run the Flask server**
Modify the `app.py` file if necessary and start the backend server:
```bash
python app.py
```
If running on a Raspberry Pi, you may need to start it with:
```bash
FLASK_APP=app.py flask run --host=0.0.0.0
```
The API will be available at:
```
http://<your-server-ip>:5000
```
Make sure to replace `<your-server-ip>` with the actual IP (e.g., `192.168.1.67`).

---

### **Frontend (React Dashboard)**
#### **1. Install Node.js dependencies**
Ensure you have Node.js (16+ recommended). Then install the frontend dependencies:

```bash
cd frontend
npm install
```

#### **2. Configure API Endpoint**
Modify `BedTimeDashboard.js` to use your Flask server's IP:
```javascript
axios.get("http://<your-server-ip>:5000/data")
```
Replace `<your-server-ip>` with your actual backend server IP.

#### **3. Run the React frontend**
Start the frontend development server:
```bash
npm start
```
The dashboard will be available at:
```
http://localhost:3000
```

---

## Troubleshooting
### **Common Issues & Fixes**
- **Backend not starting?**
  - Ensure Flask is installed and you’re in the correct virtual environment.
  - Check if another process is using port 5000 (`lsof -i :5000` on macOS/Linux).
- **React app not connecting to backend?**
  - Ensure the backend is running and accessible from the frontend machine.
  - Check CORS errors in the browser console and update Flask settings if needed.
- **Database issues?**
  - Delete `backend/instance/bed_data.db` and restart the backend.

---

## Future Improvements
- Implement user authentication
- Store data in a cloud database instead of SQLite
- Improve UI design with more detailed analytics

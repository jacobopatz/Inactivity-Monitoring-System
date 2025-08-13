# Inactivity Monitoring System

A personal inactivity monitoring system that leverages computer vision, IoT, and web technologies to track and visualize periods of inactivity. The system consists of:

- **Raspberry Pi** with a camera and YOLO-based visual detection for person presence.
- **Flask** backend with an SQLAlchemy database for data storage and API endpoints.
- **React** frontend for an interactive dashboard and visualization.

## Overview

The project is divided into three main components:

### 1. `picamera/` — Raspberry Pi Detection Module
- Runs Python scripts directly on a Raspberry Pi connected to a camera.
- Utilizes the **YOLO** object detection model to identify the presence of a person in the camera’s view.
- Processes detection results locally and sends boolean values (`person_detected = True/False`) to the backend via secure **HTTP requests**.
- Designed to run continuously and efficiently on Raspberry Pi hardware.

### 2. `backend/` — Flask API and Database
- Built with **Flask** to serve as the communication bridge between the Raspberry Pi and the frontend dashboard.
- Stores detection events in a **SQLAlchemy**-managed relational database.
- Parses and validates incoming data from the Raspberry Pi before committing it to the database.
- Provides RESTful API endpoints for data retrieval by the frontend.

### 3. `frontend/` — React Dashboard
- Implements a clean, responsive UI for the end user.
- Fetches data from the Flask backend to display inactivity patterns and statistics.
- Offers visualizations of **time spent inactive**, such as periods spent in locations (e.g., couch) associated with inactivity.
- Designed with usability in mind, providing actionable insights into personal activity levels.

## Technology Stack

**Hardware**
- Raspberry Pi with camera module

**Backend**
- Python
- Flask
- SQLAlchemy
- YOLO (via Python)

**Frontend**
- React
- JavaScript (ES6+)
- CSS/HTML

**Communication**
- Secure HTTP requests between Raspberry Pi and Flask API

## Project Structure

```text
inactivity-monitoring-system/
│
├── picamera/   # Raspberry Pi detection scripts (YOLO processing + HTTP requests)
├── backend/    # Flask API and SQLAlchemy database integration
└── frontend/   # React-based dashboard UI
```

## How It Works

1. **Detection** — The Raspberry Pi Captures a photo at an interval decided by the user, runs yolo detection on this image, and decides whether a person is present or not. 
2. **Data Transmission** — Each detection result is sent via an HTTP POST request to the backend. No image is ever sent and only exists momentarily on the rasberry pi.
3. **Storage** — The Flask backend processes the request and records the detection event in the SQLAlchemy database.
4. **Visualization** — The React frontend fetches the data and displays an interactive dashboard showing inactivity trends.

## Potential Applications
- Personal wellness tracking
- Productivity improvement
- Health-related inactivity monitoring

---

**Note:** This project is for personal and educational purposes. When deploying in real environments, ensure compliance with privacy laws and ethical data practices.
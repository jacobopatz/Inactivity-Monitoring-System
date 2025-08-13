import React, { useEffect, useState } from "react";
import axios from "axios";
import "./BedTimeDashboard.css";
import { useNavigate } from "react-router-dom";

const BedTimeDashboard = () => {
  const [data, setData] = useState([]);
  const nav = useNavigate();
  const [isInBed, setIsInBed] = useState(false);

  useEffect(() => {
    axios.get("https://inactivity-monitoring-system-backend.onrender.com/data")
      .then((res) => {
        if (Array.isArray(res.data)) {
          setData(res.data);
          const lastEntry = res.data[res.data.length - 1];
          setIsInBed(lastEntry.person_detected);
        } else {
          console.error("Unexpected response format:", res.data);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="dashboard-container">
      <div className="card">
        <h1 className="header">Inactivity Tracker </h1>
        <p className="description">Track daily inactivity</p>

        <div className="button-container">
          <button onClick={() => nav("/log")}>📘 Log</button>
          <button onClick={() => nav("/info")}>📊 Stats</button>
        </div>

        <div className="status-section">
          <p className="status-label">Currently in Bed?</p>
          <div className={`status-pill ${isInBed ? "in-bed" : "out-of-bed"}`}>
            {isInBed ? "Yes 😴" : "No 😃"}
          </div>
        </div>

        <img
          src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExenZqNnVwMndxcWpsbmJneGJ4Ynl0NmkzcXB0amQ1end2aWo0MzFjdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wagHaQhJNaugXh3Zw6/giphy.gif"
          alt="Sleeping"
          className="sleep-gif"
        />
      </div>
    </div>
  );
};

export default BedTimeDashboard;

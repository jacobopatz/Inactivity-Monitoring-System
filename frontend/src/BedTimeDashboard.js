import React, { useEffect, useState } from "react";
import axios from "axios";
import "./BedTimeDashboard.css"; 
import {useNavigate} from "react-router-dom";

const BedTimeDashboard = () => {
  const [data, setData] = useState([]);
  const nav = useNavigate();
  const [isInBed, setIsInBed] = useState(false);
  
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/data") // Data url
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
    <div  className="dashboard-container">

      {/* Title */}
      <h1 className="header">Bed Time Tracking 🛌 </h1>
      <p className="description">
        Track your time in bed! 
      </p>
      
      {/* Buttons to other pages */}
      <div className="button-container">
      <button onClick={() => nav("/log")}>
          Log
      </button>
      
      <button onClick={() => nav("/info")}>
          Stats & Info
      </button>
      </div>

      {/* Current Status */}
      <div className="header">
        <p className="description">Currently In Bed? </p>
                <div className={`status ${isInBed ? "in-bed" : "out-of-bed"}`}>
                  {isInBed ? "Yes" : "No"}
                </div>
      </div>
      
      {/* Gif */}
      <img
        src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExenZqNnVwMndxcWpsbmJneGJ4Ynl0NmkzcXB0amQ1end2aWo0MzFjdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wagHaQhJNaugXh3Zw6/giphy.gif"
        alt="Bed"
        className="bed-image"
      />
    </div>
  );
};

export default BedTimeDashboard;

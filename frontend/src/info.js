import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";
import "./info.css";


// tooltip behavior for the bar chart when hovered over
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const totalMinutes = payload[0].value;
    const hours = Math.floor(totalMinutes / 60);
    const minutes = Math.round(totalMinutes % 60);

    return (
      <div className="custom-tooltip" style={{ backgroundColor: "#fff", border: "1px solid #ccc", padding: "8px" }}>
        <p className="label">{label}</p>
        <p className="intro">
          {hours} hour{hours !== 1 ? "s" : ""} {minutes} minute{minutes !== 1 ? "s" : ""}
        </p>
      </div>
    );
  }

  return null;
};

function Info() {
  const nav = useNavigate();
  
  const [dailyStats, setDailyStats] = useState([]);
  const [todayTime, setTodayTime] = useState(0);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/data")
      .then((res) => {
        const raw = res.data;
        const durations = {};
        const today = new Date();
        const todayString = today.toISOString().split("T")[0];
        let todayTotal = 0;
        let i = 0;

        while (i < raw.length){
          if (raw[i].person_detected) {
            let j = i + 1;
            while (j < raw.length && raw[j].person_detected) j++;
            
            if (j < raw.length && !raw[j].person_detected) {
              const start = new Date(raw[i].timestamp);
              const end = new Date(raw[j].timestamp);
              const duration = (end - start) / (1000 * 60); // in minutes
              
              const day = start.toLocaleDateString("en-US", { weekday: "short" });
              durations[day] = (durations[day] ||0) + duration;

              if (start.toISOString().split("T")[0] === todayString) {
                todayTotal += duration;
              }

              i = j + 1; // Move to the next non-person detected entry
            } else{
              break;
            }
          } else {
            i++;
          }
        }

        const r = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map(day => ({
          day,
          duration: durations[day] || 0
        }));

        setDailyStats(r);
        setTodayTime(todayTotal);
      });
    }, []);

  return (
    <div className = "info-container" style={{ width: "100%", height: 300 }}>
        <div className = "stat-text">
          Total time in bed today: {Math.floor(todayTime / 60)} hours {Math.round(todayTime % 60)} minutes 
              {/* Uncomment the following lines to display daily stats */}
              {/* {dailyStats.map((stat) => (
                  <div key={stat.day}>
                      {stat.day}: {stat.duration} minutes
                  </div>
              ))} */}
        </div>
        <div className = "stat-text">
          Average time in bed this week: {Math.floor(dailyStats.reduce((acc, stat) => acc + stat.duration, 0) / 7)} minutes
        </div>

        {/* Bar chart for daily stats */}
        <div style={{ width: "100%", height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={dailyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis label = {{ value: "Minutes", angle: -90, position:"insideLeft"}}/>
              <Tooltip content={<CustomTooltip/>} /> {/* Custom tooltip behavior*/}
              <Bar dataKey="duration" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
            
        {/* Button to go back to home */}
        <button className="back-button" onClick={() => nav("/")}>
          Back to Home
        </button>
    </div>
  );
}

export default Info;

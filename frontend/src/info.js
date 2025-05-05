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
  const [weekOffset, setWeekOffset] = useState(0); //set which week you're viewing
  useEffect(() => {
    axios.get("http://127.0.0.1:1/data")
      .then((res) => {
        const raw = res.data;
        const durations = {};
        const today = new Date();
        const baseDay = new Date();
        today.setDate(today.getDate()); // shift back by 7 days * offset
        baseDay.setDate(baseDay.getDate() - (7 * weekOffset)); //this day allows for checking past weeks
        const todayString = today.toLocaleDateString('en-CA').split("T")[0];
        const days = [];
        
       
       
        
        
        for (let i = 6; i >= 0; i--) {
          const d = new Date(baseDay);  // fresh copy every loop
          d.setDate(baseDay.getDate() - i);
          days.push(d.toLocaleDateString('en-CA').split("T")[0]);
        }
        
        days.forEach(dateStr => {
          durations[dateStr] = 0;  // Initialize all the dates you're displaying
        });
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
              
              const startDate = start.toLocaleDateString('en-CA').split("T")[0];
              //group by date string instead of day name, allows checking for past weeks
              if (durations.hasOwnProperty(startDate)) {
                durations[startDate] += duration;
              }

              if (start.toLocaleDateString('en-CA').split("T")[0] === todayString) {
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
        
        const r = days.map(dateStr => {
          const d = new Date(dateStr);
          const label = new Date(dateStr).toLocaleDateString("en-US", { weekday: "short" } + " " + (d.getMonth() + 1) + "/" + d.getDate());
          return { day: label, duration: durations[dateStr] };
        });
        

        setDailyStats(r);
        setTodayTime(todayTotal);
      });
    }, [weekOffset]);

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
        {/* add button to toggle week*/}
        <div className="week-nav-buttons">
          <button onClick={() => setWeekOffset(prev => prev + 1)}>← Previous Week</button>
          <button onClick={() => setWeekOffset(prev => Math.max(0, prev - 1))} disabled={weekOffset === 0}>
            Next Week → 
          </button>
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

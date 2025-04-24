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

function Info() {
  const nav = useNavigate();
  const [dailyStats, setDailyStats] = useState([
    { day: "Mon", duration: 0 },
    { day: "Tue", duration: 0 },
    { day: "Wed", duration: 0 },
    { day: "Thu", duration: 0 },
    { day: "Fri", duration: 0 },
    { day: "Sat", duration: 0 },
    { day: "Sun", duration: 0},
  ]);

  const [todayTime, setTodayTime] = useState(0);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/data")
      .then((res) => {
        const raw = res.data;
        const durations = [];
        const today = new Date();
        const todayString = today.toISOString().split("T")[0];
        let todayTotal = 0;
        

        for (let i = 0; i < raw.length -1; i++) {
            if(raw[i].person_detected && !raw[i + 1].person_detected) {
                const start = new Date(raw[i].timestamp);
                const end = new Date(raw[i + 1].timestamp);
                const duration = (end - start) / (1000 * 60); // in minutes
                
                durations.push({
                    date: start.toISOString().split("T")[0],
                    duration: duration
                });
                
                if (start.toISOString().split("T")[0] === todayString) {
                    todayTotal += duration;
                }
            }
         }
         
        setDailyStats(durations);
        setTodayTime(todayTotal);
    });
    }, []);

  return (
    <div style={{ width: "100%", height: 300 }}>
            <div>
                Total time in bed today: {todayTime} minutes
            </div>
            
        <button onClick={() => nav("/")}>
        Back to Home
        </button>
    </div>
  );
}

export default Info;

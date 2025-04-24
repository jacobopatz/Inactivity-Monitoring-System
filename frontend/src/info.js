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
        const durations = {};
        const today = new Date();
        const todayString = today.toISOString().split("T")[0];
        let todayTotal = 0;
        let i = 0;

        while (i < raw.length){
          if (raw[i].person_detected) {
            let j = i + 1;
            while (j < raw.length && raw[j].person_detected) {
              j++;
            }
            
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
    <div style={{ width: "100%", height: 300 }}>
            <div>
                Total time in bed today: {todayTime} minutes

                {/* Uncomment the following lines to display daily stats */}
                {/* {dailyStats.map((stat) => (
                    <div key={stat.day}>
                        {stat.day}: {stat.duration} minutes
                    </div>
                ))} */}
            </div>
            <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dailyStats}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis label = {{ value: "Minutes", angle: -90, position:"insideLeft"}}/>
                    <Tooltip />
                    <Bar dataKey="duration" fill="#8884d8" />
                </BarChart>
            </ResponsiveContainer>
            </div>
            
        <button onClick={() => nav("/")}>
        Back to Home
        </button>
    </div>
  );
}

export default Info;

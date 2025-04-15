import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import "./BedTimeDashboard.css"; 

const BedTimeDashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000") // Update with your actual Flask server URL
      .then((res) => {
        if (Array.isArray(res.data)) {
          setData(res.data);
        } else {
          console.error("Unexpected response format:", res.data);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="dashboard-container">
      <h2 className="header">Bed Time Tracking</h2>
      {data.length > 0 ? (
        <LineChart width={600} height={300} data={data}>
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <CartesianGrid stroke="#ccc" />
          <Line type="monotone" dataKey="duration" stroke="#8884d8" />
        </LineChart>
      ) : (
        <p>Loading data or no records available...</p>
      )}
    </div>
  );
};

export default BedTimeDashboard;


import React, {useEffect, useState} from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./log.css";

function Log() {
    const [logData, setLogData] = useState([]);
    const nav = useNavigate();
    
    useEffect(() => {
        axios.get("https://inactivity-monitoring-system-backend.onrender.com/data") // Fetching data
          .then((res) => {
            if (Array.isArray(res.data)) {
              //show newest entries first
              const reversedData = res.data.slice().reverse();
              setLogData(reversedData);
            } else {
              console.error("Unexpected response format:", res.data);
            }
          })
          .catch((err) => console.error("Error fetching data:", err));
      }, []);

    return(
        <div className="log-container">
          <h1 className="log-header">Camera Detection Log</h1>
          <div className="log-list"> 
          
            {/* Log entries */}
            {logData.length > 0 ? (
              logData.map((entry, index) => (
                <div key={index} className="log-entry">
                  <div className="timestamp">{new Date(entry.timestamp).toLocaleString()}</div>
                  <div className={`status ${entry.person_detected ? "in-bed" : "out-of-bed"}`}>
                      {entry.person_detected ? "In bed" : "Out of bed"}
                  </div>
                </div>
            ))
        ) : (
          // if logData is empty
          <p>No log entries found.</p>
        )}
          </div>
        
        {/* Button to go back to home */}
        <button className="back-button" onClick={() => nav("/")}>
            Back to Home
        </button>
        </div>
    );
}
  export default Log;
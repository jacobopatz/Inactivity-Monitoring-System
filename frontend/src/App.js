import React from "react";
import BedTimeDashboard from "./BedTimeDashboard";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Log from "./log";
import Info from "./info";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<BedTimeDashboard />} />
        <Route path="/log" element={<Log />} />
        <Route path="/info" element={<Info />} />
      </Routes>
    </Router>
  
  );
}


export default App;

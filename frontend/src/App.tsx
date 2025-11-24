import React from "react";
import { Route, Routes } from "react-router-dom";
import AdminPage from "./pages/Admin/AdminPage";
import DashboardPage from "./pages/Dashboard/DashboardPage";
import RiskReport from "./pages/RiskReport/RiskReportPage";
import TenderPage from "./pages/Tender/TenderPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/risk-report" element={<RiskReport />} />
      <Route path="/tender" element={<TenderPage />} />
      <Route path="/admin" element={<AdminPage />} />
    </Routes>
  );
}

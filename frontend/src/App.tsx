import React from "react";
import { Route, Routes } from "react-router-dom";
import DashboardPage from "./pages/Dashboard/DashboardPage";
import TenderPage from "./pages/Tender/TenderPage";
import TenderListPage from "./pages/Tender/TenderListPage";
import NotFoundPage from "./pages/NotFound/NotFoundPage";
import Layout from "./components/Layout";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/tender/:id" element={<TenderPage />} />
        <Route path="/tenders" element={<TenderListPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Layout>
  );
}

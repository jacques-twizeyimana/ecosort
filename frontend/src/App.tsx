import { useState } from "react";
import {
  LayoutDashboard,
  Upload as UploadIcon,
  RefreshCw,
  Leaf,
} from "lucide-react";
import Dashboard from "./components/Dashboard";
import Predict from "./components/Predict";
import Retrain from "./components/Retrain";

function App() {
  const [activeTab, setActiveTab] = useState<
    "dashboard" | "predict" | "retrain"
  >("dashboard");

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-gray-800 border-r border-gray-700 p-6">
        <div className="flex items-center gap-3 mb-10">
          <div className="p-2 bg-green-500 rounded-lg">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
            EcoSort
          </h1>
        </div>

        <nav className="space-y-2">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              activeTab === "dashboard"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30"
                : "text-gray-400 hover:bg-gray-700 hover:text-white"
            }`}
          >
            <LayoutDashboard className="w-5 h-5" />
            Dashboard
          </button>

          <button
            onClick={() => setActiveTab("predict")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              activeTab === "predict"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30"
                : "text-gray-400 hover:bg-gray-700 hover:text-white"
            }`}
          >
            <UploadIcon className="w-5 h-5" />
            Predict
          </button>

          <button
            onClick={() => setActiveTab("retrain")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              activeTab === "retrain"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30"
                : "text-gray-400 hover:bg-gray-700 hover:text-white"
            }`}
          >
            <RefreshCw className="w-5 h-5" />
            Retrain
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <main className="ml-64 p-8">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold text-white">
              {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}
            </h2>
            <p className="text-gray-400 mt-1">
              {activeTab === "dashboard" &&
                "Overview of model performance and metrics"}
              {activeTab === "predict" && "Classify waste items in real-time"}
              {activeTab === "retrain" && "Update the model with new data"}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 rounded-full border border-gray-700">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm text-gray-300">System Online</span>
            </div>
          </div>
        </header>

        <div className="animate-fade-in">
          {activeTab === "dashboard" && <Dashboard />}
          {activeTab === "predict" && <Predict />}
          {activeTab === "retrain" && <Retrain />}
        </div>
      </main>
    </div>
  );
}

export default App;

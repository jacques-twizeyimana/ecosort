import { useState } from "react";
import { RefreshCw, Upload, Check, AlertTriangle } from "lucide-react";
import axios from "axios";

function Retrain() {
  const [isRetraining, setIsRetraining] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [files, setFiles] = useState<FileList | null>(null);
  const [category, setCategory] = useState<"Organic" | "Recyclable">(
    "Recyclable"
  );

  const handleUpload = async () => {
    if (!files || files.length === 0) return;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      setUploadStatus("Uploading...");
      await axios.post(
        `http://localhost:8000/upload?category=${category}`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setUploadStatus(
        `Successfully uploaded ${files.length} images to ${category}`
      );
      setFiles(null);
    } catch (err) {
      console.error(err);
      setUploadStatus("Upload failed.");
    }
  };

  const handleRetrain = async () => {
    try {
      setIsRetraining(true);
      await axios.post("http://localhost:8000/retrain");
      // In a real app, we'd poll for status. Here we just show a message.
      setTimeout(() => setIsRetraining(false), 2000); // Simulate immediate ack
    } catch (err) {
      console.error(err);
      setIsRetraining(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Upload Section */}
      <div className="card">
        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <Upload className="w-6 h-6 text-blue-500" />
          Upload New Training Data
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <label className="block text-sm font-medium text-gray-400">
              Select Category
            </label>
            <div className="flex gap-4">
              <button
                onClick={() => setCategory("Organic")}
                className={`flex-1 py-3 px-4 rounded-lg border transition-all ${
                  category === "Organic"
                    ? "bg-orange-500/20 border-orange-500 text-orange-400"
                    : "bg-gray-700 border-gray-600 text-gray-400 hover:bg-gray-600"
                }`}
              >
                Organic
              </button>
              <button
                onClick={() => setCategory("Recyclable")}
                className={`flex-1 py-3 px-4 rounded-lg border transition-all ${
                  category === "Recyclable"
                    ? "bg-green-500/20 border-green-500 text-green-400"
                    : "bg-gray-700 border-gray-600 text-gray-400 hover:bg-gray-600"
                }`}
              >
                Recyclable
              </button>
            </div>

            <div className="relative">
              <input
                type="file"
                multiple
                onChange={(e) => setFiles(e.target.files)}
                className="block w-full text-sm text-gray-400
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-600 file:text-white
                  hover:file:bg-blue-700
                  cursor-pointer"
              />
            </div>

            <button
              onClick={handleUpload}
              disabled={!files}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Upload Files
            </button>

            {uploadStatus && (
              <p
                className={`text-sm ${
                  uploadStatus.includes("failed")
                    ? "text-red-400"
                    : "text-green-400"
                }`}
              >
                {uploadStatus}
              </p>
            )}
          </div>

          <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
            <h4 className="text-sm font-medium text-gray-400 mb-4">
              Instructions
            </h4>
            <ul className="space-y-2 text-sm text-gray-500">
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-green-500 mt-0.5" />
                Upload clear images of waste items
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-green-500 mt-0.5" />
                Ensure correct category selection
              </li>
              <li className="flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 text-yellow-500 mt-0.5" />
                Avoid uploading blurry or multiple items
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Retrain Section */}
      <div className="card border-blue-500/30">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
              <RefreshCw className="w-6 h-6 text-blue-500" />
              Model Retraining
            </h3>
            <p className="text-gray-400">
              Trigger a new training session with the latest uploaded data
            </p>
          </div>

          <button
            onClick={handleRetrain}
            disabled={isRetraining}
            className={`px-6 py-3 rounded-lg font-medium transition-all flex items-center gap-2 ${
              isRetraining
                ? "bg-blue-600/50 cursor-wait"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            <RefreshCw
              className={`w-5 h-5 ${isRetraining ? "animate-spin" : ""}`}
            />
            {isRetraining ? "Retraining Started..." : "Start Retraining"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Retrain;

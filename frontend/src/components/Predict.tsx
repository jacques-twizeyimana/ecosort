import { useState, useRef } from "react";
import { Upload, X, CheckCircle, AlertCircle, Loader2 } from "lucide-react";
import axios from "axios";

function Predict() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{
    label: string;
    confidence: number;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
      setError(null);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith("image/")) {
      setFile(droppedFile);
      setPreview(URL.createObjectURL(droppedFile));
      setResult(null);
      setError(null);
    }
  };

  const handlePredict = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Assuming API is running on localhost:8000
      const response = await axios.post(
        "http://localhost:8000/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to get prediction. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const clearSelection = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="card">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-white mb-2">
            Waste Classification
          </h2>
          <p className="text-gray-400">
            Upload an image to identify if it's Organic or Recyclable
          </p>
        </div>

        {!preview ? (
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            className="border-2 border-dashed border-gray-600 rounded-xl p-12 text-center hover:border-blue-500 transition-colors cursor-pointer bg-gray-800/50"
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Upload className="w-8 h-8 text-blue-500" />
            </div>
            <h3 className="text-lg font-medium text-white mb-2">
              Click to upload or drag and drop
            </h3>
            <p className="text-sm text-gray-400">
              SVG, PNG, JPG or GIF (max. 800x400px)
            </p>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
            />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="relative rounded-xl overflow-hidden bg-black/50 aspect-video flex items-center justify-center">
              <img
                src={preview}
                alt="Preview"
                className="max-h-full max-w-full object-contain"
              />
              <button
                onClick={clearSelection}
                className="absolute top-4 right-4 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex justify-center">
              {!result ? (
                <button
                  onClick={handlePredict}
                  disabled={loading}
                  className="btn-primary flex items-center gap-2 px-8 py-3 text-lg"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Upload className="w-5 h-5" />
                      Analyze Image
                    </>
                  )}
                </button>
              ) : (
                <div
                  className={`flex items-center gap-4 px-6 py-4 rounded-xl border ${
                    result.label === "Recyclable"
                      ? "bg-green-500/10 border-green-500/50 text-green-400"
                      : "bg-orange-500/10 border-orange-500/50 text-orange-400"
                  }`}
                >
                  {result.label === "Recyclable" ? (
                    <CheckCircle className="w-8 h-8" />
                  ) : (
                    <AlertCircle className="w-8 h-8" />
                  )}
                  <div className="text-left">
                    <p className="text-sm opacity-80">Prediction Result</p>
                    <h3 className="text-2xl font-bold">{result.label}</h3>
                    <p className="text-sm opacity-80">
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              )}
            </div>

            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-center">
                {error}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Predict;

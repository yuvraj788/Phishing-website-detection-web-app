import { useState } from "react";
import UrlForm from "./components/UrlForm";
import ResultCard from "./components/ResultCard";
import FeatureTable from "./components/FeatureTable";
import Loader from "./components/Loader";
import { predictUrl } from "./services/api";
import "./index.css";

function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handlePredict = async (url) => {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await predictUrl(url);
      setResult(response);
    } catch (err) {
      setError(
        err?.response?.data?.error || "Something went wrong while checking the URL."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResult(null);
    setError("");
  };

  return (
    <div className="app-shell">
      <div className="bg-glow bg-glow-1"></div>
      <div className="bg-glow bg-glow-2"></div>

      <div className="container">
        <div className="hero-card">
          <p className="section-tag">Cyber Security Analyzer</p>
          <h1 className="hero-title">Phishing Website Detection</h1>
          <p className="hero-subtitle">
            Analyze a URL using URL-based and webpage-based phishing indicators.
          </p>

          <UrlForm onPredict={handlePredict} onClear={handleClear} loading={loading} />

          {error && <div className="error-box">{error}</div>}
        </div>

        {loading && <Loader />}

        {!loading && <ResultCard result={result} />}
        {!loading && <FeatureTable result={result} />}
      </div>
    </div>
  );
}

export default App;
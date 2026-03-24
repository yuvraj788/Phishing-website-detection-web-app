import { useState } from "react";

function UrlForm({ onPredict, onClear, loading }) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url.trim()) return;
    onPredict(url.trim());
  };

  const handleClear = () => {
    setUrl("");
    onClear();
  };

  return (
    <form className="url-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter suspicious or legitimate website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="url-input"
      />

      <button type="submit" className="primary-btn" disabled={loading}>
        {loading ? "Checking..." : "Check URL"}
      </button>

      <button type="button" className="secondary-btn" onClick={handleClear}>
        Clear
      </button>
    </form>
  );
}

export default UrlForm;
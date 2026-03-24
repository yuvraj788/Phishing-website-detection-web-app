function ResultCard({ result }) {
  if (!result) return null;

  const { label, risk_level, probability, url } = result.data;
  const probabilityPercent =
    probability !== null && probability !== undefined
      ? `${(probability * 100).toFixed(0)}%`
      : "N/A";

  const isPhishing = label === "Phishing";

  return (
    <div className={`result-card ${isPhishing ? "danger-card" : "safe-card"}`}>
      <div className="result-header">
        <div>
          <p className="section-tag">Prediction Result</p>
          <h2>{isPhishing ? "Phishing Alert!" : "Website Looks Legitimate"}</h2>
        </div>

        <div className={`status-badge ${isPhishing ? "high-risk" : "low-risk"}`}>
          {risk_level} Risk
        </div>
      </div>

      <div className="result-grid">
        <div className="result-item">
          <span>URL</span>
          <strong>{url}</strong>
        </div>

        <div className="result-item">
          <span>Prediction</span>
          <strong>{label}</strong>
        </div>

        <div className="result-item">
          <span>Risk Level</span>
          <strong>{risk_level}</strong>
        </div>

        <div className="result-item">
          <span>Confidence</span>
          <strong>{probabilityPercent}</strong>
        </div>
      </div>

      <div className="risk-meter">
        <div className="risk-meter-labels">
          <span>Low</span>
          <span>Medium</span>
          <span>High</span>
        </div>
        <div className="risk-bar">
          <div
            className={`risk-fill ${isPhishing ? "risk-fill-high" : "risk-fill-low"}`}
          ></div>
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
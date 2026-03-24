function FeatureTable({ result }) {
  if (!result) return null;

  const features = result.data.features;
  const entries = Object.entries(features);

  const formatValue = (value) => {
    if (value === 1) return "Safe / Positive";
    if (value === 0) return "Neutral";
    if (value === -1) return "Suspicious";
    return value;
  };

  const getValueClass = (value) => {
    if (value === 1) return "value-safe";
    if (value === 0) return "value-neutral";
    if (value === -1) return "value-danger";
    return "";
  };

  const formatFeatureName = (name) => {
    const customNames = {
      having_IP_Address: "IP Address Usage",
      URL_Length: "URL Length",
      Shortining_Service: "URL Shortening Service",
      having_At_Symbol: "@ Symbol in URL",
      double_slash_redirecting: "Double Slash Redirecting",
      Prefix_Suffix: "Prefix / Suffix in Domain",
      having_Sub_Domain: "Subdomain Presence",
      SSLfinal_State: "SSL Final State",
      Favicon: "Favicon Source",
      HTTPS_token: "HTTPS Token in Domain",
      Request_URL: "Request URL Signals",
      URL_of_Anchor: "Anchor URL Behavior",
      Links_in_tags: "Links in Tags",
      SFH: "Server Form Handler",
      Submitting_to_email: "Submitting to Email",
      Abnormal_URL: "Abnormal URL",
      Redirect: "Redirect Behavior",
      on_mouseover: "Mouseover Behavior",
      RightClick: "Right Click Disabled",
      popUpWidnow: "Popup Window",
      Iframe: "Iframe Usage",
    };

    return customNames[name] || name.replace(/_/g, " ");
  };

  return (
    <div className="feature-table-card">
      <div className="feature-table-header">
        <p className="section-tag">Feature Analysis</p>
        <h2>Extracted Security Signals</h2>
      </div>

      <div className="feature-grid">
        {entries.map(([key, value]) => (
          <div className="feature-box" key={key}>
            <p className="feature-name">{formatFeatureName(key)}</p>
            <p className={`feature-value ${getValueClass(value)}`}>
              {formatValue(value)}
            </p>
            <small className="feature-raw">Raw value: {value}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FeatureTable;
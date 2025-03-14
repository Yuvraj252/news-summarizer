import React, { useState } from "react";
import axios from "axios";
import { FaNewspaper } from "react-icons/fa";
import "./SummarizerApp.css"; // Import custom CSS

const SummarizerApp = () => {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async () => {
    if (!url) {
      setError("Please enter a valid URL");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:5000/summarize", {
        url,
      });
      setSummary(response.data.summary);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to summarize article");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        {/* Header */}
        <div className="header">
          <FaNewspaper className="icon" />
          <h1 className="title">News Summarizer</h1>
        </div>

        {/* Input Field */}
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter news article URL..."
          className="input"
        />

        {/* Summarize Button */}
        <button
          onClick={handleSummarize}
          className={`button ${loading ? "disabled" : ""}`}
          disabled={loading}
        >
          {loading ? "Summarizing..." : "Summarize"}
        </button>

        {/* Error Message */}
        {error && <div className="error">{error}</div>}

        {/* Summary Output */}
        {summary && (
          <div className="summary">
            <h2>Summary:</h2>
            <p>{summary}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SummarizerApp;

import React, { useState } from 'react';

const WebsiteInputStep = ({ onSubmit }) => {
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [urlError, setUrlError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic URL validation
    if (!websiteUrl) {
      setUrlError('Please enter a website URL');
      return;
    }
    
    try {
      new URL(websiteUrl);
      setUrlError('');
      onSubmit(websiteUrl);
    } catch (err) {
      setUrlError('Please enter a valid URL (e.g., https://example.com)');
    }
  };

  return (
    <div>
      <h2 className="mb-4">Enter Your Website</h2>
      <p className="mb-4">
        We'll analyze your website and identify your main competitors, then provide detailed intelligence
        about their products, social media presence, and market positioning.
      </p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group mb-4">
          <label htmlFor="websiteUrl" className="form-label">Your Website URL</label>
          <input
            type="text"
            className={`form-control ${urlError ? 'is-invalid' : ''}`}
            id="websiteUrl"
            placeholder="https://yourwebsite.com"
            value={websiteUrl}
            onChange={(e) => setWebsiteUrl(e.target.value)}
          />
          {urlError && <div className="invalid-feedback">{urlError}</div>}
          <div className="form-text mt-2">
            Enter the full URL including https:// or http://
          </div>
        </div>
        
        <div className="form-group mb-4">
          <div className="form-check">
            <input className="form-check-input" type="checkbox" id="consent" required />
            <label className="form-check-label" htmlFor="consent">
              I consent to the analysis of my website and competitors
            </label>
          </div>
        </div>
        
        <div className="d-grid">
          <button type="submit" className="btn btn-primary btn-lg">
            Analyze Website
          </button>
        </div>
      </form>
    </div>
  );
};

export default WebsiteInputStep;
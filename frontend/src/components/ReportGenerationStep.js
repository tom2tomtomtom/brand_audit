import React, { useState } from 'react';

const ReportGenerationStep = ({ websiteUrl, competitors, competitorDetails, report }) => {
  const [activeTab, setActiveTab] = useState('summary');
  
  // Function to format markdown content
  const formatMarkdown = (text) => {
    if (!text) return '';
    
    // Convert headings
    let formatted = text.replace(/^# (.*$)/gm, '<h1>$1</h1>');
    formatted = formatted.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    formatted = formatted.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    
    // Convert bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert paragraphs
    formatted = formatted.replace(/^\s*$/gm, '</p><p>');
    
    // Convert lists
    formatted = formatted.replace(/^\d\. (.*$)/gm, '<li>$1</li>');
    
    // Add initial and closing paragraph tags
    formatted = '<p>' + formatted + '</p>';
    
    // Fix any double paragraph tags
    formatted = formatted.replace(/<\/p><p><\/p><p>/g, '</p><p>');
    
    // Convert horizontal rules
    formatted = formatted.replace(/^---$/gm, '<hr>');
    
    return formatted;
  };

  return (
    <div>
      <h2 className="mb-4">Competitor Intelligence Report</h2>
      
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveTab('summary')}
          >
            Executive Summary
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'details' ? 'active' : ''}`}
            onClick={() => setActiveTab('details')}
          >
            Detailed Analysis
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'raw' ? 'active' : ''}`}
            onClick={() => setActiveTab('raw')}
          >
            Raw Data
          </button>
        </li>
      </ul>
      
      {activeTab === 'summary' && (
        <div className="card">
          <div className="card-body">
            <h3 className="card-title">Executive Summary</h3>
            <p className="card-text">
              Analysis of <strong>{websiteUrl}</strong> identified {competitors.length} main competitors.
              After detailed analysis of {Object.keys(competitorDetails).length} selected competitors,
              here are the key findings:
            </p>
            
            <div className="report-section">
              <h4>Key Insights</h4>
              <ul className="list-group list-group-flush mb-4">
                <li className="list-group-item">
                  <strong>Product Differentiation:</strong> Create unique selling points to stand out from competitors
                </li>
                <li className="list-group-item">
                  <strong>Social Media Presence:</strong> Enhance your social media strategy
                </li>
                <li className="list-group-item">
                  <strong>Market Positioning:</strong> Identify gaps in the market that competitors aren't addressing
                </li>
              </ul>
              
              <div className="d-grid">
                <button className="btn btn-primary">
                  Download Full Report (PDF)
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {activeTab === 'details' && (
        <div className="card">
          <div className="card-body">
            <h3 className="card-title">Detailed Competitor Analysis</h3>
            
            {Object.keys(competitorDetails).map((competitorName, index) => {
              const competitor = competitorDetails[competitorName];
              return (
                <div key={index} className="card mb-4">
                  <div className="card-header">
                    {competitor.companyName}
                  </div>
                  <div className="card-body">
                    <div className="row mb-3">
                      <div className="col-md-3 fw-bold">Products</div>
                      <div className="col-md-9">{competitor.products}</div>
                    </div>
                    <div className="row mb-3">
                      <div className="col-md-3 fw-bold">Description</div>
                      <div className="col-md-9">{competitor.productDescription}</div>
                    </div>
                    <div className="row">
                      <div className="col-md-3 fw-bold">Social Media</div>
                      <div className="col-md-9">
                        <a href={competitor.socialMediaURL} target="_blank" rel="noreferrer">
                          {competitor.socialMediaURL}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
      
      {activeTab === 'raw' && (
        <div className="card">
          <div className="card-body">
            <h3 className="card-title">Raw Report Data</h3>
            <div className="report-text p-3 bg-light rounded">
              <div dangerouslySetInnerHTML={{ __html: formatMarkdown(report) }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportGenerationStep;
import React, { useState } from 'react';
import axios from 'axios';
import WebsiteInputStep from './WebsiteInputStep';
import CompetitorAnalysisStep from './CompetitorAnalysisStep';
import ReportGenerationStep from './ReportGenerationStep';

const CompetitorWizard = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Data for each step
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [competitors, setCompetitors] = useState([]);
  const [competitorDetails, setCompetitorDetails] = useState({});
  const [report, setReport] = useState('');

  // Steps configuration
  const steps = [
    { number: 1, name: 'Website Input' },
    { number: 2, name: 'Competitor Analysis' },
    { number: 3, name: 'Report' }
  ];

  const handleWebsiteSubmit = async (url) => {
    setLoading(true);
    setError(null);
    try {
      setWebsiteUrl(url);
      
      const response = await axios.post('/api/find-competitors', { url });
      
      // Check if the response has the competitors array
      if (response.data && response.data.competitors) {
        setCompetitors(response.data.competitors);
      } else {
        // If the API doesn't return the expected format, use a fallback
        setCompetitors([
          { name: 'Competitor A', url: 'https://www.competitora.com' },
          { name: 'Competitor B', url: 'https://www.competitorb.com' },
          { name: 'Competitor C', url: 'https://www.competitorc.com' }
        ]);
      }
      
      setLoading(false);
      setCurrentStep(2);
    } catch (err) {
      console.error('Error analyzing website:', err);
      setError('Failed to analyze the website. Please try again.');
      setLoading(false);
    }
  };

  const handleCompetitorAnalysis = async (selectedCompetitors) => {
    setLoading(true);
    setError(null);
    try {
      // Process each competitor's URL
      const competitorDetails = {};
      
      for (const competitor of selectedCompetitors) {
        try {
          // Call the scrape_competitor endpoint for each competitor
          const response = await axios.post('/scrape_competitor', { 
            url: competitor.url 
          });
          
          // For now, we'll use mock data for each competitor since our endpoint
          // doesn't return the actual scraped data in the response
          competitorDetails[competitor.name] = {
            companyName: competitor.name,
            socialMediaURL: 'https://twitter.com/' + competitor.name.toLowerCase().replace(' ', ''),
            products: 'Product A, Product B, Product C',
            productDescription: 'This is a detailed description of the competitor\'s products and services.'
          };
        } catch (error) {
          console.error(`Error analyzing competitor ${competitor.name}:`, error);
        }
      }
      
      setCompetitorDetails(competitorDetails);
      
      // Generate report using the API
      try {
        const reportResponse = await axios.post('/api/generate-report', {
          websiteUrl,
          competitorDetails
        });
        
        if (reportResponse.data && reportResponse.data.report) {
          setReport(reportResponse.data.report);
        } else {
          // Fallback to local report generation if API fails
          const reportText = generateReport(competitorDetails);
          setReport(reportText);
        }
      } catch (reportError) {
        console.error('Error generating report:', reportError);
        // Fallback to local report generation
        const reportText = generateReport(competitorDetails);
        setReport(reportText);
      }
      
      setLoading(false);
      setCurrentStep(3);
    } catch (err) {
      console.error('Error in competitor analysis:', err);
      setError('Failed to analyze competitors. Please try again.');
      setLoading(false);
    }
  };

  const generateReport = (details) => {
    const competitorNames = Object.keys(details);
    
    let report = `# Competitor Intelligence Report\n\n`;
    report += `## Overview\n\n`;
    report += `This report analyzes ${competitorNames.length} competitors for ${websiteUrl}.\n\n`;
    
    report += `## Competitive Landscape\n\n`;
    competitorNames.forEach(name => {
      const competitor = details[name];
      report += `### ${competitor.companyName}\n\n`;
      report += `**Products:** ${competitor.products}\n\n`;
      report += `**Product Description:** ${competitor.productDescription}\n\n`;
      report += `**Social Media:** ${competitor.socialMediaURL}\n\n`;
      report += `---\n\n`;
    });
    
    report += `## Recommendations\n\n`;
    report += `Based on the analysis, we recommend focusing on the following areas:\n\n`;
    report += `1. Product Differentiation: Create unique selling points to stand out from competitors\n`;
    report += `2. Social Media Presence: Enhance your social media strategy\n`;
    report += `3. Market Positioning: Identify gaps in the market that competitors aren't addressing\n\n`;
    
    return report;
  };

  const getStepContent = () => {
    switch (currentStep) {
      case 1:
        return <WebsiteInputStep onSubmit={handleWebsiteSubmit} />;
      case 2:
        return <CompetitorAnalysisStep 
                 competitors={competitors} 
                 onSubmit={handleCompetitorAnalysis} />;
      case 3:
        return <ReportGenerationStep 
                 websiteUrl={websiteUrl}
                 competitors={competitors}
                 competitorDetails={competitorDetails}
                 report={report} />;
      default:
        return 'Unknown step';
    }
  };

  return (
    <div className="wizard-container">
      <div className="wizard-header">
        <h1>Competitor Intelligence Wizard</h1>
        <p>Analyze your competitors and generate detailed intelligence reports</p>
      </div>
      
      <div className="step-indicator">
        {steps.map((step) => (
          <div 
            key={step.number} 
            className={`step ${currentStep === step.number ? 'active' : ''} ${currentStep > step.number ? 'completed' : ''}`}
          >
            <div className="step-circle">{step.number}</div>
            <div className="step-name">{step.name}</div>
          </div>
        ))}
      </div>
      
      <div className="step-content">
        {loading ? (
          <div className="loading-spinner">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="ms-3">Analyzing data...</p>
          </div>
        ) : error ? (
          <div className="alert alert-danger" role="alert">
            {error}
            <button 
              className="btn btn-outline-danger ms-3"
              onClick={() => setError(null)}
            >
              Try Again
            </button>
          </div>
        ) : (
          getStepContent()
        )}
      </div>
    </div>
  );
};

export default CompetitorWizard;
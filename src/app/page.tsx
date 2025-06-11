'use client';

import { useState } from 'react';
import BrandInput from '@/components/BrandInput';
import AnalysisReport from '@/components/AnalysisReport';
import LoadingAnalysis from '@/components/LoadingAnalysis';

export default function HomePage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (brands: string[]) => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysisData(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ brands }),
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔍 Universal Brand Audit Tool
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Generate comprehensive visual competitor analysis reports for any brands, any industry.
            Extract logos, colors, typography, and competitive insights automatically.
          </p>
        </div>

        {/* Content */}
        {!isAnalyzing && !analysisData && (
          <BrandInput onAnalyze={handleAnalyze} />
        )}

        {isAnalyzing && (
          <LoadingAnalysis />
        )}

        {error && (
          <div className="max-w-2xl mx-auto bg-red-50 border border-red-200 rounded-lg p-6">
            <div className="flex items-center">
              <div className="text-red-600 mr-3">⚠️</div>
              <div>
                <h3 className="text-lg font-semibold text-red-800">Analysis Failed</h3>
                <p className="text-red-700">{error}</p>
                <button 
                  onClick={() => {setError(null); setAnalysisData(null);}}
                  className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        )}

        {analysisData && (
          <AnalysisReport 
            data={analysisData} 
            onNewAnalysis={() => {setAnalysisData(null); setError(null);}}
          />
        )}
      </div>
    </main>
  );
}
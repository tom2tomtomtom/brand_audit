'use client';

import { useState, useEffect } from 'react';

export default function LoadingAnalysis() {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('Initializing analysis...');

  const steps = [
    'Analyzing website structure...',
    'Extracting logos and visual assets...',
    'Analyzing color palettes...',
    'Detecting typography and fonts...',
    'Scraping content and messaging...',
    'Analyzing social media presence...',
    'Processing with AI insights...',
    'Generating competitive comparison...',
    'Finalizing comprehensive report...'
  ];

  useEffect(() => {
    let stepIndex = 0;
    let progressValue = 0;

    const interval = setInterval(() => {
      progressValue += Math.random() * 15;
      if (progressValue > 95) progressValue = 95;
      
      setProgress(progressValue);
      
      if (stepIndex < steps.length - 1 && progressValue > (stepIndex + 1) * 10) {
        stepIndex++;
        setCurrentStep(steps[stepIndex]);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8">
        {/* Main Loading Animation */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mb-4">
            <div className="w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            🔍 Analyzing Brands
          </h2>
          <p className="text-gray-600">
            Performing comprehensive visual and competitive analysis...
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-700 mb-2">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Current Step */}
        <div className="bg-blue-50 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <div className="text-blue-600 mr-3">⚡</div>
            <div>
              <p className="font-medium text-blue-900">Current Step:</p>
              <p className="text-blue-700">{currentStep}</p>
            </div>
          </div>
        </div>

        {/* Analysis Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="space-y-2">
            <h4 className="font-semibold text-gray-800">🎨 Visual Analysis</h4>
            <ul className="space-y-1 text-gray-600">
              <li>• Extracting brand logos</li>
              <li>• Analyzing color schemes</li>
              <li>• Detecting typography</li>
              <li>• Capturing screenshots</li>
            </ul>
          </div>
          <div className="space-y-2">
            <h4 className="font-semibold text-gray-800">📊 Competitive Intel</h4>
            <ul className="space-y-1 text-gray-600">
              <li>• Market positioning</li>
              <li>• Content strategy</li>
              <li>• Digital presence</li>
              <li>• Brand messaging</li>
            </ul>
          </div>
        </div>

        {/* Estimated Time */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            ⏱️ Estimated completion: 2-5 minutes
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Processing time varies based on website complexity and number of brands
          </p>
        </div>
      </div>
    </div>
  );
}
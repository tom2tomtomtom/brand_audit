'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  BarChart3, 
  Brain, 
  FileText, 
  Globe, 
  Palette, 
  Search, 
  Zap,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

export function LandingPage() {
  const features = [
    {
      icon: <Search className="h-8 w-8 text-primary" />,
      title: 'Intelligent Web Scraping',
      description: 'Automatically collect brand assets, logos, and positioning statements from competitor websites with ethical scraping practices.',
    },
    {
      icon: <Brain className="h-8 w-8 text-primary" />,
      title: 'AI-Powered Analysis',
      description: 'Leverage advanced LLM technology to analyze brand positioning, visual identity, and competitive landscape with detailed insights.',
    },
    {
      icon: <Palette className="h-8 w-8 text-primary" />,
      title: 'Visual Asset Management',
      description: 'Organize and categorize collected brand assets with automatic image optimization and intelligent tagging.',
    },
    {
      icon: <BarChart3 className="h-8 w-8 text-primary" />,
      title: 'Competitive Intelligence',
      description: 'Generate comprehensive competitive analysis reports with SWOT analysis, market positioning, and trend identification.',
    },
    {
      icon: <FileText className="h-8 w-8 text-primary" />,
      title: 'Automated Presentations',
      description: 'Create professional presentation decks automatically with multiple templates and export to PDF/PPTX formats.',
    },
    {
      icon: <Zap className="h-8 w-8 text-primary" />,
      title: 'Real-time Collaboration',
      description: 'Work with your team in real-time with role-based access control and live updates on analysis progress.',
    },
  ];

  const benefits = [
    'Save 80% of time on competitive research',
    'Generate professional reports in minutes',
    'Access AI-powered brand insights',
    'Collaborate with unlimited team members',
    'Export to multiple formats',
    'Secure cloud storage included',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Globe className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold gradient-text">Brand Audit Tool</span>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="#features" className="text-gray-600 hover:text-primary transition-colors">
              Features
            </Link>
            <Link href="#pricing" className="text-gray-600 hover:text-primary transition-colors">
              Pricing
            </Link>
            <Link href="/auth/login" className="text-gray-600 hover:text-primary transition-colors">
              Sign In
            </Link>
            <Button asChild>
              <Link href="/auth/register">Get Started</Link>
            </Button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Competitive Brand Analysis
            <span className="block gradient-text">Powered by AI</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Automate your competitive research with intelligent web scraping, AI-powered analysis, 
            and professional presentation generation. Get deep brand insights in minutes, not weeks.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild className="text-lg px-8 py-3">
              <Link href="/auth/register">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild className="text-lg px-8 py-3">
              <Link href="#demo">
                Watch Demo
              </Link>
            </Button>
          </div>
          <p className="text-sm text-gray-500 mt-4">
            No credit card required • 14-day free trial • Cancel anytime
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything you need for brand analysis
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              From data collection to presentation generation, our platform handles the entire 
              competitive analysis workflow.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="card-hover">
                <CardHeader>
                  <div className="mb-4">{feature.icon}</div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary/5 to-blue-500/5">
        <div className="container mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Why choose Brand Audit Tool?
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Transform your competitive research process with our comprehensive platform 
                that combines automation, AI insights, and professional presentation tools.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Ready to get started?
              </h3>
              <p className="text-gray-600 mb-6">
                Join thousands of marketing professionals who trust Brand Audit Tool 
                for their competitive analysis needs.
              </p>
              <Button size="lg" className="w-full" asChild>
                <Link href="/auth/register">
                  Start Your Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <p className="text-sm text-gray-500 text-center mt-4">
                14-day free trial • No setup fees
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Globe className="h-6 w-6" />
                <span className="text-lg font-bold">Brand Audit Tool</span>
              </div>
              <p className="text-gray-400">
                AI-powered competitive brand analysis platform for modern marketing teams.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#features" className="hover:text-white transition-colors">Features</Link></li>
                <li><Link href="#pricing" className="hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="#demo" className="hover:text-white transition-colors">Demo</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
                <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/help" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="/docs" className="hover:text-white transition-colors">Documentation</Link></li>
                <li><Link href="/api" className="hover:text-white transition-colors">API</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Brand Audit Tool. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

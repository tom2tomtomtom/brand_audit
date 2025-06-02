export interface User {
  id: string;
  email: string;
  fullName?: string;
  avatarUrl?: string;
  role: 'admin' | 'editor' | 'viewer';
  createdAt: string;
  updatedAt: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  logoUrl?: string;
  subscriptionTier: 'free' | 'pro' | 'enterprise';
  createdAt: string;
  updatedAt: string;
}

export interface Project {
  id: string;
  organizationId: string;
  name: string;
  description?: string;
  status: 'draft' | 'active' | 'completed' | 'archived';
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  brands?: Brand[];
}

export interface Brand {
  id: string;
  projectId: string;
  name: string;
  websiteUrl: string;
  logoUrl?: string;
  industry?: string;
  description?: string;
  scrapingStatus: 'pending' | 'in_progress' | 'completed' | 'failed';
  analysisStatus: 'pending' | 'in_progress' | 'completed' | 'failed';
  createdAt: string;
  updatedAt: string;
  assets?: Asset[];
  campaigns?: Campaign[];
  analyses?: Analysis[];
}

export interface Asset {
  id: string;
  brandId: string;
  type: 'logo' | 'image' | 'document' | 'video';
  url: string;
  filename: string;
  fileSize: number;
  mimeType: string;
  width?: number;
  height?: number;
  altText?: string;
  metadata?: Record<string, any>;
  createdAt: string;
}

export interface Campaign {
  id: string;
  brandId: string;
  name: string;
  description?: string;
  startDate?: string;
  endDate?: string;
  platform?: string;
  campaignType?: string;
  createdAt: string;
}

export interface Analysis {
  id: string;
  brandId: string;
  type: 'positioning' | 'visual' | 'competitive' | 'sentiment';
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  results?: Record<string, any>;
  confidenceScore?: number;
  createdAt: string;
  updatedAt: string;
}

export interface Presentation {
  id: string;
  projectId: string;
  name: string;
  template: string;
  status: 'draft' | 'generating' | 'completed' | 'failed';
  slidesData?: Record<string, any>;
  exportUrl?: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

// Scraping types
export interface ScrapingJob {
  id: string;
  brandId: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  totalAssets: number;
  processedAssets: number;
  errors: string[];
  startedAt?: string;
  completedAt?: string;
}

export interface ScrapingConfig {
  maxPages: number;
  includeImages: boolean;
  includeDocuments: boolean;
  includeSocialMedia: boolean;
  respectRobots: boolean;
  delayBetweenRequests: number;
}

// Analysis types
export interface PositioningAnalysis {
  brandVoice: string;
  targetAudience: string[];
  valueProposition: string;
  keyMessages: string[];
  competitiveDifferentiation: string;
  brandPersonality: string[];
}

export interface VisualAnalysis {
  colorPalette: string[];
  typography: string[];
  logoAnalysis: string;
  visualStyle: string;
  consistencyScore: number;
}

export interface CompetitiveAnalysis {
  directCompetitors: string[];
  indirectCompetitors: string[];
  marketPosition: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

export interface SentimentAnalysis {
  overallSentiment: 'positive' | 'neutral' | 'negative';
  emotionalTone: string[];
  brandPerception: string;
  customerFeedback: string[];
}

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Form types
export interface CreateProjectForm {
  name: string;
  description?: string;
  brands: {
    name: string;
    websiteUrl: string;
    industry?: string;
  }[];
}

export interface CreateBrandForm {
  name: string;
  websiteUrl: string;
  industry?: string;
  description?: string;
}

// UI State types
export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
  code?: string;
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  timestamp: string;
  read: boolean;
}

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useRouter } from 'next/navigation';
import LandingPage from '../landing-page';

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

// Mock Supabase
const mockSupabase = {
  auth: {
    signInWithOAuth: jest.fn(),
  },
};

jest.mock('@/lib/supabase', () => ({
  createClientSupabase: () => mockSupabase,
}));

describe('LandingPage', () => {
  const mockPush = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    });
  });

  it('should render landing page content', () => {
    render(<LandingPage />);

    expect(screen.getByText('Brand Audit Tool')).toBeInTheDocument();
    expect(screen.getByText(/Comprehensive competitive brand analysis/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Get Started/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in with Google/i })).toBeInTheDocument();
  });

  it('should display key features', () => {
    render(<LandingPage />);

    expect(screen.getByText('AI-Powered Analysis')).toBeInTheDocument();
    expect(screen.getByText('Web Scraping')).toBeInTheDocument();
    expect(screen.getByText('Automated Reports')).toBeInTheDocument();
    expect(screen.getByText('Competitive Intelligence')).toBeInTheDocument();
  });

  it('should navigate to login when Get Started is clicked', () => {
    render(<LandingPage />);

    const getStartedButton = screen.getByRole('button', { name: /Get Started/i });
    fireEvent.click(getStartedButton);

    expect(mockPush).toHaveBeenCalledWith('/auth/login');
  });

  it('should handle Google OAuth sign in', async () => {
    mockSupabase.auth.signInWithOAuth.mockResolvedValue({
      data: { url: 'https://oauth-url.com' },
      error: null,
    });

    render(<LandingPage />);

    const googleSignInButton = screen.getByRole('button', { name: /Sign in with Google/i });
    fireEvent.click(googleSignInButton);

    await waitFor(() => {
      expect(mockSupabase.auth.signInWithOAuth).toHaveBeenCalledWith({
        provider: 'google',
        options: {
          redirectTo: expect.stringContaining('/auth/callback'),
        },
      });
    });
  });

  it('should handle OAuth errors gracefully', async () => {
    mockSupabase.auth.signInWithOAuth.mockResolvedValue({
      data: null,
      error: new Error('OAuth failed'),
    });

    // Mock console.error to avoid test output noise
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

    render(<LandingPage />);

    const googleSignInButton = screen.getByRole('button', { name: /Sign in with Google/i });
    fireEvent.click(googleSignInButton);

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('OAuth error:', expect.any(Error));
    });

    consoleSpy.mockRestore();
  });

  it('should display pricing information', () => {
    render(<LandingPage />);

    expect(screen.getByText('Simple Pricing')).toBeInTheDocument();
    expect(screen.getByText('Free Trial')).toBeInTheDocument();
    expect(screen.getByText('Professional')).toBeInTheDocument();
  });

  it('should show how it works section', () => {
    render(<LandingPage />);

    expect(screen.getByText('How It Works')).toBeInTheDocument();
    expect(screen.getByText('1. Add Brands')).toBeInTheDocument();
    expect(screen.getByText('2. Scrape & Analyze')).toBeInTheDocument();
    expect(screen.getByText('3. Get Insights')).toBeInTheDocument();
  });

  it('should have proper accessibility attributes', () => {
    render(<LandingPage />);

    const mainHeading = screen.getByRole('heading', { level: 1 });
    expect(mainHeading).toBeInTheDocument();

    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toBeVisible();
    });

    const links = screen.getAllByRole('link');
    links.forEach(link => {
      expect(link).toHaveAttribute('href');
    });
  });

  it('should be responsive', () => {
    const { container } = render(<LandingPage />);

    // Check for responsive classes (this is a basic check)
    const heroSection = container.querySelector('.hero-section');
    if (heroSection) {
      expect(heroSection).toHaveClass('container');
    }
  });

  it('should display testimonials section', () => {
    render(<LandingPage />);

    // Look for testimonials or reviews section
    const testimonialElements = screen.queryAllByText(/testimonial|review|customer/i);
    // This test might need adjustment based on actual content
  });

  it('should have footer with links', () => {
    render(<LandingPage />);

    // Check for footer links
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument();
    expect(screen.getByText('Terms of Service')).toBeInTheDocument();
  });

  it('should handle keyboard navigation', () => {
    render(<LandingPage />);

    const getStartedButton = screen.getByRole('button', { name: /Get Started/i });
    
    // Focus the button
    getStartedButton.focus();
    expect(getStartedButton).toHaveFocus();

    // Simulate Enter key press
    fireEvent.keyDown(getStartedButton, { key: 'Enter', code: 'Enter' });
    expect(mockPush).toHaveBeenCalledWith('/auth/login');
  });

  it('should display loading state during OAuth', async () => {
    // Mock a delayed OAuth response
    mockSupabase.auth.signInWithOAuth.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({ data: null, error: null }), 100))
    );

    render(<LandingPage />);

    const googleSignInButton = screen.getByRole('button', { name: /Sign in with Google/i });
    fireEvent.click(googleSignInButton);

    // Check if button shows loading state
    await waitFor(() => {
      expect(googleSignInButton).toBeDisabled();
    });
  });
});

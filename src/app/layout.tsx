import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from '@/components/providers';
import { Toaster } from 'react-hot-toast';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Brand Audit Tool - Competitive Brand Analysis',
  description: 'Comprehensive brand audits with AI-powered insights and automated presentation generation',
  keywords: ['brand audit', 'competitive analysis', 'brand intelligence', 'marketing insights'],
  authors: [{ name: 'Brand Audit Tool' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'Brand Audit Tool - Competitive Brand Analysis',
    description: 'Comprehensive brand audits with AI-powered insights and automated presentation generation',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Brand Audit Tool - Competitive Brand Analysis',
    description: 'Comprehensive brand audits with AI-powered insights and automated presentation generation',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'hsl(var(--background))',
                color: 'hsl(var(--foreground))',
                border: '1px solid hsl(var(--border))',
              },
            }}
          />
        </Providers>
      </body>
    </html>
  );
}

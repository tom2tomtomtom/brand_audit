import { Suspense } from 'react';

export default function AnalyticsPage() {
  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-muted-foreground">
          View insights and analytics from your brand audit projects
        </p>
      </div>
      
      <Suspense fallback={<div>Loading analytics...</div>}>
        <div className="text-center py-12">
          <p className="text-muted-foreground">
            Analytics will be available once you have completed brand analyses.
          </p>
        </div>
      </Suspense>
    </div>
  );
}
/**
 * Lazy Loading System
 * Implements intersection observer for images, components, and data
 */

import { useEffect, useRef, useState, useCallback } from 'react';

interface LazyLoadOptions {
  threshold?: number;
  rootMargin?: string;
  placeholder?: React.ReactNode;
  onLoad?: () => void;
  onError?: (error: Error) => void;
  retries?: number;
  retryDelay?: number;
}

/**
 * Hook for lazy loading images
 */
export function useLazyImage(
  src: string,
  options: LazyLoadOptions = {}
): {
  imgRef: React.RefObject<HTMLImageElement>;
  imgSrc: string | undefined;
  isLoaded: boolean;
  isError: boolean;
  retry: () => void;
} {
  const [imgSrc, setImgSrc] = useState<string | undefined>();
  const [isLoaded, setIsLoaded] = useState(false);
  const [isError, setIsError] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const imgRef = useRef<HTMLImageElement>(null);

  const loadImage = useCallback(() => {
    const img = new Image();
    
    img.onload = () => {
      setImgSrc(src);
      setIsLoaded(true);
      setIsError(false);
      options.onLoad?.();
    };

    img.onerror = () => {
      setIsError(true);
      
      if (retryCount < (options.retries || 3)) {
        setTimeout(() => {
          setRetryCount(prev => prev + 1);
          loadImage();
        }, options.retryDelay || 1000);
      } else {
        options.onError?.(new Error('Failed to load image'));
      }
    };

    img.src = src;
  }, [src, retryCount, options]);

  useEffect(() => {
    if (!imgRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isLoaded && !imgSrc) {
          loadImage();
        }
      },
      {
        threshold: options.threshold || 0.1,
        rootMargin: options.rootMargin || '50px',
      }
    );

    observer.observe(imgRef.current);

    return () => {
      observer.disconnect();
    };
  }, [loadImage, isLoaded, imgSrc, options.threshold, options.rootMargin]);

  const retry = useCallback(() => {
    setRetryCount(0);
    setIsError(false);
    loadImage();
  }, [loadImage]);

  return { imgRef, imgSrc, isLoaded, isError, retry };
}

/**
 * Hook for lazy loading components
 */
export function useLazyComponent<T = any>(
  importFn: () => Promise<{ default: React.ComponentType<T> }>,
  options: LazyLoadOptions = {}
): {
  Component: React.ComponentType<T> | null;
  isLoaded: boolean;
  isError: boolean;
  error: Error | null;
  retry: () => void;
} {
  const [Component, setComponent] = useState<React.ComponentType<T> | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const loadComponent = useCallback(async () => {
    try {
      const module = await importFn();
      setComponent(() => module.default);
      setIsLoaded(true);
      setIsError(false);
      setError(null);
      options.onLoad?.();
    } catch (err) {
      setIsError(true);
      setError(err as Error);
      
      if (retryCount < (options.retries || 3)) {
        setTimeout(() => {
          setRetryCount(prev => prev + 1);
          loadComponent();
        }, options.retryDelay || 1000);
      } else {
        options.onError?.(err as Error);
      }
    }
  }, [importFn, retryCount, options]);

  useEffect(() => {
    if (!isLoaded && !Component) {
      loadComponent();
    }
  }, [loadComponent, isLoaded, Component]);

  const retry = useCallback(() => {
    setRetryCount(0);
    setIsError(false);
    setError(null);
    loadComponent();
  }, [loadComponent]);

  return { Component, isLoaded, isError, error, retry };
}

/**
 * Hook for lazy loading data
 */
export function useLazyData<T = any>(
  fetchFn: () => Promise<T>,
  options: LazyLoadOptions & { deps?: any[] } = {}
): {
  data: T | null;
  isLoaded: boolean;
  isLoading: boolean;
  isError: boolean;
  error: Error | null;
  retry: () => void;
  refetch: () => void;
} {
  const [data, setData] = useState<T | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const elementRef = useRef<HTMLDivElement>(null);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await fetchFn();
      setData(result);
      setIsLoaded(true);
      setIsError(false);
      setError(null);
      options.onLoad?.();
    } catch (err) {
      setIsError(true);
      setError(err as Error);
      
      if (retryCount < (options.retries || 3)) {
        setTimeout(() => {
          setRetryCount(prev => prev + 1);
          loadData();
        }, options.retryDelay || 1000);
      } else {
        options.onError?.(err as Error);
      }
    } finally {
      setIsLoading(false);
    }
  }, [fetchFn, retryCount, options]);

  useEffect(() => {
    if (!elementRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isLoaded && !isLoading) {
          loadData();
        }
      },
      {
        threshold: options.threshold || 0.1,
        rootMargin: options.rootMargin || '50px',
      }
    );

    observer.observe(elementRef.current);

    return () => {
      observer.disconnect();
    };
  }, [loadData, isLoaded, isLoading, options.threshold, options.rootMargin, ...(options.deps || [])]);

  const retry = useCallback(() => {
    setRetryCount(0);
    setIsError(false);
    setError(null);
    loadData();
  }, [loadData]);

  const refetch = useCallback(() => {
    setIsLoaded(false);
    loadData();
  }, [loadData]);

  return { data, isLoaded, isLoading, isError, error, retry, refetch };
}

/**
 * Lazy Image Component
 */
export function LazyImage({
  src,
  alt,
  className,
  placeholder,
  ...props
}: React.ImgHTMLAttributes<HTMLImageElement> & {
  placeholder?: React.ReactNode;
}) {
  const { imgRef, imgSrc, isLoaded, isError, retry } = useLazyImage(src || '', {
    placeholder,
  });

  if (isError) {
    return (
      <div className={className} onClick={retry}>
        <div className="flex items-center justify-center h-full bg-gray-100 text-gray-400">
          <span className="text-sm">Failed to load image. Click to retry.</span>
        </div>
      </div>
    );
  }

  return (
    <>
      {!isLoaded && placeholder}
      <img
        ref={imgRef}
        src={imgSrc}
        alt={alt}
        className={className}
        style={{ opacity: isLoaded ? 1 : 0, transition: 'opacity 0.3s' }}
        {...props}
      />
    </>
  );
}

/**
 * Lazy Component Wrapper
 */
export function LazyComponent<T = any>({
  importFn,
  fallback,
  errorFallback,
  ...props
}: {
  importFn: () => Promise<{ default: React.ComponentType<T> }>;
  fallback?: React.ReactNode;
  errorFallback?: React.ReactNode;
} & T) {
  const { Component, isLoaded, isError, retry } = useLazyComponent<T>(importFn);

  if (isError) {
    return (
      <>
        {errorFallback || (
          <div className="flex items-center justify-center p-4">
            <button onClick={retry} className="text-blue-500 hover:underline">
              Failed to load component. Click to retry.
            </button>
          </div>
        )}
      </>
    );
  }

  if (!isLoaded || !Component) {
    return <>{fallback || <div className="animate-pulse bg-gray-200 rounded h-32" />}</>;
  }

  return <Component {...props} />;
}

/**
 * Lazy Data Wrapper
 */
export function LazyData<T = any>({
  fetchFn,
  children,
  fallback,
  errorFallback,
  deps = [],
}: {
  fetchFn: () => Promise<T>;
  children: (data: T) => React.ReactNode;
  fallback?: React.ReactNode;
  errorFallback?: React.ReactNode;
  deps?: any[];
}) {
  const { data, isLoaded, isLoading, isError, retry } = useLazyData<T>(fetchFn, { deps });

  if (isError) {
    return (
      <>
        {errorFallback || (
          <div className="flex items-center justify-center p-4">
            <button onClick={retry} className="text-blue-500 hover:underline">
              Failed to load data. Click to retry.
            </button>
          </div>
        )}
      </>
    );
  }

  if (isLoading || !isLoaded || !data) {
    return <>{fallback || <div className="animate-pulse bg-gray-200 rounded h-32" />}</>;
  }

  return <>{children(data)}</>;
}

/**
 * Preload images in the background
 */
export function preloadImages(urls: string[]): Promise<void[]> {
  const promises = urls.map(url => {
    return new Promise<void>((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve();
      img.onerror = () => reject(new Error(`Failed to preload: ${url}`));
      img.src = url;
    });
  });

  return Promise.all(promises);
}

/**
 * Create virtualized list for large datasets
 */
export function useVirtualList<T>({
  items,
  itemHeight,
  containerHeight,
  overscan = 5,
}: {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  overscan?: number;
}) {
  const [scrollTop, setScrollTop] = useState(0);

  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
  const endIndex = Math.min(
    items.length - 1,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan
  );

  const visibleItems = items.slice(startIndex, endIndex + 1);
  const totalHeight = items.length * itemHeight;
  const offsetY = startIndex * itemHeight;

  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  return {
    visibleItems,
    totalHeight,
    offsetY,
    handleScroll,
  };
}

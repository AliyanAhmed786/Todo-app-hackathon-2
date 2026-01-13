// Performance utilities for optimizing page load time and UI responsiveness

// Performance monitoring for dashboard load times
interface PerformanceMetrics {
  navigationStart: number;
  loadEventEnd: number;
  domContentLoaded: number;
  firstPaint: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  cumulativeLayoutShift: number;
  interactionToNextPaint: number;
}

/**
 * Measures the time taken for a function to execute
 */
export const measurePerformance = async <T>(
  fn: () => Promise<T>,
  label: string
): Promise<T> => {
  const start = performance.now();
  const result = await fn();
  const end = performance.now();

  console.log(`${label}: ${end - start} milliseconds`);

  // Log performance metrics to help maintain 60fps
  if (end - start > 16.67) {
    console.warn(`${label} exceeded 60fps budget (${end - start}ms > 16.67ms)`);
  }

  return result;
};

/**
 * Measures dashboard-specific performance metrics
 */
export const measureDashboardPerformance = (): PerformanceMetrics => {
  const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
  const paint = performance.getEntriesByType('paint');
  const lcp = performance.getEntriesByType('largest-contentful-paint')[0];
  const cls = performance.getEntriesByType('layout-shift');

  let cumulativeLayoutShift = 0;
  if (cls) {
    cls.forEach((entry: any) => {
      if (!entry.hadRecentInput) {
        cumulativeLayoutShift += entry.value;
      }
    });
  }

  return {
    navigationStart: navigation?.navigationStart || 0,
    loadEventEnd: navigation?.loadEventEnd || 0,
    domContentLoaded: navigation?.domContentLoadedEventEnd || 0,
    firstPaint: paint.find(entry => entry.name === 'first-paint')?.startTime || 0,
    firstContentfulPaint: paint.find(entry => entry.name === 'first-contentful-paint')?.startTime || 0,
    largestContentfulPaint: lcp?.startTime || 0,
    cumulativeLayoutShift,
    interactionToNextPaint: 0 // Would need additional setup to measure
  };
};

/**
 * Reports dashboard performance metrics to console or analytics service
 */
export const reportDashboardPerformance = (pageName: string = 'dashboard') => {
  if (typeof window !== 'undefined') {
    // Wait for all resources to load
    window.addEventListener('load', () => {
      setTimeout(() => {
        const metrics = measureDashboardPerformance();

        console.group(`Performance Metrics - ${pageName}`);
        console.log('Load Time:', (metrics.loadEventEnd - metrics.navigationStart).toFixed(2), 'ms');
        console.log('DOM Content Loaded:', (metrics.domContentLoaded - metrics.navigationStart).toFixed(2), 'ms');
        console.log('First Paint:', metrics.firstPaint.toFixed(2), 'ms');
        console.log('First Contentful Paint:', metrics.firstContentfulPaint.toFixed(2), 'ms');
        console.log('Largest Contentful Paint:', metrics.largestContentfulPaint.toFixed(2), 'ms');
        console.log('Cumulative Layout Shift:', metrics.cumulativeLayoutShift.toFixed(4));
        console.groupEnd();

        // In a real app, you would send these metrics to an analytics service
        if (process.env.NODE_ENV === 'production') {
          // Example: analytics.track('Dashboard Performance', { page: pageName, metrics });
        }
      }, 1000); // Wait a bit for all metrics to be available
    });
  }
};

/**
 * Measures the time taken for API calls
 */
export const measureApiCall = async <T>(
  fn: () => Promise<T>,
  endpoint: string
): Promise<T> => {
  const start = performance.now();
  try {
    const result = await fn();
    const end = performance.now();

    const duration = end - start;
    console.log(`API call to ${endpoint}: ${duration.toFixed(2)}ms`);

    // Log slow API calls
    if (duration > 1000) {
      console.warn(`Slow API call to ${endpoint}: ${duration.toFixed(2)}ms`);
    }

    return result;
  } catch (error) {
    const end = performance.now();
    const duration = end - start;
    console.error(`API call to ${endpoint} failed after ${duration.toFixed(2)}ms:`, error);
    throw error;
  }
};

/**
 * Debounces a function to improve UI responsiveness
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout | null = null;

  return (...args: Parameters<T>) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      func(...args);
    }, delay);
  };
};

/**
 * Throttles a function to improve UI responsiveness
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
};

/**
 * Implements requestAnimationFrame for smooth animations
 */
export const raf = (callback: FrameRequestCallback): number => {
  if (typeof window !== 'undefined') {
    return window.requestAnimationFrame(callback);
  }
  // Fallback for SSR
  return setTimeout(callback, 16.67) as unknown as number;
};

/**
 * Calculates frames per second (FPS) for UI responsiveness
 */
export class FPSCounter {
  private frameCount = 0;
  private lastTime = performance.now();
  private fps = 0;

  update(): number {
    this.frameCount++;
    const now = performance.now();

    if (now >= this.lastTime + 1000) {
      this.fps = Math.round((this.frameCount * 1000) / (now - this.lastTime));
      this.frameCount = 0;
      this.lastTime = now;
    }

    return this.fps;
  }

  getFPS(): number {
    return this.fps;
  }
}

/**
 * Preloads images to improve page load time
 */
export const preloadImage = (src: string): Promise<HTMLImageElement> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
};

/**
 * Implements a simple caching mechanism to improve performance
 */
export class SimpleCache<T> {
  private cache = new Map<string, { value: T; timestamp: number }>();
  private ttl: number; // Time to live in milliseconds

  constructor(ttl = 5 * 60 * 1000) { // Default 5 minutes
    this.ttl = ttl;
  }

  get(key: string): T | undefined {
    const item = this.cache.get(key);
    if (!item) return undefined;

    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      return undefined;
    }

    return item.value;
  }

  set(key: string, value: T): void {
    this.cache.set(key, { value, timestamp: Date.now() });
  }

  clear(): void {
    this.cache.clear();
  }
}

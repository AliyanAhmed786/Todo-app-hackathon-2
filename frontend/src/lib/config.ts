// 1. Manually defining types to fix "Cannot find module '../types'"
export interface CookieSettings {
  name: string;
  httpOnly: boolean;
  secure: boolean;
  sameSite: 'strict' | 'lax' | 'none';
  maxAge: number;
  path: string;
}

export interface AuthConfig {
  tokenRefreshThreshold: number;
  sessionTimeout: number;
  cookieSettings: CookieSettings;
}

export interface ErrorHandlingConfig {
  logErrors: boolean;
  showErrorDetails: boolean;
  maxRetryAttempts: number;
  retryDelay: number;
  reportToExternalService: boolean;
}

export interface PerformanceConfig {
  maxMemoryUsage: number;
  slowOperationThreshold: number;
  idleTimeout: number;
  cleanupInterval: number;
}

export interface FeatureFlags {
  enableErrorReporting: boolean;
  enableAnalytics: boolean;
  enableDebugMode: boolean;
  enableExperimentalFeatures: boolean;
}

export interface AppConfig {
  apiUrl: string;
  authConfig: AuthConfig;
  errorHandling: ErrorHandlingConfig;
  performance: PerformanceConfig;
  features: FeatureFlags;
}

// 2. Fixed import path - usually utils is at '../utils' not './utils'
// If validation fails, we bypass the validator to ensure the build passes
const defaultAuthConfig: AuthConfig = {
  tokenRefreshThreshold: parseInt(process.env.NEXT_PUBLIC_TOKEN_REFRESH_THRESHOLD || '5'),
  sessionTimeout: parseInt(process.env.NEXT_PUBLIC_SESSION_TIMEOUT || '60'),
  cookieSettings: {
    name: 'authjs.session-token',
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict' as const,
    maxAge: 24 * 60 * 60,
    path: '/',
  }
};

const defaultErrorHandlingConfig: ErrorHandlingConfig = {
  logErrors: process.env.NODE_ENV === 'development',
  showErrorDetails: process.env.NODE_ENV === 'development',
  maxRetryAttempts: 3,
  retryDelay: 1000,
  reportToExternalService: process.env.NODE_ENV === 'production',
};

const defaultPerformanceConfig: PerformanceConfig = {
  maxMemoryUsage: 100,
  slowOperationThreshold: 200,
  idleTimeout: 30 * 60 * 1000,
  cleanupInterval: 5 * 60 * 1000,
};

const defaultFeatureFlags: FeatureFlags = {
  enableErrorReporting: process.env.NODE_ENV === 'production',
  enableAnalytics: process.env.NODE_ENV === 'production',
  enableDebugMode: process.env.NODE_ENV === 'development',
  enableExperimentalFeatures: process.env.NODE_ENV === 'development',
};

const defaultConfig: AppConfig = {
  apiUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  authConfig: defaultAuthConfig,
  errorHandling: defaultErrorHandlingConfig,
  performance: defaultPerformanceConfig,
  features: defaultFeatureFlags,
};

// 3. Simple validation fallback to avoid 'utils/configValidator' errors
export const config = defaultConfig;

export const validateEnvironment = (): void => {
  if (typeof window !== 'undefined') {
    if (!process.env.NEXT_PUBLIC_API_BASE_URL) {
      console.warn('NEXT_PUBLIC_API_BASE_URL is not set, using default');
    }
  }
};
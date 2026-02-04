import {
  AppConfig,
  AuthConfig,
  CookieSettings,
  ErrorHandlingConfig,
  PerformanceConfig,
  FeatureFlags
} from '../types';
import { validateConfig as validateConfigUtil, isConfigValid, getDefaultConfig } from '../utils/configValidator';

const defaultAuthConfig: AuthConfig = {
  tokenRefreshThreshold: parseInt(process.env.NEXT_PUBLIC_TOKEN_REFRESH_THRESHOLD || '5'), // Minutes before expiration to refresh
  sessionTimeout: parseInt(process.env.NEXT_PUBLIC_SESSION_TIMEOUT || '60'), // Minutes of inactivity before session expires
  cookieSettings: {
    name: 'authjs.session-token',
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict' as const,
    maxAge: 24 * 60 * 60, // 24 hours in seconds
    path: '/',
  }
};

const defaultErrorHandlingConfig: ErrorHandlingConfig = {
  logErrors: process.env.NODE_ENV === 'development',
  showErrorDetails: process.env.NODE_ENV === 'development',
  maxRetryAttempts: 3,
  retryDelay: 1000, // 1 second
  reportToExternalService: process.env.NODE_ENV === 'production',
};

const defaultPerformanceConfig: PerformanceConfig = {
  maxMemoryUsage: 100, // MB
  slowOperationThreshold: 200, // milliseconds
  idleTimeout: 30 * 60 * 1000, // 30 minutes in milliseconds
  cleanupInterval: 5 * 60 * 1000, // 5 minutes in milliseconds
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

// Validate the configuration and fall back to defaults if invalid
let validatedConfig: AppConfig = defaultConfig;
try {
  if (isConfigValid(defaultConfig)) {
    validatedConfig = defaultConfig;
  } else {
    console.warn('Configuration validation failed, using default configuration');
    validatedConfig = getDefaultConfig();
  }
} catch (error) {
  console.error('Configuration validation error:', error);
  console.warn('Using default configuration');
  validatedConfig = getDefaultConfig();
}

export const config = validatedConfig;

// Function to validate environment variables and fail gracefully
export const validateEnvironment = (): void => {
  if (typeof window !== 'undefined') {
    // Client-side check
    if (!process.env.NEXT_PUBLIC_API_BASE_URL) {
      console.warn('NEXT_PUBLIC_API_BASE_URL is not set, using default');
    }
  }
};
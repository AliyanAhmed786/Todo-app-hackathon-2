// ErrorBoundary component for comprehensive error handling
import React from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: React.ErrorInfo;
}

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: undefined,
      errorInfo: undefined
    };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Update state with error info for detailed display
    this.setState({ errorInfo });

    // Log the error to an error reporting service
    console.error('Error caught by boundary:', error, errorInfo);

    // Call the optional onError callback if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Send error to logging service in production
    if (process.env.NODE_ENV === 'production') {
      // In a real app, you would send this to an error reporting service like Sentry
      // For now, we'll just log it to the console
      console.error('Error details:', {
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack
      });
    }
  }

  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided, otherwise use default enhanced fallback
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default enhanced fallback UI with error details
      return (
        <div className="backdrop-blur-2xl bg-white/40 p-6 rounded-3xl border border-white/60 shadow-xl shadow-gray-900/10 max-w-2xl mx-auto my-8">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mt-4">Something went wrong</h3>
            <p className="mt-2 text-sm text-gray-500">
              An unexpected error occurred. Please try refreshing the page or contact support if the problem persists.
            </p>
            <div className="mt-6">
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-xl shadow-sm text-white bg-gradient-to-r from-coral-600 to-coral-700 hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-coral-500"
              >
                Refresh Page
              </button>
            </div>
          </div>

          {/* Error details for debugging (only shown in development) */}
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <div className="mt-6 p-4 bg-red-50/60 border border-red-200/60 rounded-xl">
              <h4 className="text-sm font-medium text-red-800 mb-2">Error Details:</h4>
              <div className="text-xs text-red-700 font-mono whitespace-pre-wrap break-words">
                <div className="mb-2">
                  <strong>Message:</strong> {this.state.error.message}
                </div>
                <div className="mb-2">
                  <strong>Name:</strong> {this.state.error.name}
                </div>
                <div className="mb-2">
                  <strong>Stack:</strong>
                  <pre className="mt-1 p-2 bg-white/60 rounded border border-red-100 overflow-x-auto">
                    {this.state.error.stack}
                  </pre>
                </div>
                {this.state.errorInfo?.componentStack && (
                  <div>
                    <strong>Component Stack:</strong>
                    <pre className="mt-1 p-2 bg-white/60 rounded border border-red-100 overflow-x-auto">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

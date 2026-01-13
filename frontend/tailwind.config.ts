import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/styles/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Coral color palette
        coral: {
          50: '#fff7f5',
          100: '#ffeee8',
          200: '#ffddd4',
          300: '#ffb9ae',
          400: '#ff8f7e',
          500: '#ff6b52',
          600: '#e64e38',
          700: '#c23a27',
          800: '#9e2f21',
          900: '#80271d',
          950: '#4a130d',
        },
        // Priority colors for accessibility
        priority: {
          low: '#10b981', // Green for low priority
          medium: '#f59e0b', // Yellow for medium priority
          high: '#ef4444', // Red for high priority
        },
        // Accessibility-focused colors
        accessible: {
          focus: '#2563eb', // Blue for focus indicators
          contrast: '#000000', // High contrast for text
        }
      },
      backgroundImage: {
        'gradient-to-r': 'linear-gradient(to right, var(--tw-gradient-stops))',
      },
      backdropBlur: {
        '2xl': '40px',
      },
      boxShadow: {
        'coral-500/30': '0 10px 15px -3px rgba(255, 107, 82, 0.3), 0 4px 6px -4px rgba(255, 107, 82, 0.3)',
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
      animation: {
        blob: "blob 7s infinite",
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'fade-out': 'fadeOut 0.3s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'slide-out': 'slideOut 0.3s ease-out',
      },
      keyframes: {
        blob: {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
          '100%': { transform: 'translate(0px, 0px) scale(1)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeOut: {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideOut: {
          '0%': { transform: 'translateY(0)', opacity: '1' },
          '100%': { transform: 'translateY(-10px)', opacity: '0' },
        }
      },
      // Accessibility enhancements
      focus: {
        'ring': '2px solid #2563eb',
        'ring-offset': '2px solid transparent',
      },
      // Minimum touch target size for accessibility
      spacing: {
        '11': '2.75rem', // 44px for accessibility touch targets
        '12': '3rem',     // 48px for larger touch targets
      },
      // Animation delays for blob animations
      animationDelay: {
        '2000': '2s',
        '4000': '4s',
      }
    },
  },
  plugins: [
    // Add plugin for accessibility features
    function ({ addUtilities }: any) {
      addUtilities({
        // High contrast mode support
        '.high-contrast': {
          '@media (prefers-contrast: high)': {
            border: '2px solid #000',
            backgroundColor: '#fff',
          }
        },
        // Reduced motion support
        '.reduced-motion': {
          '@media (prefers-reduced-motion: reduce)': {
            animation: 'none',
            transition: 'none',
          }
        },
        // Focus visible for accessibility
        '.focus-visible': {
          outline: '2px solid #2563eb',
          outlineOffset: '2px',
        },
        // Animation delay utilities
        '.animation-delay-2000': {
          'animation-delay': '2s',
        },
        '.animation-delay-4000': {
          'animation-delay': '4s',
        }
      })
    }
  ],
};
export default config;
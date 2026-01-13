// SignupForm component for user registration using Better Auth
import React, { useState } from 'react';
import { signUp } from '../lib/authClient';

interface SignupFormProps {
  onSignupSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

const SignupForm: React.FC<SignupFormProps> = ({ onSignupSuccess, onSwitchToLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    if (!email) {
      setError('Email is required');
      return false;
    }

    if (!password) {
      setError('Password is required');
      return false;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return false;
    }

    if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(password)) {
      setError('Password must contain uppercase, lowercase, number, and special character');
      return false;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await signUp.email({
        email,
        password,
      });

      if (result?.error) {
        setError(result.error.message || 'Signup failed. Please try again.');
      } else {
        // Call the success callback
        if (onSignupSuccess) {
          onSignupSuccess();
        }
      }
    } catch (err: any) {
      console.error('Signup error:', err);
      setError(err.message || 'Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md backdrop-blur-2xl bg-white/40 p-4 sm:p-8 rounded-3xl border border-white/60 shadow-xl shadow-gray-900/10">
      <div>
        <h2 className="mt-6 text-center text-2xl sm:text-3xl font-extrabold text-gray-900">
          Create your account
        </h2>
      </div>
      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
        {error && (
          <div className="backdrop-blur-xl bg-red-100/80 border border-red-400/60 text-red-700 px-4 py-3 rounded-2xl relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="rounded-xl shadow-sm -space-y-px">
          <div>
            <label htmlFor="email" className="sr-only">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-3 bg-white/60 border border-white/40 placeholder-gray-500 text-gray-900 rounded-t-xl focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 focus:z-10 sm:text-sm"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="password" className="sr-only">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-3 bg-white/60 border border-white/40 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 focus:z-10 sm:text-sm"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="confirmPassword" className="sr-only">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              autoComplete="new-password"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-3 bg-white/60 border border-white/40 placeholder-gray-500 text-gray-900 rounded-b-xl focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 focus:z-10 sm:text-sm"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={loading}
            className={`group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-coral-600 to-coral-700 hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95'
            } transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none`}
          >
            {loading ? 'Creating Account...' : 'Sign up'}
          </button>
        </div>
      </form>

      <div className="text-center mt-4">
        <button
          type="button"
          onClick={onSwitchToLogin}
          className="text-coral-600 hover:text-coral-700 text-sm font-medium"
        >
          Already have an account? Sign in
        </button>
      </div>
    </div>
  );
};

export default SignupForm;

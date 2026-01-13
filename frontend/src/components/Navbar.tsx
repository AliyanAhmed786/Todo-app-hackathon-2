// Navbar component for navigation and user info
import React from 'react';
import { getUserIdFromToken, logout } from '../utils/auth';

interface NavbarProps {
  userEmail?: string;
}

const Navbar: React.FC<NavbarProps> = ({ userEmail }) => {
  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="fixed w-full top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-white/40 shadow-lg shadow-gray-900/5">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-2xl font-bold bg-gradient-to-r from-coral-600 to-coral-700 bg-clip-text text-transparent">
                TodoApp
              </span>
            </div>
            <div className="hidden md:block ml-10">
              <div className="flex items-baseline space-x-4">
                <a
                  href="/dashboard"
                  className="text-gray-700 hover:text-coral-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  Dashboard
                </a>
                <a
                  href="/dashboard"
                  className="text-gray-700 hover:text-coral-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  My Tasks
                </a>
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center space-x-4">
              {userEmail && (
                <p className="text-gray-700 text-sm font-medium mr-4">
                  {userEmail}
                </p>
              )}
              <button
                onClick={handleLogout}
                className="p-[10px] bg-gradient-to-r from-coral-600 to-coral-700 text-white text-sm font-semibold rounded-xl transition-all duration-300 hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 focus:ring-2 focus:ring-coral-300 focus:outline-none active:scale-95"
              >
                Logout
              </button>
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <button
              type="button"
              className="backdrop-blur-xl bg-white/60 inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-coral-600 border border-white/60 focus:outline-none focus:ring-2 focus:ring-coral-300"
              aria-controls="mobile-menu"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div className="md:hidden" id="mobile-menu">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 backdrop-blur-xl bg-white/60 border-t border-white/60">
          <a
            href="/dashboard"
            className="text-gray-700 hover:text-coral-600 block px-3 py-2 rounded-md text-base font-medium"
          >
            Dashboard
          </a>
          <a
            href="/dashboard"
            className="text-gray-700 hover:text-coral-600 block px-3 py-2 rounded-md text-base font-medium"
          >
            My Tasks
          </a>
          <button
            onClick={handleLogout}
            className="w-full text-left text-gray-700 hover:text-coral-600 block px-3 py-2 rounded-md text-base font-medium"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

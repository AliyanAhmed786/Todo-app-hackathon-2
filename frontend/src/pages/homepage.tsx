import Link from 'next/link';
import { isServerAuthenticated } from '../lib/auth';

export default async function HomePage() {
  // Check if user is authenticated server-side
  const isAuthenticated = await isServerAuthenticated();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-[#FF6767]">Todo App</h1>
            </div>

            <div className="flex items-center space-x-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-64 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF6767]"
                />
                <svg
                  className="absolute right-3 top-2.5 h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>

              <div className="flex items-center space-x-4">
                {!isAuthenticated ? (
                  <>
                    <Link href="/login" className="px-4 py-2 text-gray-700 hover:text-[#FF6767] transition-colors">
                      Sign In
                    </Link>
                    <Link
                      href="/signup"
                      className="px-6 py-2 bg-[#FF6767] text-white rounded-lg hover:bg-[#e55a5a] transition-colors"
                    >
                      Get Started
                    </Link>
                  </>
                ) : (
                  <Link
                    href="/dashboard"
                    className="px-6 py-2 bg-[#FF6767] text-white rounded-lg hover:bg-[#e55a5a] transition-colors"
                  >
                    Dashboard
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-6">
              Organize Your Tasks, <br />
              <span className="text-[#FF6767]">Simplify Your Life</span>
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              A beautiful and intuitive task management application designed to help you stay organized and productive.
              Get started today and take control of your tasks.
            </p>
            <div className="flex space-x-4">
              <Link
                href={isAuthenticated ? "/dashboard" : "/signup"}
                className="px-8 py-3 bg-[#FF6767] text-white rounded-lg hover:bg-[#e55a5a] transition-colors font-semibold"
              >
                {isAuthenticated ? "Go to Dashboard" : "Get Started"}
              </Link>
              <Link
                href="/#features"
                className="px-8 py-3 border-2 border-[#FF6767] text-[#FF6767] rounded-lg hover:bg-[#FF6767] hover:text-white transition-colors font-semibold"
              >
                Learn More
              </Link>
            </div>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-200">
            <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full h-64 flex items-center justify-center">
              <span className="text-gray-500">Dashboard Preview</span>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="container mx-auto px-6 py-16 bg-white">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Powerful Features for Productivity</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-gray-50 p-8 rounded-xl border border-gray-200 text-center">
            <div className="w-16 h-16 bg-[#FF6767]/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-[#FF6767]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Task Management</h3>
            <p className="text-gray-600">
              Create, organize, and track your tasks with ease. Set priorities, due dates, and categories to stay organized.
            </p>
          </div>

          <div className="bg-gray-50 p-8 rounded-xl border border-gray-200 text-center">
            <div className="w-16 h-16 bg-[#FF6767]/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-[#FF6767]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Time Tracking</h3>
            <p className="text-gray-600">
              Monitor how much time you spend on each task. Get insights into your productivity patterns.
            </p>
          </div>

          <div className="bg-gray-50 p-8 rounded-xl border border-gray-200 text-center">
            <div className="w-16 h-16 bg-[#FF6767]/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-[#FF6767]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Team Collaboration</h3>
            <p className="text-gray-600">
              Share tasks with your team, assign responsibilities, and collaborate in real-time.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-6 py-16 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Ready to get started?</h2>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Join thousands of users who have transformed their productivity with our task management solution.
        </p>
        <Link
          href={isAuthenticated ? "/dashboard" : "/signup"}
          className="inline-block px-8 py-4 bg-[#FF6767] text-white rounded-lg hover:bg-[#e55a5a] transition-colors font-semibold text-lg"
        >
          {isAuthenticated ? "Go to Dashboard" : "Create Your Account"}
        </Link>
      </div>

      {/* Footer */}
      <footer className="bg-gray-100 py-12">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h3 className="text-xl font-bold text-gray-900">Todo App</h3>
              <p className="text-gray-600">Simplify your tasks, enhance your productivity</p>
            </div>
            <div className="flex space-x-6">
              <Link href="/privacy" className="text-gray-600 hover:text-[#FF6767]">Privacy</Link>
              <Link href="/terms" className="text-gray-600 hover:text-[#FF6767]">Terms</Link>
              <Link href="/contact" className="text-gray-600 hover:text-[#FF6767]">Contact</Link>
            </div>
          </div>
          <div className="mt-8 text-center text-gray-500 text-sm">
            © {new Date().getFullYear()} Todo App. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}

// Metadata export for the home page
export async function generateMetadata() {
  return {
    title: 'Todo App - Organize Your Tasks, Simplify Your Life',
    description: 'A beautiful and intuitive task management application designed to help you stay organized and productive.',
  };
}

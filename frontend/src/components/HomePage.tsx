import Link from 'next/link';

export default function HomePage({ isAuthenticated }) {

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 relative overflow-hidden">
      {/* Decorative blur orbs */}
      <div className="absolute top-20 -left-20 w-96 h-96 bg-coral-300/30 rounded-full blur-3xl animate-pulse" aria-hidden="true"></div>
      <div className="absolute top-40 right-10 w-80 h-80 bg-coral-400/20 rounded-full blur-3xl float-animation" aria-hidden="true"></div>
      <div className="absolute bottom-20 left-1/3 w-72 h-72 bg-coral-200/25 rounded-full blur-3xl" style={{ animationDelay: '2s' }} aria-hidden="true"></div>

      {/* Glassmorphic Navigation Bar */}
      <nav className="glass-nav sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold gradient-text">Todo App</h1>
            </div>

            <div className="flex items-center space-x-4">
              <div className="relative hidden md:block">
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-64 px-4 py-2 bg-white/60 backdrop-blur-sm border border-white/40 rounded-xl focus:outline-none focus:ring-2 focus:ring-coral-300 transition-all duration-200"
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
                    <Link href="/login" className="px-4 py-2 text-gray-700 hover:text-coral-600 transition-colors font-medium">
                      Sign In
                    </Link>
                    <Link
                      href="/signup"
                      className="px-6 py-2 bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 transition-all duration-300 font-semibold"
                    >
                      Get Started
                    </Link>
                  </>
                ) : (
                  <Link
                    href="/dashboard"
                    className="px-6 py-2 bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 transition-all duration-300 font-semibold"
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
      <div className="container mx-auto px-6 py-16 md:py-24 relative">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="fade-in">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Organize Your Tasks, <br />
              <span className="gradient-text">Simplify Your Life</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-600 mb-8 leading-relaxed">
              A beautiful and intuitive task management application designed to help you stay organized and productive.
              Get started today and take control of your tasks.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href={isAuthenticated ? "/dashboard" : "/signup"}
                className="px-8 py-4 bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-1 transition-all duration-300 font-semibold text-center"
              >
                {isAuthenticated ? "Go to Dashboard" : "Get Started"}
              </Link>
              <Link
                href="/#features"
                className="px-8 py-4 backdrop-blur-xl bg-white/40 border-2 border-coral-600/30 text-coral-600 rounded-xl hover:bg-white/60 hover:border-coral-600 hover:-translate-y-1 transition-all duration-300 font-semibold text-center"
              >
                Learn More
              </Link>
            </div>
          </div>

          {/* Dashboard Preview Mockup */}
          <div className="relative slide-in-right">
            <div className="backdrop-blur-xl bg-white/40 p-6 rounded-3xl border border-white/60 shadow-2xl shadow-gray-900/10">
              {/* Mini Header */}
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200/50">
                <h3 className="text-lg font-bold text-gray-900">Task Dashboard</h3>
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-coral-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                </div>
              </div>

              {/* Mini Stats */}
              <div className="grid grid-cols-3 gap-3 mb-6">
                <div className="bg-gradient-to-br from-coral-500/20 to-coral-600/20 p-3 rounded-xl backdrop-blur-sm">
                  <p className="text-xs text-coral-700 font-semibold mb-1">Total</p>
                  <p className="text-2xl font-bold text-coral-600">24</p>
                </div>
                <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 p-3 rounded-xl backdrop-blur-sm">
                  <p className="text-xs text-green-700 font-semibold mb-1">Done</p>
                  <p className="text-2xl font-bold text-green-600">18</p>
                </div>
                <div className="bg-gradient-to-br from-amber-500/20 to-amber-600/20 p-3 rounded-xl backdrop-blur-sm">
                  <p className="text-xs text-amber-700 font-semibold mb-1">Active</p>
                  <p className="text-2xl font-bold text-amber-600">6</p>
                </div>
              </div>

              {/* Mini Task Cards */}
              <div className="space-y-3">
                <div className="bg-white/60 backdrop-blur-sm p-3 rounded-xl border border-white/40 flex items-center space-x-3">
                  <div className="w-5 h-5 rounded-full border-2 border-green-500 flex items-center justify-center">
                    <svg className="w-3 h-3 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 line-through">Complete project proposal</p>
                  </div>
                  <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded-full">High</span>
                </div>

                <div className="bg-white/60 backdrop-blur-sm p-3 rounded-xl border border-white/40 flex items-center space-x-3">
                  <div className="w-5 h-5 rounded-full border-2 border-gray-400"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">Review team feedback</p>
                  </div>
                  <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full">Med</span>
                </div>

                <div className="bg-white/60 backdrop-blur-sm p-3 rounded-xl border border-white/40 flex items-center space-x-3">
                  <div className="w-5 h-5 rounded-full border-2 border-gray-400"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">Update documentation</p>
                  </div>
                  <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">Low</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="container mx-auto px-6 py-16 md:py-24 relative">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-4">Powerful Features for Productivity</h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">Everything you need to manage your tasks efficiently and boost your productivity</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Feature Card 1 */}
          <div className="glass-card card-hover rounded-2xl p-8 text-center group">
            <div className="w-20 h-20 bg-gradient-to-br from-coral-500 to-coral-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow group-hover:shadow-glow-lg transition-all duration-300 group-hover:scale-110">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Task Management</h3>
            <p className="text-gray-600 leading-relaxed">
              Create, organize, and track your tasks with ease. Set priorities, due dates, and categories to stay organized.
            </p>
          </div>

          {/* Feature Card 2 */}
          <div className="glass-card card-hover rounded-2xl p-8 text-center group" style={{ animationDelay: '100ms' }}>
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg shadow-blue-500/30 group-hover:shadow-xl group-hover:shadow-blue-500/40 transition-all duration-300 group-hover:scale-110">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Time Tracking</h3>
            <p className="text-gray-600 leading-relaxed">
              Monitor how much time you spend on each task. Get insights into your productivity patterns.
            </p>
          </div>

          {/* Feature Card 3 */}
          <div className="glass-card card-hover rounded-2xl p-8 text-center group" style={{ animationDelay: '200ms' }}>
            <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg shadow-green-500/30 group-hover:shadow-xl group-hover:shadow-green-500/40 transition-all duration-300 group-hover:scale-110">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Team Collaboration</h3>
            <p className="text-gray-600 leading-relaxed">
              Share tasks with your team, assign responsibilities, and collaborate in real-time.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-6 py-16 md:py-24 text-center relative">
        <div className="backdrop-blur-xl bg-gradient-to-br from-coral-500/10 via-coral-400/10 to-coral-600/10 rounded-3xl p-12 md:p-16 border border-white/60 shadow-2xl shadow-coral-900/10">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">Ready to get started?</h2>
          <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            Join thousands of users who have transformed their productivity with our task management solution.
          </p>
          <Link
            href={isAuthenticated ? "/dashboard" : "/signup"}
            className="inline-block px-10 py-4 bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-xl hover:shadow-2xl hover:shadow-coral-500/40 hover:-translate-y-1 transition-all duration-300 font-semibold text-lg"
          >
            {isAuthenticated ? "Go to Dashboard" : "Create Your Account"}
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative mt-16 backdrop-blur-xl bg-white/40 border-t border-white/60 py-12 shadow-inner">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-6 md:mb-0 text-center md:text-left">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Todo App</h3>
              <p className="text-gray-600">Simplify your tasks, enhance your productivity</p>
            </div>
            <div className="flex space-x-8">
              <span className="text-gray-600">Privacy</span>
              <span className="text-gray-600">Terms</span>
              <span className="text-gray-600">Contact</span>
            </div>
          </div>
          <div className="mt-8 pt-6 border-t border-white/40 text-center text-gray-500 text-sm">
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

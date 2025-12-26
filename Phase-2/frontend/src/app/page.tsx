'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-[#1a1a2e] via-[#16213e] to-[#0f3460]">
      {/* Navigation */}
      <nav className="bg-[#1a1a2e]/80 backdrop-blur-md border-b border-[#e94560]/20 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-4">
            <h1 className="text-xl sm:text-2xl font-bold text-[#e94560]">Task Manager</h1>
            <div className="flex gap-2 sm:gap-4 w-full sm:w-auto">
              <Link
                href="/auth/login"
                className="flex-1 sm:flex-none px-3 sm:px-4 py-2 text-white hover:text-[#e94560] font-medium text-center sm:text-left transition-colors"
              >
                Login
              </Link>
              <Link
                href="/auth/signup"
                className="flex-1 sm:flex-none px-3 sm:px-4 py-2 bg-[#e94560] text-white rounded-lg hover:bg-[#ff6b6b] font-medium text-center transition-colors"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {/* Hero Section */}
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-20 text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-[#e94560] via-[#ff6b6b] to-[#feca57] bg-clip-text text-transparent mb-4 sm:mb-6">
            Manage Your Tasks Smartly
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-gray-300 mb-8 sm:mb-12 max-w-2xl mx-auto px-2">
            Organize your work, track progress, and stay productive with a modern, secure, and lightning-fast task manager.
          </p>

          {/* Feature Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8 mt-8 sm:mt-12 mb-8 sm:mb-12">
            <div className="bg-white/10 backdrop-blur-xl border border-[#e94560]/20 rounded-2xl p-6 hover:scale-105 transition-transform">
              <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">⚡</div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3 text-[#e94560]">Fast & Simple</h3>
              <p className="text-sm sm:text-base text-gray-300">
                Clean UI designed for speed and simplicity
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-xl border border-[#0ea5e9]/20 rounded-2xl p-6 hover:scale-105 transition-transform">
              <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">📊</div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3 text-[#0ea5e9]">Track Progress</h3>
              <p className="text-sm sm:text-base text-gray-300">
                Stay on top of completed and pending tasks
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-xl border border-[#feca57]/20 rounded-2xl p-6 hover:scale-105 transition-transform">
              <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🔒</div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3 text-[#feca57]">Secure</h3>
              <p className="text-sm sm:text-base text-gray-300">
                Your data is private and protected
              </p>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
            <Link
              href="/auth/signup"
              className="px-6 sm:px-8 py-3 bg-gradient-to-r from-[#e94560] to-[#ff6b6b] text-white rounded-lg hover:opacity-90 font-medium text-base sm:text-lg text-center transition-opacity"
            >
              Get Started
            </Link>
            <Link
              href="/auth/login"
              className="px-6 sm:px-8 py-3 bg-white/10 text-white rounded-lg hover:bg-white/20 font-medium text-base sm:text-lg text-center border border-white/20 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-[#1a1a2e]/80 border-t border-[#e94560]/20 text-white py-6 sm:py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 text-center">
          <p className="text-sm sm:text-base text-gray-400">&copy; 2025 Hackathon-2 Task Manager • Built with ❤ & AI</p>
          <p className="text-xs text-gray-500 mt-1">DEVELOPED BY: HAFIZ NAVEED UDDIN</p>
        </div>
      </footer>
    </div>
  )
}

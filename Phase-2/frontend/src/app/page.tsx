'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-4">
            <h1 className="text-xl sm:text-2xl font-bold text-blue-600">Task Manager</h1>
            <div className="flex gap-2 sm:gap-4 w-full sm:w-auto">
              <Link
                href="/auth/login"
                className="flex-1 sm:flex-none px-3 sm:px-4 py-2 text-blue-600 hover:text-blue-800 font-medium text-center sm:text-left"
              >
                Login
              </Link>
              <Link
                href="/auth/signup"
                className="flex-1 sm:flex-none px-3 sm:px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-center"
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
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-dark mb-4 sm:mb-6">
            Manage Your Tasks Efficiently
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-gray-600 mb-8 sm:mb-12 max-w-2xl mx-auto px-2">
            A powerful task management system to organize your work, track progress,
            and achieve your goals with ease.
          </p>

          {/* Feature Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8 mt-8 sm:mt-12 mb-8 sm:mb-12">
            <div className="card card-hover">
              <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">✓</div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3">Easy to Use</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Intuitive interface for managing your tasks efficiently
              </p>
            </div>

            <div className="card card-hover">
              <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">📊</div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3">Track Progress</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Monitor task completion and stay on top of your goals
              </p>
            </div>

            <div className="card card-hover">
              <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🔒</div>
              <h3 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-3">Secure & Private</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Your data is encrypted and only accessible to you
              </p>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
            <Link
              href="/auth/signup"
              className="px-6 sm:px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-base sm:text-lg text-center"
            >
              Get Started
            </Link>
            <Link
              href="/auth/login"
              className="px-6 sm:px-8 py-3 bg-white text-blue-600 rounded-lg hover:bg-gray-50 font-medium text-base sm:text-lg text-center border-2 border-blue-600"
            >
              Sign In
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-dark text-white py-6 sm:py-8 mt-12 sm:mt-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 text-center">
          <p className="text-sm sm:text-base">&copy; 2025 Hackathon-2 Task Manager. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

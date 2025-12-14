'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">Task Manager</h1>
          <div className="space-x-4">
            <Link
              href="/auth/login"
              className="px-4 py-2 text-blue-600 hover:text-blue-800 font-medium"
            >
              Login
            </Link>
            <Link
              href="/auth/signup"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-4 py-20 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-dark mb-4">
          Manage Your Tasks Efficiently
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          A powerful task management system to organize your work, track progress,
          and achieve your goals with ease.
        </p>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12 mb-12">
          <div className="card card-hover">
            <div className="text-4xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">Easy to Use</h3>
            <p className="text-gray-600">
              Intuitive interface for managing your tasks efficiently
            </p>
          </div>

          <div className="card card-hover">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Track Progress</h3>
            <p className="text-gray-600">
              Monitor task completion and stay on top of your goals
            </p>
          </div>

          <div className="card card-hover">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold mb-2">Secure & Private</h3>
            <p className="text-gray-600">
              Your data is encrypted and only accessible to you
            </p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="space-x-4">
          <Link
            href="/auth/signup"
            className="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-lg"
          >
            Get Started
          </Link>
          <Link
            href="/auth/login"
            className="inline-block px-8 py-3 bg-white text-blue-600 rounded-lg hover:bg-gray-50 font-medium text-lg border-2 border-blue-600"
          >
            Sign In
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-dark text-white mt-20 py-8">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>&copy; 2025 Hackathon-2 Task Manager. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

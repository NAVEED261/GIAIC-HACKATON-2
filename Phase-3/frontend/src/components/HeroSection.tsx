'use client'

import Link from 'next/link'

export default function HeroSection() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden pt-20">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      </div>

      {/* Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-screen flex flex-col justify-center">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

          {/* Left Content */}
          <div className="space-y-8 animate-fade-in">
            <div>
              <span className="inline-block px-4 py-2 bg-purple-500/20 border border-purple-500/50 rounded-full text-sm font-semibold text-purple-300 mb-6">
                ✨ AI-Powered Task Management
              </span>
              <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold leading-tight mb-4">
                <span className="bg-gradient-to-r from-purple-300 via-cyan-300 to-purple-300 bg-clip-text text-transparent">
                  Master Your Tasks
                </span>
                <br />
                <span className="text-slate-100">with AI</span>
              </h2>
            </div>

            <p className="text-lg text-slate-400 leading-relaxed max-w-xl">
              Meet your intelligent task assistant. Powered by advanced AI, our platform helps you manage, organize, and complete your tasks effortlessly using natural language conversations.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/chat"
                className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold rounded-xl shadow-lg shadow-cyan-500/40 hover:shadow-cyan-500/60 transition-all duration-300 transform hover:scale-105 text-center"
              >
                Start Chat Now
              </Link>
              <Link
                href="/signup"
                className="px-8 py-4 border-2 border-slate-600 hover:border-slate-500 text-slate-300 hover:text-white font-bold rounded-xl backdrop-blur transition-all duration-300 text-center"
              >
                Learn More
              </Link>
            </div>

            {/* Feature Grid */}
            <div className="grid grid-cols-2 gap-4 pt-8">
              <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-4 backdrop-blur hover:bg-slate-700/50 transition">
                <span className="text-2xl mb-2 block">📝</span>
                <p className="text-sm text-slate-300 font-semibold">Add Tasks</p>
                <p className="text-xs text-slate-500 mt-1">Just describe what you need</p>
              </div>
              <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-4 backdrop-blur hover:bg-slate-700/50 transition">
                <span className="text-2xl mb-2 block">📋</span>
                <p className="text-sm text-slate-300 font-semibold">Organize</p>
                <p className="text-xs text-slate-500 mt-1">Smart categorization</p>
              </div>
              <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-4 backdrop-blur hover:bg-slate-700/50 transition">
                <span className="text-2xl mb-2 block">✔️</span>
                <p className="text-sm text-slate-300 font-semibold">Track Progress</p>
                <p className="text-xs text-slate-500 mt-1">Stay on top of goals</p>
              </div>
              <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-4 backdrop-blur hover:bg-slate-700/50 transition">
                <span className="text-2xl mb-2 block">🚀</span>
                <p className="text-sm text-slate-300 font-semibold">Achieve More</p>
                <p className="text-xs text-slate-500 mt-1">AI-powered insights</p>
              </div>
            </div>
          </div>

          {/* Right Content - Visual */}
          <div className="hidden lg:flex items-center justify-center">
            <div className="relative w-full h-96 flex items-center justify-center">
              {/* Chat Bubble Animation */}
              <div className="absolute w-64 h-80 bg-gradient-to-br from-slate-700 to-slate-800 border border-slate-600/50 rounded-2xl shadow-2xl shadow-purple-500/20 backdrop-blur p-6 space-y-4">
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-sm">🤖</span>
                  </div>
                  <div className="flex-1 bg-slate-600/50 rounded-lg p-3">
                    <p className="text-xs text-slate-300">I'll help you manage all your tasks efficiently</p>
                  </div>
                </div>

                <div className="flex gap-3 justify-end">
                  <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg p-3 max-w-xs">
                    <p className="text-xs text-white">Add task: Complete project report</p>
                  </div>
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-sm">👤</span>
                  </div>
                </div>

                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-sm">🤖</span>
                  </div>
                  <div className="flex-1 bg-slate-600/50 rounded-lg p-3">
                    <p className="text-xs text-slate-300">✅ Task added! Due date set for tomorrow</p>
                  </div>
                </div>

                <div className="relative pt-4">
                  <input
                    type="text"
                    placeholder="Tell me what to do..."
                    className="w-full bg-slate-600/50 border border-slate-500/50 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
                    disabled
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats/Trust Section */}
        <div className="mt-20 pt-20 border-t border-slate-700/50 grid grid-cols-3 gap-8 text-center">
          <div>
            <p className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-cyan-300 bg-clip-text text-transparent">1000+</p>
            <p className="text-slate-400 text-sm mt-2">Active Users</p>
          </div>
          <div>
            <p className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-cyan-300 bg-clip-text text-transparent">10K+</p>
            <p className="text-slate-400 text-sm mt-2">Tasks Completed</p>
          </div>
          <div>
            <p className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-cyan-300 bg-clip-text text-transparent">99%</p>
            <p className="text-slate-400 text-sm mt-2">Satisfaction Rate</p>
          </div>
        </div>
      </div>
    </section>
  )
}

'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="fixed w-full top-0 z-50 bg-gradient-to-r from-slate-900/95 via-slate-900/95 to-slate-900/95 backdrop-blur-xl border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">

          {/* Left Side - Logo */}
          <Link href="/" className="flex items-center gap-2 group cursor-pointer">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg shadow-purple-500/50 group-hover:shadow-purple-500/75 transition-all duration-300">
              <span className="text-xl font-bold text-white">✓</span>
            </div>
            <span className="text-sm font-semibold text-slate-300 hidden sm:inline">TODO</span>
          </Link>

          {/* Center - App Name */}
          <div className="flex-1 text-center">
            <h1 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-300 via-cyan-300 to-purple-300 bg-clip-text text-transparent">
              FATIMA ZEHRAA TODO APP
            </h1>
          </div>

          {/* Right Side - Auth Buttons (Desktop) */}
          <div className="hidden md:flex items-center gap-4">
            <Link
              href="/tasks"
              className="px-6 py-2 text-slate-300 hover:text-white font-semibold transition-colors duration-200 border border-slate-600/50 hover:border-slate-500/75 rounded-lg backdrop-blur"
            >
              📋 Tasks
            </Link>
            <Link
              href="/signin"
              className="px-6 py-2 text-slate-300 hover:text-white font-semibold transition-colors duration-200 border border-slate-600/50 hover:border-slate-500/75 rounded-lg backdrop-blur"
            >
              Sign In
            </Link>
            <Link
              href="/signup"
              className="px-6 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold rounded-lg shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 transition-all duration-200 transform hover:scale-105"
            >
              Sign Up
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden w-10 h-10 flex flex-col justify-center items-center gap-1.5 hover:bg-slate-700/50 rounded-lg transition"
          >
            <span className={`w-6 h-0.5 bg-slate-300 transition-all duration-300 ${isOpen ? 'rotate-45 translate-y-2' : ''}`}></span>
            <span className={`w-6 h-0.5 bg-slate-300 transition-all duration-300 ${isOpen ? 'opacity-0' : ''}`}></span>
            <span className={`w-6 h-0.5 bg-slate-300 transition-all duration-300 ${isOpen ? '-rotate-45 -translate-y-2' : ''}`}></span>
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4 space-y-2 animate-fade-in">
            <Link
              href="/tasks"
              className="block w-full px-4 py-2 text-slate-300 hover:text-white font-semibold transition-colors duration-200 border border-slate-600/50 rounded-lg backdrop-blur text-center"
              onClick={() => setIsOpen(false)}
            >
              📋 Tasks
            </Link>
            <Link
              href="/signin"
              className="block w-full px-4 py-2 text-slate-300 hover:text-white font-semibold transition-colors duration-200 border border-slate-600/50 rounded-lg backdrop-blur text-center"
              onClick={() => setIsOpen(false)}
            >
              Sign In
            </Link>
            <Link
              href="/signup"
              className="block w-full px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold rounded-lg shadow-lg shadow-cyan-500/30 text-center transition-all duration-200"
              onClick={() => setIsOpen(false)}
            >
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

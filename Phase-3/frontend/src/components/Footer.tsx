'use client'

import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-900 border-t border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">

        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">

          {/* Brand Column */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg">
                <span className="text-lg font-bold text-white">✓</span>
              </div>
              <span className="font-semibold text-white text-lg">FATIMA TODO</span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed">
              Master your tasks with AI-powered assistance. Organize, track, and achieve your goals effortlessly.
            </p>
            <div className="flex gap-4 pt-4">
              <a href="#" className="w-10 h-10 bg-slate-700/50 hover:bg-slate-600/50 rounded-full flex items-center justify-center text-slate-300 hover:text-cyan-400 transition">
                <span>f</span>
              </a>
              <a href="#" className="w-10 h-10 bg-slate-700/50 hover:bg-slate-600/50 rounded-full flex items-center justify-center text-slate-300 hover:text-cyan-400 transition">
                <span>𝕏</span>
              </a>
              <a href="#" className="w-10 h-10 bg-slate-700/50 hover:bg-slate-600/50 rounded-full flex items-center justify-center text-slate-300 hover:text-cyan-400 transition">
                <span>in</span>
              </a>
            </div>
          </div>

          {/* Product Column */}
          <div className="space-y-4">
            <h3 className="font-semibold text-white text-lg">Product</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Features
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Pricing
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Security
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Roadmap
                </Link>
              </li>
            </ul>
          </div>

          {/* Company Column */}
          <div className="space-y-4">
            <h3 className="font-semibold text-white text-lg">Company</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Blog
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Careers
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal Column */}
          <div className="space-y-4">
            <h3 className="font-semibold text-white text-lg">Legal</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Cookie Policy
                </Link>
              </li>
              <li>
                <Link href="/" className="text-slate-400 hover:text-cyan-400 text-sm transition">
                  Accessibility
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-slate-700/50 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-400 text-sm">
              © 2024 Fatima Zehraa Todo App. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              <p className="text-slate-500 text-sm">
                Made with <span className="text-red-400">❤</span> for productivity
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

import './globals.css'

export const metadata = {
  title: 'Todo Assistant - AI Chat',
  description: 'Manage your tasks with AI-powered chat',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-white">{children}</body>
    </html>
  )
}

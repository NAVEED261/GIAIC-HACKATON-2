# Frontend - Task Management System

Phase-2 Frontend: React/Next.js web application for task management with user authentication and responsive design.

## Technology Stack

- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **State Management:** Zustand
- **UI Components:** Custom React components

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── layout.tsx    # Root layout
│   │   ├── globals.css   # Global styles
│   │   ├── page.tsx      # Home/landing page
│   │   └── auth/         # Authentication pages
│   ├── components/       # Reusable React components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utility functions
│   ├── types/            # TypeScript type definitions
│   └── store/            # Zustand state management
├── public/               # Static assets
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── next.config.js        # Next.js config
├── tailwind.config.ts    # Tailwind CSS config
├── postcss.config.js     # PostCSS config
└── .eslintrc.json        # ESLint config
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd Phase-2/frontend
npm install
```

### 2. Environment Configuration

Create `.env.local` from `.env.example`:

```bash
cp .env.example .env.local
```

Configure the backend API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Development Server

```bash
npm run dev
```

Access the application at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

### 5. Type Checking

```bash
npm run type-check
```

### 6. Linting

```bash
npm run lint
```

## Features (Phase 2C)

### Step 9: Frontend Setup ✓
- [x] Next.js 16+ with App Router
- [x] TypeScript configuration
- [x] Tailwind CSS setup
- [x] Project structure
- [x] Environment configuration
- [x] Home/landing page

### Step 10: Authentication Pages (In Progress)
- [ ] Signup page with form
- [ ] Login page with form
- [ ] Form validation
- [ ] Error/success messages
- [ ] JWT token storage
- [ ] Logout functionality

### Step 11: Task Management Pages (Pending)
- [ ] Dashboard with task list
- [ ] Create task form
- [ ] Edit task form
- [ ] Task filtering and search
- [ ] Task status management
- [ ] Delete task confirmation

### Step 12: API Integration (Pending)
- [ ] API client setup
- [ ] Data fetching hooks
- [ ] Error handling
- [ ] Loading states
- [ ] Retry logic

### Step 13: Responsive Design (Pending)
- [ ] Mobile-first approach
- [ ] Breakpoint testing
- [ ] Touch-friendly UI
- [ ] Accessibility improvements

## API Integration

The frontend connects to the backend API at:

```
http://localhost:8000 (default)
```

### Authentication Endpoints

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user

### Task Endpoints

- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Mark complete

## File Organization

### Pages (`src/app/`)
- `page.tsx` - Home/landing page
- `auth/signup/page.tsx` - Sign up page
- `auth/login/page.tsx` - Login page
- `dashboard/page.tsx` - Task dashboard
- `tasks/create/page.tsx` - Create task form
- `tasks/[id]/edit/page.tsx` - Edit task form

### Components (`src/components/`)
- `AuthForm.tsx` - Reusable auth form
- `TaskList.tsx` - Display tasks
- `TaskCard.tsx` - Individual task card
- `TaskForm.tsx` - Create/edit form
- `TaskFilters.tsx` - Filter controls
- `Navigation.tsx` - Header/navbar
- `Loading.tsx` - Loading spinner

### Hooks (`src/hooks/`)
- `useAuth.ts` - Authentication logic
- `useTasks.ts` - Task operations
- `useApi.ts` - API client

### Store (`src/store/`)
- `authStore.ts` - User auth state
- `taskStore.ts` - Task state

### Types (`src/types/`)
- `auth.ts` - Auth type definitions
- `task.ts` - Task type definitions

## Styling

### Tailwind CSS

- Responsive breakpoints: `sm:` (640px), `md:` (768px), `lg:` (1024px)
- Custom color scheme in `tailwind.config.ts`
- Global utilities in `globals.css`

### Color Palette

- Primary: Blue (#3b82f6)
- Secondary: Purple (#8b5cf6)
- Success: Green (#10b981)
- Warning: Amber (#f59e0b)
- Danger: Red (#ef4444)

## Development Guidelines

### Component Structure

```typescript
'use client'  // Use client component for interactivity

import { useState } from 'react'

export default function MyComponent() {
  const [state, setState] = useState()

  return (
    <div className="p-4 bg-white rounded-lg">
      {/* Component content */}
    </div>
  )
}
```

### Custom Hooks

```typescript
// hooks/useCustom.ts
import { useState, useEffect } from 'react'

export function useCustom() {
  const [data, setData] = useState(null)

  useEffect(() => {
    // Hook logic
  }, [])

  return { data }
}
```

### Form Handling

Use native HTML forms with validation:

```typescript
<form onSubmit={handleSubmit}>
  <input
    type="email"
    required
    placeholder="Email"
  />
  <button type="submit">Submit</button>
</form>
```

## Testing (Phase 2D)

- Unit tests for components
- Integration tests for API calls
- E2E tests for user workflows
- Mock API responses for development

## Performance Tips

- Use `next/image` for optimized images
- Lazy load components with `dynamic()`
- Implement pagination for large lists
- Cache API responses where appropriate
- Minimize bundle size with code splitting

## Security

- Store JWT tokens in secure httpOnly cookies
- Validate all user input
- Sanitize output to prevent XSS
- Use environment variables for secrets
- Enforce HTTPS in production

## Common Commands

```bash
# Development
npm run dev

# Build
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
npm run lint -- --fix
```

## Troubleshooting

### Port 3000 already in use
```bash
PORT=3001 npm run dev
```

### Module not found errors
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

### Build failures
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Backend Integration

The frontend is designed to work with the Phase-2 backend API:

- **Base URL:** `NEXT_PUBLIC_API_URL` environment variable
- **Authentication:** JWT Bearer tokens in Authorization header
- **Data Format:** JSON request/response
- **Error Handling:** Consistent error response format

## Next Steps

1. Create authentication pages (Step 10)
2. Implement API integration (Step 12)
3. Build task management pages (Step 11)
4. Add responsive design (Step 13)
5. Comprehensive testing (Phase 2D)

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Documentation](https://react.dev)

## Support

For issues or questions, refer to the main project documentation in the parent directory.

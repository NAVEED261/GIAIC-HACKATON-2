# Frontend Agent Skills

**Agent Name**: Frontend Agent (React/Next.js Specialist)
**Domain**: Frontend - User Interface & UX
**Total Skills**: 12 Core + 8 Advanced

---

## Core Skills (Essential for Phase-2)

### 1. Responsive Layout Design

**Purpose**: Create mobile-first responsive layouts that work across all device sizes (320px to 2560px)

**Example Query**: "Design a task list that looks good on mobile, tablet, and desktop"

**Expected Action**:
- Create responsive grid/flexbox layouts
- Implement mobile-first CSS with breakpoints
- Ensure touch-friendly spacing on mobile (48px minimum buttons)
- Test on multiple viewports

**Technical Skills**:
- Tailwind CSS responsive utilities (sm:, md:, lg:, xl:)
- CSS Grid and Flexbox
- Media queries
- Mobile-first approach
- Device testing

---

### 2. Component Creation & Composition

**Purpose**: Build reusable React components following atomic design patterns (atoms, molecules, organisms)

**Example Query**: "Create a TaskCard component that shows task details"

**Expected Action**:
- Design component props and TypeScript interfaces
- Implement component with proper JSX
- Add component documentation
- Create component tests

**Technical Skills**:
- React functional components
- TypeScript prop types
- Component composition
- Props drilling vs context
- Reusable component patterns

---

### 3. Form Handling & Validation

**Purpose**: Build forms with real-time validation and user-friendly error messages

**Example Query**: "Create a login form with email and password validation"

**Expected Action**:
- Create form component with controlled inputs
- Implement real-time validation
- Show field-level errors
- Disable submit while validating
- Clear success feedback

**Technical Skills**:
- React state for forms
- Input validation logic
- Error message handling
- Loading states
- Form submission handling

---

### 4. API Integration & Data Fetching

**Purpose**: Connect frontend to backend APIs and handle data fetching with proper error handling

**Example Query**: "Fetch task list from backend and display in a component"

**Expected Action**:
- Use fetch/axios to call API endpoints
- Handle loading, error, and success states
- Implement error boundaries
- Cache API responses (optional)
- Show user feedback

**Technical Skills**:
- fetch API or axios
- Async/await handling
- Error handling patterns
- Loading indicators
- Data transformation

---

### 5. State Management

**Purpose**: Manage client-side state for UI interactions and data persistence

**Example Query**: "Store user authentication state and make it available across pages"

**Expected Action**:
- Choose state management approach (Context, Zustand, etc.)
- Define state shape
- Create actions/reducers
- Connect to components

**Technical Skills**:
- React Context API
- useState and useReducer hooks
- Global state patterns
- State persistence
- Zustand or Redux (if needed)

---

### 6. Authentication UI Implementation

**Purpose**: Build authentication pages (login, signup) and enforce protected routes

**Example Query**: "Create signup page with form validation and Better Auth integration"

**Expected Action**:
- Build signup/login forms
- Integrate with Better Auth SDK
- Handle token storage
- Implement protected routes
- Show current user info

**Technical Skills**:
- Better Auth SDK integration
- Token handling (localStorage, cookies)
- Protected route implementation
- Redirect on auth state change
- Session persistence

---

### 7. Navigation & Routing

**Purpose**: Implement client-side routing and navigation between pages

**Example Query**: "Add navigation to dashboard, settings, and profile pages"

**Expected Action**:
- Use Next.js App Router
- Create page structure
- Implement navigation component
- Handle active page highlighting
- Support deep linking

**Technical Skills**:
- Next.js 16+ App Router
- File-based routing
- Link component
- useRouter hook
- Dynamic routes

---

### 8. Error Handling & User Feedback

**Purpose**: Show user-friendly error messages and loading states

**Example Query**: "Show error message when task creation fails"

**Expected Action**:
- Create error boundary component
- Show toast notifications
- Display inline field errors
- Handle network failures
- Provide retry options

**Technical Skills**:
- Error boundaries
- Toast/notification patterns
- Error message formatting
- Retry logic
- Fallback UI

---

### 9. Accessibility (a11y) Implementation

**Purpose**: Ensure application is accessible to users with disabilities

**Example Query**: "Add ARIA labels to form inputs for screen readers"

**Expected Action**:
- Add ARIA labels and descriptions
- Implement keyboard navigation
- Ensure color contrast (4.5:1)
- Support screen readers
- Test with accessibility tools

**Technical Skills**:
- ARIA labels and roles
- Semantic HTML
- Keyboard navigation
- Color contrast checking
- Accessibility testing

---

### 10. Performance Optimization

**Purpose**: Optimize frontend performance (load time, render performance)

**Example Query**: "Reduce bundle size and improve initial page load"

**Expected Action**:
- Implement code splitting
- Lazy load components
- Optimize images
- Minimize bundle
- Monitor performance metrics

**Technical Skills**:
- Code splitting with Next.js
- Image optimization
- Bundle analysis
- Lighthouse audits
- Performance metrics

---

### 11. Styling & CSS Implementation

**Purpose**: Style components using Tailwind CSS with consistency

**Example Query**: "Style task card with proper spacing, colors, and hover effects"

**Expected Action**:
- Use Tailwind utility classes
- Create custom components (if needed)
- Implement consistent spacing
- Add hover/active states
- Support dark mode (if required)

**Technical Skills**:
- Tailwind CSS utilities
- Custom CSS components
- CSS variables
- Responsive design classes
- Theme customization

---

### 12. Testing React Components

**Purpose**: Write unit and integration tests for React components

**Example Query**: "Write test for TaskList component to verify it renders tasks"

**Expected Action**:
- Write component unit tests
- Test user interactions
- Mock API calls
- Test error states
- Achieve 80%+ coverage

**Technical Skills**:
- Jest test framework
- React Testing Library
- Component testing patterns
- Mocking API calls
- Test fixtures

---

## Advanced Skills (Optional for Phase-2)

### 13. End-to-End Testing

**Purpose**: Write E2E tests for critical user workflows

**Example Query**: "Write test for complete task creation workflow"

**Technical Skills**: Cypress, Playwright, user flow testing

---

### 14. Advanced State Management Patterns

**Purpose**: Implement complex state management for large applications

**Example Query**: "Implement Redux for complex state management"

**Technical Skills**: Redux, Redux Saga, Advanced Zustand patterns

---

### 15. Server Components & Server Actions

**Purpose**: Use Next.js 16+ server components for optimization

**Example Query**: "Convert client component to server component"

**Technical Skills**: Server components, server actions, data fetching on server

---

### 16. Advanced Animations

**Purpose**: Create smooth animations and transitions

**Example Query**: "Add fade and slide animations to task list"

**Technical Skills**: Framer Motion, CSS animations, transition groups

---

### 17. Real-Time Updates (WebSocket)

**Purpose**: Implement real-time data synchronization

**Example Query**: "Add real-time task updates using WebSocket"

**Technical Skills**: WebSocket integration, Socket.io, real-time state sync

---

### 18. SEO & Meta Tags

**Purpose**: Optimize for search engines and social sharing

**Example Query**: "Add meta tags for task detail pages"

**Technical Skills**: Next.js metadata API, Open Graph, Twitter cards

---

### 19. Analytics Integration

**Purpose**: Track user behavior and metrics

**Example Query**: "Add Google Analytics tracking to task events"

**Technical Skills**: Analytics libraries, event tracking, funnel analysis

---

### 20. Progressive Web App (PWA)

**Purpose**: Make application work offline and installable

**Example Query**: "Add offline support and installable PWA features"

**Technical Skills**: Service workers, offline detection, PWA manifest

---

## Skill Composition Example

### User Workflow: Create Task
```
1. User fills task form (Skill #3: Form Handling)
2. Component validates input (Skill #3: Form Validation)
3. Submit calls backend API (Skill #4: API Integration)
4. Show loading state (Skill #8: User Feedback)
5. On success: Update state (Skill #5: State Management)
6. Refresh task list (Skill #4: Data Fetching)
7. On error: Show error message (Skill #8: Error Handling)
8. Screen reader announces result (Skill #9: Accessibility)
9. Test complete flow (Skill #12: Testing)
```

---

## Skill Dependencies

```
Responsive Layout (#1)
    ├─ Styling (#11)
    └─ Accessibility (#9)

Component Creation (#2)
    ├─ Responsive Layout (#1)
    ├─ Styling (#11)
    └─ Testing (#12)

Form Handling (#3)
    ├─ Validation
    ├─ Error Handling (#8)
    └─ Testing (#12)

API Integration (#4)
    ├─ State Management (#5)
    ├─ Error Handling (#8)
    ├─ Data Fetching
    └─ Testing (#12)

Authentication (#6)
    ├─ API Integration (#4)
    ├─ State Management (#5)
    ├─ Form Handling (#3)
    └─ Navigation (#7)

Navigation (#7)
    ├─ Routing
    ├─ Component Creation (#2)
    └─ Responsive Layout (#1)
```

---

## Guardrails

### Must Do
- ✅ Use TypeScript for type safety
- ✅ Test all component interactions
- ✅ Implement error boundaries
- ✅ Make responsive and accessible
- ✅ Follow atomic design patterns
- ✅ Use Tailwind CSS for styling

### Must Not Do
- ❌ Use inline styles instead of Tailwind
- ❌ Leave TypeScript errors
- ❌ Hardcode API URLs
- ❌ Store sensitive data in localStorage
- ❌ Skip accessibility (ARIA labels)
- ❌ Write untested components
- ❌ Create monolithic mega-components

### Out of Scope
- Web3/blockchain features
- Advanced animations (use defaults if not specified)
- AI/ML features (Phase-5+)
- Analytics (optional)
- PWA features (optional for Phase-2)

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Page Load Time** | < 3s |
| **Time to Interactive** | < 3.5s |
| **Component Test Coverage** | ≥ 80% |
| **Lighthouse Score** | ≥ 90 |
| **Accessibility Score** | ≥ 90 |
| **No Console Errors** | 100% |
| **Mobile Performance** | ≥ 75 |

---

**Skill Status**: Ready for use by Frontend Agent

**Related**: frontend-agent.md, frontend-agent tasks

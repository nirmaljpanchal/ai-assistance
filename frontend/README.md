# AI Assistance Frontend

A modern frontend application built with Vite, React, and TypeScript with strict mode enabled.

## Tech Stack

- **Build Tool**: Vite
- **Framework**: React 18
- **Language**: TypeScript (strict mode)
- **Linting**: ESLint with TypeScript support
- **Formatting**: Prettier
- **Testing**: Vitest
- **CSS**: Standard CSS

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The application will open at `http://localhost:3000` with hot module replacement (HMR) enabled.

### Build

Create an optimized production build:

```bash
npm run build
```

### Preview

Preview the production build locally:

```bash
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production (includes TypeScript compilation)
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (fails on errors)
- `npm run lint:fix` - Fix ESLint issues automatically
- `npm run format` - Format code with Prettier
- `npm run test` - Run tests in watch mode
- `npm run test:ui` - Run tests with UI
- `npm run test:run` - Run tests once

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main App component
│   ├── App.css          # App styles
│   ├── App.test.tsx     # App tests
│   ├── index.css        # Global styles
│   └── main.tsx         # Entry point
├── index.html           # HTML entry point
├── vite.config.ts       # Vite configuration
├── vitest.config.ts     # Vitest configuration
├── tsconfig.json        # TypeScript configuration (strict mode)
├── .eslintrc.cjs        # ESLint configuration
├── .prettierrc           # Prettier configuration
└── package.json         # Dependencies and scripts
```

## TypeScript Strict Mode

This project uses TypeScript strict mode with all strict flags enabled:

- `strict: true` - Enables all strict type checking options
- `noImplicitAny` - Disallow implicit `any` types
- `strictNullChecks` - Strict null and undefined checking
- `noImplicitThis` - Disallow implicit `this` types
- `noUnusedLocals` - Report unused local variables
- `noUnusedParameters` - Report unused parameters
- `noImplicitReturns` - Report functions with unreachable end of function

## Code Quality

### Linting

ESLint is configured with:
- TypeScript support
- React Hooks rules
- React Refresh plugin

Run `npm run lint` to check for issues, or `npm run lint:fix` to auto-fix them.

### Formatting

Prettier is configured to maintain consistent code style:
- 2-space indentation
- Single quotes
- Trailing commas
- Line width: 100 characters

Run `npm run format` to format all code.

### Testing

Vitest is configured for unit and component testing with:
- jsdom environment for DOM testing
- React Testing Library for component testing
- UI mode for visual test runner

## Environment Variables

Create a `.env.local` file in the root directory for local development:

```env
VITE_API_URL=http://localhost:8000
```

Access environment variables in the code with `import.meta.env.VITE_*`

## Browser Support

The project targets modern browsers with ES2020 JavaScript support.

# Architecture

The platform uses a split frontend/backend architecture. Next.js owns user experience, client-side state, loading/error states, charts, and Vercel deployment. FastAPI owns generation, validation, persistence, rate controls, and integrations with OpenAI, PostgreSQL, Redis, and vector search.

## Frontend decisions
- Next.js 15 App Router gives route-level composition for landing, generation, quiz-taking, results, and analytics pages.
- TypeScript keeps API contracts explicit through shared `QuizResponse`, `Question`, and `Difficulty` types.
- TailwindCSS and shadcn-style primitives provide fast, consistent, accessible UI without a heavyweight component framework.
- React Query isolates server state, request retries, and loading/error handling from page components.
- Recharts supports bar, pie, and trend charts with responsive containers for dashboard analytics.
- Session storage preserves a demo quiz flow across generator, quiz, and results pages without requiring authentication for the first release.

## Backend decisions
- FastAPI provides async endpoints and generated Swagger documentation.
- SQLAlchemy Async keeps database access non-blocking under concurrent LLM requests.
- PostgreSQL is the source of truth for quizzes, questions, attempts, and analytics.
- Redis is used for cache, rate-limiting buckets, and session payloads.
- Embeddings and vector similarity enforce duplicate detection before a question is accepted.

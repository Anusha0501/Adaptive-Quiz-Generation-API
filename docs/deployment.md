# Deployment Guide

## Frontend: Vercel
1. Set project root to the repository root.
2. Use `vercel.json`, which builds from `frontend/`.
3. Configure `NEXT_PUBLIC_API_BASE_URL` with the Railway backend URL.
4. Deploy and verify the landing page, generator, quiz, results, and analytics routes.

## Backend: Railway
1. Create a Railway service from this repository.
2. Railway uses `railway.toml` and the root `Dockerfile`.
3. Set environment variables from `.env.example`.
4. Configure `DATABASE_URL` with Neon PostgreSQL.
5. Configure `REDIS_URL` with Upstash Redis.
6. Configure `CHROMA_PATH` to a persistent mounted path.
7. Verify `/health` and `/docs` after deployment.

## Database: Neon PostgreSQL
1. Create a Neon project and database.
2. Copy the pooled async connection string into `DATABASE_URL` using the `postgresql+asyncpg://` scheme.
3. Run Alembic migrations from a Railway one-off job or CI deployment step.

## Redis: Upstash
1. Create an Upstash Redis database.
2. Copy the Redis URL into `REDIS_URL`.
3. Use Redis for rate limit counters, quiz cache entries, and session payloads.

## Vector Store: ChromaDB persistent storage
Use `CHROMA_PATH` on a persistent Railway volume or a managed vector-store replacement for production. The duplicate detector uses embeddings and a `0.85` similarity threshold before accepting questions.

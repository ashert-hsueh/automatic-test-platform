from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.config import settings
from app.api.v1 import auth, projects, testcases, jobs

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 路由注册 ──────────────────────────────────────────────
API_PREFIX = settings.API_V1_STR
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(projects.router, prefix=API_PREFIX)
app.include_router(testcases.router, prefix=API_PREFIX)
app.include_router(jobs.router, prefix=API_PREFIX)


@app.get("/", tags=["健康检查"])
async def root():
    return {"message": f"{settings.PROJECT_NAME} is running 🚀", "version": settings.PROJECT_VERSION}


@app.get("/health", tags=["健康检查"])
async def health():
    return {"status": "ok"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.chat import router as chat_router
from api.routers.feedback import router as feedback_router
from api.routers.generate import router as generate_router
from api.routers.analytics import router as analytics_router
from api.routers.reputation import router as reputation_router
from api.config import settings

app = FastAPI(
    title="Customer AI Chat System",
    description="A simple FAQ-based customer support chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(feedback_router, prefix="/api/v1", tags=["feedback"])
app.include_router(generate_router, prefix="/api/v1", tags=["generate"])
app.include_router(analytics_router, prefix="/api/v1", tags=["analytics"])
app.include_router(reputation_router, prefix="/api/v1", tags=["reputation"])

@app.get("/")
async def root():
    return {"message": "Customer AI Chat System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

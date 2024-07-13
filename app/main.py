import logging
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from app.config import settings
from app.routers import trends, auth
from app.utils.error_handler import http_error_handler
from app.services.trends_service import TrendsService
from app.models.trend_models import TrendRequest
from app.utils.auth import get_api_key
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add error handler
app.add_exception_handler(HTTPException, http_error_handler)

# Create API router
api_router = APIRouter()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(trends.router, prefix="/trends", tags=["trends"])

# Add API router to the main app with version prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

# Keep the trend endpoints in the main file for backwards compatibility
@app.get("/trend")
async def get_trend(request: TrendRequest, api_key: str = Depends(get_api_key)):
    try:
        return await TrendsService.get_trend(request.keywords, request.timeframe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/geo-trend/{keyword}")
async def get_geo_trend(keyword: str, api_key: str = Depends(get_api_key)):
    return await TrendsService.get_geo_trend(keyword)

@app.get("/related-queries/{keyword}")
async def get_related_queries(keyword: str, api_key: str = Depends(get_api_key)):
    return await TrendsService.get_related_queries(keyword)

@app.get("/related-topics/{keyword}")
async def get_related_topics(keyword: str, api_key: str = Depends(get_api_key)):
    return await TrendsService.get_related_topics(keyword)

@app.get("/trend-with-news/{keyword}")
async def get_trend_with_news(keyword: str, api_key: str = Depends(get_api_key)):
    trend_data = await TrendsService.get_trend_data(keyword, 'today 12-m')
    news_data = await TrendsService.get_news_data(keyword)
    return {"trend": trend_data[keyword].to_dict(), "news": news_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
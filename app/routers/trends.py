from fastapi import APIRouter, Depends, HTTPException
from app.services.trends_service import TrendsService
from app.models.trend_models import TrendRequest
from app.utils.auth import get_api_key

router = APIRouter()

@router.get("/trend")
async def get_trend(request: TrendRequest, api_key: str = Depends(get_api_key)):
    try:
        return await TrendsService.get_trend(request.keywords, request.timeframe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geo-trend/{keyword}")
async def get_geo_trend(keyword: str, api_key: str = Depends(get_api_key)):
    return await TrendsService.get_geo_trend(keyword)

@router.get("/related-queries/{keyword}")
async def get_related_queries(keyword: str, api_key: str = Depends(get_api_key)):
    return await TrendsService.get_related_queries(keyword)

@router.get("/related-topics/{keyword}")
async def get_related_topics(keyword: str, api_key: str = Depends(get_api_key)):
    return await TrendsService.get_related_topics(keyword)

@router.get("/trend-with-news/{keyword}")
async def get_trend_with_news(keyword: str, api_key: str = Depends(get_api_key)):
    trend_data = await TrendsService.get_trend_data(keyword, 'today 12-m')
    news_data = await TrendsService.get_news_data(keyword)
    return {"trend": trend_data[keyword].to_dict(), "news": news_data}
from pytrends.request import TrendReq
from app.utils.visualization import create_matplotlib_plot
from ..services.cache_service import CacheService


class TrendsService:
    @staticmethod
    async def get_trend_data(keywords: str, timeframe: str):
        # Wrapping the actual fetch function
        def fetch_trend_data():
            pytrends = TrendReq(hl='en-US', tz=360)
            keyword_list = keywords.split(',')
            pytrends.build_payload(keyword_list, timeframe=timeframe)
            return pytrends.interest_over_time()

        return CacheService.get_cached_data(f"trend_data:{keywords}:{timeframe}", fetch_trend_data)

    @staticmethod
    async def get_trend(keywords: str, timeframe: str):
        df = await TrendsService.get_trend_data(keywords, timeframe)
        keyword_list = keywords.split(',')
        plot = create_matplotlib_plot(df, keyword_list)
        trend_data = {keyword: df[keyword].to_dict() for keyword in keyword_list}
        return {
            "keywords": keyword_list,
            "trend_data": trend_data,
            "plot": plot
        }

    @staticmethod
    async def get_geo_trend(keyword: str):
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword])
        return pytrends.interest_by_region().to_dict()

    @staticmethod
    async def get_related_queries(keyword: str):
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword])
        return pytrends.related_queries()

    @staticmethod
    async def get_related_topics(keyword: str):
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword])
        return pytrends.related_topics()

    @staticmethod
    async def get_news_data(keyword: str):
        # This is a placeholder. You would implement actual news API call here.
        return {"articles": [{"title": f"News about {keyword}", "url": "https://example.com"}]}
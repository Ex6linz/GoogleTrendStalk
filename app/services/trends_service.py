from pytrends.request import TrendReq
from app.utils.visualization import create_matplotlib_plot
from ..services.cache_service import CacheService
from datetime import datetime, timedelta


class TrendsService:
    pytrends = TrendReq(hl='en-US', tz=360)

    @staticmethod
    async def get_trend(keywords, timeframe=None):
        if not timeframe:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=2)
            timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"

        TrendsService.pytrends.build_payload(keywords.split(','), cat=0, timeframe=timeframe, geo='', gprop='')
        return TrendsService.pytrends.interest_over_time().to_dict(orient='records')

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
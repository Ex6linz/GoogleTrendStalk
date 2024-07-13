from pydantic import BaseModel, constr

class TrendRequest(BaseModel):
    keywords: constr(min_length=1, max_length=100)
    timeframe: str = 'today 12-m'
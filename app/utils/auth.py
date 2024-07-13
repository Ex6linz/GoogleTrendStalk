import logging
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.config import settings

api_key_header = APIKeyHeader(name='Authorization')

def get_api_key(api_key_header: str = Security(api_key_header)):
    expected_key = f"Bearer {settings.API_KEY}"
    logging.info(f"Received API key: {api_key_header}")
    logging.info(f"Expected API key: {expected_key}")

    if api_key_header == expected_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
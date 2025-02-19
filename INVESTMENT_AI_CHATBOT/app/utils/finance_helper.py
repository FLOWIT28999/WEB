"""
금융 데이터 수집 및 처리를 위한 유틸리티 함수들을 제공하는 모듈입니다.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Tuple
import requests
from datetime import datetime, timedelta
from config.config import ALPHA_VANTAGE_API_KEY

def get_stock_info(ticker: str) -> Dict:
    """
    주식 종목의 기본 정보를 가져옵니다.

    Args:
        ticker (str): 주식 종목 코드 (예: '005930.KS' for 삼성전자)

    Returns:
        Dict: 주식 기본 정보
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'name': info.get('longName', 'N/A'),
            'current_price': info.get('currentPrice', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'per': info.get('forwardPE', 'N/A'),
            'pbr': info.get('priceToBook', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'description': info.get('longBusinessSummary', 'N/A')
        }
    except Exception as e:
        return {'error': f'주식 정보 조회 중 오류 발생: {str(e)}'}

def get_stock_history(
    ticker: str,
    period: str = '1y',
    interval: str = '1d'
) -> Optional[pd.DataFrame]:
    """
    주식의 히스토리 데이터를 가져옵니다.

    Args:
        ticker (str): 주식 종목 코드
        period (str): 데이터 기간 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval (str): 데이터 간격 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

    Returns:
        Optional[pd.DataFrame]: 주가 히스토리 데이터
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period, interval=interval)
        return history
    except Exception as e:
        print(f'주가 히스토리 조회 중 오류 발생: {str(e)}')
        return None
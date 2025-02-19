"""
금융 데이터 수집 및 처리를 위한 유틸리티 함수들을 제공하는 모듈입니다.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Tuple
import requests
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import ALPHA_VANTAGE_API_KEY

def format_korean_ticker(ticker: str) -> str:
    """
    한국 주식 종목 코드를 Yahoo Finance 형식으로 변환합니다.
    예: '005930' -> '005930.KS'
    """
    # 이미 .KS가 포함된 경우 그대로 반환
    if '.KS' in ticker:
        return ticker
    
    # 숫자로만 이루어진 경우 .KS 추가
    if ticker.isdigit():
        return f"{ticker}.KS"
    
    return ticker

def get_stock_info(ticker: str) -> Dict:
    """
    주식 종목의 기본 정보를 가져옵니다.

    Args:
        ticker (str): 주식 종목 코드 (예: '005930' 또는 '005930.KS')

    Returns:
        Dict: 주식 기본 정보
    """
    try:
        formatted_ticker = format_korean_ticker(ticker)
        stock = yf.Ticker(formatted_ticker)
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
        formatted_ticker = format_korean_ticker(ticker)
        stock = yf.Ticker(formatted_ticker)
        history = stock.history(period=period, interval=interval)
        return history
    except Exception as e:
        print(f'주가 히스토리 조회 중 오류 발생: {str(e)}')
        return None

def calculate_technical_indicators(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    기술적 지표를 계산합니다.

    Args:
        df (pd.DataFrame): 주가 데이터

    Returns:
        Tuple[pd.DataFrame, Dict]: 지표가 추가된 데이터프레임과 기술적 분석 결과
    """
    # 이동평균선 계산
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA60'] = df['Close'].rolling(window=60).mean()
    
    # RSI 계산 (14일)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD 계산
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # 기술적 분석 결과
    latest = df.iloc[-1]
    analysis = {
        'trend': '상승' if latest['MA5'] > latest['MA20'] else '하락',
        'rsi_status': '과매수' if latest['RSI'] > 70 else '과매도' if latest['RSI'] < 30 else '중립',
        'macd_signal': '매수' if latest['MACD'] > latest['Signal_Line'] else '매도'
    }
    
    return df, analysis

def get_company_news(ticker: str) -> list:
    """
    회사 관련 최신 뉴스를 가져옵니다.

    Args:
        ticker (str): 주식 종목 코드

    Returns:
        list: 뉴스 기사 리스트
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        formatted_news = []
        for article in news[:5]:  # 최근 5개 뉴스만 가져옴
            formatted_news.append({
                'title': article.get('title', ''),
                'link': article.get('link', ''),
                'publisher': article.get('publisher', ''),
                'published': datetime.fromtimestamp(article.get('providerPublishTime', 0))
            })
        
        return formatted_news
    except Exception as e:
        return [{'error': f'뉴스 조회 중 오류 발생: {str(e)}'}] 
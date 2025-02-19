"""
OpenAI API를 활용한 투자 조언 관련 유틸리티 함수들을 제공하는 모듈입니다.
"""

import openai
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import OPENAI_API_KEY, GPT_MODEL, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

def get_investment_advice(
    user_message: str,
    chat_history: List[Dict[str, str]] = None
) -> str:
    """
    사용자의 투자 관련 질문에 대한 AI 조언을 제공합니다.

    Args:
        user_message (str): 사용자의 질문
        chat_history (List[Dict[str, str]], optional): 이전 대화 기록

    Returns:
        str: AI의 투자 조언
    """
    if chat_history is None:
        chat_history = []

    # 시스템 프롬프트를 포함한 메시지 구성
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # 이전 대화 기록 추가
    messages.extend(chat_history)

    # 현재 사용자 메시지 추가
    messages.append({"role": "user", "content": user_message})

    try:
        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        
        return response.choices[0].message.content

    except Exception as e:
        error_message = f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}"
        return error_message

def analyze_stock(stock_info: Dict) -> str:
    """
    주식 정보를 분석하여 AI의 분석 결과를 제공합니다.

    Args:
        stock_info (Dict): 주식 관련 정보 (가격, 재무제표, 뉴스 등)

    Returns:
        str: AI의 주식 분석 결과
    """
    # 주식 분석을 위한 프롬프트 구성
    analysis_prompt = f"""
    다음 주식 정보를 분석하여 투자자에게 도움이 될 만한 인사이트를 제공해주세요:
    
    기업: {stock_info.get('name', 'N/A')}
    현재가: {stock_info.get('current_price', 'N/A')}
    시가총액: {stock_info.get('market_cap', 'N/A')}
    PER: {stock_info.get('per', 'N/A')}
    PBR: {stock_info.get('pbr', 'N/A')}
    최근 뉴스: {stock_info.get('recent_news', 'N/A')}
    
    다음 사항을 포함해주세요:
    1. 기업의 현재 상황 분석
    2. 주요 재무지표 평가
    3. 투자 위험 요소
    4. 향후 전망
    """

    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        
        return response.choices[0].message.content

    except Exception as e:
        error_message = f"주식 분석 중 오류가 발생했습니다: {str(e)}"
        return error_message 
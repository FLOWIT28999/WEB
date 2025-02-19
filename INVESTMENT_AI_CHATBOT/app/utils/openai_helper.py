"""
OpenAI API를 활용한 투자 조언 관련 유틸리티 함수들을 제공하는 모듈입니다.
"""

from openai import Openai
from typing import List, Dict
from config.config import OPENAI_API_KEY, GPT_MODEL, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT

client = Openai(api_key=OPENAI_API_KEY)

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
        completion = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        error_message = f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}"
        return error_message 
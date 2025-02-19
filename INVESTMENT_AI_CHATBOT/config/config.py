"""
환경 변수 및 설정을 관리하는 모듈입니다.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# 로컬 개발 환경에서는 .env 파일 로드
if os.path.exists(".env"):
    load_dotenv()

# API 키 설정 (Streamlit Cloud의 secrets에서 가져오거나 환경 변수에서 가져옴)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"] if "ALPHA_VANTAGE_API_KEY" in st.secrets else os.getenv("ALPHA_VANTAGE_API_KEY")

# OpenAI 모델 설정
GPT_MODEL = "gpt-3.5-turbo"  # 사용할 GPT 모델

# 투자 조언 시스템 설정
MAX_TOKENS = 1000  # 응답 최대 토큰 수
TEMPERATURE = 0.7  # 응답의 창의성 정도 (0: 보수적, 1: 창의적)

# 챗봇 시스템 프롬프트
SYSTEM_PROMPT = """
당신은 투자 전문가 AI 어시스턴트입니다. 
다음과 같은 원칙을 따라 사용자의 질문에 답변해주세요:

1. 객관적이고 정확한 정보를 제공합니다.
2. 투자의 위험성을 항상 고지합니다.
3. 개인의 투자 성향과 리스크 허용도를 고려합니다.
4. 장기적인 관점에서 조언을 제공합니다.
5. 투자 교육적 관점을 유지합니다.
"""

# Streamlit 페이지 설정
PAGE_TITLE = "투자 조언 AI 챗봇"
PAGE_ICON = "��"
LAYOUT = "wide" 
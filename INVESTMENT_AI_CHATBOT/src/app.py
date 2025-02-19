"""
투자 조언 AI 챗봇의 메인 Streamlit 애플리케이션입니다.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.openai_helper import get_investment_advice, analyze_stock
from utils.finance_helper import (
    get_stock_info,
    get_stock_history,
    calculate_technical_indicators,
    get_company_news
)
from config.config import PAGE_TITLE, PAGE_ICON, LAYOUT

# 페이지 설정
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    """
    메인 애플리케이션 함수
    """
    st.title("💰 투자 조언 AI 챗봇")
    st.markdown("---")

    # 사이드바 - 주식 분석
    with st.sidebar:
        st.subheader("주식 분석")
        ticker = st.text_input(
            "종목 코드를 입력하세요 (예: 005930.KS)",
            placeholder="005930.KS"
        )
        
        if ticker:
            stock_info = get_stock_info(ticker)
            
            if 'error' not in stock_info:
                st.write(f"**{stock_info['name']}**")
                st.write(f"현재가: {stock_info['current_price']:,}원")
                st.write(f"시가총액: {stock_info['market_cap']:,}원")
                st.write(f"PER: {stock_info['per']}")
                st.write(f"PBR: {stock_info['pbr']}")
                
                # 주가 차트
                history_df = get_stock_history(ticker)
                if history_df is not None:
                    df, analysis = calculate_technical_indicators(history_df)
                    
                    fig = go.Figure()
                    
                    # 캔들스틱 차트
                    fig.add_trace(go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name='OHLC'
                    ))
                    
                    # 이동평균선
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['MA5'],
                        name='MA5',
                        line=dict(color='blue', width=1)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['MA20'],
                        name='MA20',
                        line=dict(color='orange', width=1)
                    ))
                    
                    fig.update_layout(
                        title=f"{stock_info['name']} 주가 차트",
                        yaxis_title='주가',
                        xaxis_title='날짜',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 기술적 분석 결과
                    st.subheader("기술적 분석")
                    st.write(f"추세: {analysis['trend']}")
                    st.write(f"RSI: {analysis['rsi_status']}")
                    st.write(f"MACD: {analysis['macd_signal']}")
                
                # 최신 뉴스
                st.subheader("관련 뉴스")
                news = get_company_news(ticker)
                for article in news:
                    if 'error' not in article:
                        st.write(f"[{article['title']}]({article['link']})")
                        st.write(f"출처: {article['publisher']}")
                        st.write(f"게시일: {article['published']}")
                        st.write("---")
            else:
                st.error(stock_info['error'])

    # 메인 영역 - 챗봇
    st.subheader("AI 투자 상담")
    
    # 채팅 히스토리 표시
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("투자에 대해 무엇이든 물어보세요!"):
        # 사용자 메시지 추가
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답
        with st.chat_message("assistant"):
            response = get_investment_advice(prompt, st.session_state.chat_history[:-1])
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 
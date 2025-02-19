# 투자 조언 AI 챗봇

OpenAI API와 Streamlit을 활용한 투자 조언 AI 챗봇입니다. 사용자의 투자 관련 질문에 답변하고, 주식 분석 기능을 제공합니다.

## 주요 기능

1. **AI 투자 상담**
   - OpenAI API를 활용한 자연어 기반 투자 상담
   - 투자 전략, 시장 분석, 포트폴리오 조언 등 제공
   - 대화 기록 유지 및 문맥 이해

2. **주식 분석**
   - 실시간 주가 정보 조회
   - 캔들스틱 차트 및 기술적 지표 분석
   - 이동평균선, RSI, MACD 등 기술적 분석 제공
   - 기업 관련 최신 뉴스 제공

## 설치 방법

1. 저장소 클론
   ```bash
   git clone [저장소 URL]
   cd [프로젝트 디렉토리]
   ```

2. 가상환경 생성 및 활성화
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

4. 환경 변수 설정
   - `.env` 파일을 생성하고 다음 내용을 추가:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   ```

## 실행 방법

1. Streamlit 앱 실행
   ```bash
   streamlit run src/main.py
   ```

2. 웹 브라우저에서 접속
   - 기본적으로 `http://localhost:8501`에서 실행됩니다.

## 프로젝트 구조

```
.
├── config/
│   └── config.py         # 설정 파일
├── src/
│   ├── main.py          # 메인 Streamlit 앱
│   └── utils/
│       ├── openai_helper.py    # OpenAI API 관련 함수
│       └── finance_helper.py   # 금융 데이터 관련 함수
├── requirements.txt      # 필요한 패키지 목록
└── README.md            # 프로젝트 설명
```

## 사용된 기술

- **Frontend**: Streamlit
- **AI/ML**: OpenAI API (GPT-4)
- **데이터 수집**: Yahoo Finance API
- **데이터 시각화**: Plotly
- **기타 라이브러리**: pandas, python-dotenv

## 주의사항

- API 키는 절대로 코드에 직접 입력하지 마시고, 반드시 환경 변수를 통해 관리하세요.
- 본 프로젝트는 투자 참고용으로만 사용하시기 바랍니다.
- 실제 투자는 본인의 판단하에 신중하게 결정하시기 바랍니다.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 LICENSE 파일을 참조하세요. 
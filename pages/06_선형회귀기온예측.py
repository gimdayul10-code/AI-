import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 페이지 설정
st.set_page_config(page_title="월별 기온 예측 앱", layout="wide")

st.title("🌡️ 과거 기온 데이터 조회 및 선형회귀 기온 예측")
st.write("선택한 월의 과거 평균기온 데이터를 시각화하고, 선형회귀 모델을 통해 미래 기온을 예측합니다.")

# 데이터 불러오기 함수 (인코딩 대응 및 캐싱)
@st.cache_data
def load_data():
    encodings = ['cp949', 'euc-kr', 'utf-8-sig', 'utf-8']
    for enc in encodings:
        try:
            df = pd.read_csv('temperature.csv', encoding=enc)
            # '일시' 컬럼 분석 (예: Oct-07 형태 처리)
            df['일시_dt'] = pd.to_datetime(df['일시'], format='%b-%y', errors='coerce')
            
            # 연도 보정 (2000년대/1900년대 구분)
            def adjust_year(dt):
                if pd.isna(dt):
                    return dt
                if dt.year > 2026:
                    return dt.replace(year=dt.year - 100)
                return dt

            df['일시_dt'] = df['일시_dt'].apply(adjust_year)
            df['연도'] = df['일시_dt'].dt.year
            df['월'] = df['일시_dt'].dt.month
            return df
        except Exception:
            continue
    st.error("temperature.csv 파일을 불러올 수 없습니다. 파일 경로와 인코딩을 확인해주세요.")
    return None

df = load_data()

if df is not None:
    # 사이드바 사용자 입력
    st.sidebar.header("📊 조회 및 예측 조건 입력")
    
    selected_month = st.sidebar.selectbox("월 선택", list(range(1, 13)), index=0)
    
    max_year_in_data = int(df['연도'].max())
    predict_year = st.sidebar.number_input(
        "예측 연도 입력", 
        min_value=max_year_in_data + 1, 
        max_value=2100, 
        value=max_year_in_data + 5, 
        step=1
    )

    # 선택된 월 데이터 필터링
    month_df = df[df['월'] == selected_month].dropna(subset=['연도', '평균기온(℃)']).sort_values('연도')

    if len(month_df) > 0:
        # 선형회귀 모델 학습
        X = month_df[['연도']].values
        y = month_df['평균기온(℃)'].values

        model = LinearRegression()
        model.fit(X, y)

        # 예측 수행
        pred_temp = model.predict([[predict_year]])[0]
        slope = model.coef_[0]
        intercept = model.intercept_

        # 예측 결과 출력
        st.subheader(f"📌 {selected_month}월 기온 분석 결과")
        col1, col2, col3 = st.columns(3)
        col1.metric("데이터 보유 기간", f"{int(X.min())}년 ~ {int(X.max())}년")
        col2.metric(f"{predict_year}년 {selected_month}월 예측 평균기온", f"{pred_temp:.2f} ℃")
        col3.metric("연간 기온 변화 추세(기울기)", f"{slope:+.4f} ℃/년")

        # 시각화 (Matplotlib)
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # 1. 과거 데이터 점 및 선 그래프
        ax.plot(month_df['연도'], y, marker='o', color='skyblue', label=f'과거 {selected_month}월 평균기온')
        
        # 2. 선형 회귀선 (과거 ~ 예측 연도까지)
        x_range = np.arange(int(X.min()), predict_year + 1).reshape(-1, 1)
        y_range_pred = model.predict(x_range)
        ax.plot(x_range, y_range_pred, color='red', linestyle='--', label='선형회귀 추세선')
        
        # 3. 예측 지점 표시
        ax.scatter([predict_year], [pred_temp], color='crimson', s=150, zorder=5, label=f'{predict_year}년 예측값 ({pred_temp:.2f}℃)')
        ax.annotate(f'{predict_year}년\n({pred_temp:.2f}℃)', 
                    xy=(predict_year, pred_temp), 
                    xytext=(predict_year - 3, pred_temp + 1),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

        ax.set_title(f"[{selected_month}월] 연도별 평균기온 변화 및 {predict_year}년 예측", fontsize=14)
        ax.set_xlabel("연도 (Year)")
        ax.set_ylabel("평균기온 (℃)")
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()

        # 그래프 출력
        st.pyplot(fig)

        # -------------------------------------------------------------
        # 선형회귀 알고리즘 설명 섹션 (그래프 하단)
        # -------------------------------------------------------------
        st.markdown("---")
        st.subheader("💡 선형회귀(Linear Regression) 알고리즘이란?")
        
        st.markdown(f"""
        **선형회귀(Linear Regression)**는 관측된 데이터 점들 사이의 경향성을 가장 잘 나타내는 **직선(추세선)**을 찾는 통계적 머신러닝 알고리즘입니다.

        * **수식 모델**: $y = ax + b$
          * $x$ (**독립변수**): 연도
          * $y$ (**종속변수**): {selected_month}월 평균기온 (℃)
          * $a$ (**기울기**): 연도가 1년 지날 때 기온이 변하는 정도 (**현재 {selected_month}월 데이터 기준: `{slope:+.4f}℃/년`**)
          * $b$ (**Y절편**): 기준점 ($x=0$일 때의 Y값)

        * **원리 (최소제곱법, Ordinary Least Squares)**:
          실제 데이터 점들과 예측 직선 사이의 **오차(거리) 제곱의 합이 최소**가 되도록 직선의 기울기($a$)와 절편($b$)을 계산합니다.
        
        * **그래프 해석 방법**:
          * 파란색 선/점은 과거 실제 측정된 {selected_month}월의 평균기온입니다.
          * 빨간색 점선은 선형회귀 알고리즘이 산출한 기온 변화 추세선입니다.
          * 빨간색 강조 점은 이 추세선을 확장하여 **{predict_year}년 {selected_month}월의 기온을 예측한 결과**입니다.
        """)

    else:
        st.warning(f"선택하신 {selected_month}월에 해당하는 데이터가 존재하지 않습니다.")

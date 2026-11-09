```python
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# 1. 페이지 설정
# -------------------------
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

# -------------------------
# 2. 제목
# -------------------------
st.title("🌡️ 월별 기온분석")
st.subheader("원하는 월을 선택하고 연도별 기온 변화를 확인해 보세요!")
st.write("1907년부터 2025년까지의 월별 최고기온과 최저기온을 비교합니다.")

# -------------------------
# 3. CSV 파일 경로
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "temperature.csv"

# -------------------------
# 4. 데이터 불러오기
# -------------------------
@st.cache_data
def load_data(file_path):
    for encoding in ["cp949", "utf-8-sig", "euc-kr"]:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 인코딩을 확인해 주세요.")

if not CSV_FILE.exists():
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.stop()

df = load_data(str(CSV_FILE))

# -------------------------
# 5. 필요한 열 확인
# -------------------------
required_columns = [
    "일시",
    "최고기온(℃)",
    "최저기온(℃)"
]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해 주세요.")
    st.write(df.columns.tolist())
    st.stop()

# -------------------------
# 6. 날짜 데이터 처리
# -------------------------
# Oct-07 형식의 날짜 처리
date_text = df["일시"].astype(str).str.strip()

# 월과 두 자리 연도 추출
date_parts = date_text.str.extract(
    r"^([A-Za-z]{3})-(\d{2})$"
)

month_names = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

df["월"] = date_parts[0].str.title().map(month_names)

# 연도 보정
# 00~25는 2000~2025년
# 26~99는 1926~1999년으로 변환
# 단, 실제 1907~1925년 데이터는 별도 형식 확인 필요
two_digit_year = pd.to_numeric(
    date_parts[1],
    errors="coerce"
)

df["연도"] = two_digit_year.apply(
    lambda x: (
        2000 + int(x) if x <= 25
        else 1900 + int(x)
    ) if pd.notna(x) else None
)

# 기온 숫자 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"],
    errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"],
    errors="coerce"
)

# 날짜 오류 제거
df = df.dropna(subset=["연도", "월"])

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

# -------------------------
# 7. 월 선택
# -------------------------
st.divider()

st.subheader("📅 분석할 월 선택")

selected_month = st.selectbox(
    "원하는 월을 선택하세요.",
    options=list(range(1, 13)),
    format_func=lambda x: f"{x}월"
)

# -------------------------
# 8. 선택한 월 데이터 추출
# -------------------------
month_df = df[
    (df["월"] == selected_month) &
    (df["연도"] >= 1907) &
    (df["연도"] <= 2025)
].copy()

# 연도별 평균 계산
year_df = (
    month_df.groupby("연도", as_index=False)
    [["최고기온(℃)", "최저기온(℃)"]]
    .mean()
)

# 1907~2025년 전체 연도 생성
all_years = pd.DataFrame({
    "연도": range(1907, 2026)
})

# 없는 연도도 포함
year_df = all_years.merge(
    year_df,
    on="연도",
    how="left"
)

# -------------------------
# 9. 그래프 출력
# -------------------------
st.divider()

if year_df[["최고기온(℃)", "최저기온(℃)"]].notna().sum().sum() == 0:

    st.warning("선택한 월에 기온 데이터가 없습니다.")

else:

    graph_df = year_df.melt(
        id_vars=["연도"],
        value_vars=["최고기온(℃)", "최저기온(℃)"],
        var_name="기온 종류",
        value_name="온도"
    )

    color_map = {
        "최고기온(℃)": "#FF1493",
        "최저기온(℃)": "#1E90FF"
    }

    fig = px.line(
        graph_df,
        x="연도",
        y="온도",
        color="기온 종류",
        color_discrete_map=color_map,
        markers=True,
        title="월별 기온분석",
        labels={
            "연도": "연도",
            "온도": "온도(℃)",
            "기온 종류": "범례"
        }
    )

    fig.update_layout(
        title={
            "text": "월별 기온분석",
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="연도",
        yaxis_title="온도(℃)",
        legend_title="기온 구분",
        hovermode="x unified",
        template="plotly_white",
        xaxis=dict(
            range=[1907, 2025],
            tickmode="linear",
            tick0=1907,
            dtick=5
        )
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
        connectgaps=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # 10. 통계
    # -------------------------
    st.divider()
    st.subheader("📈 기온 통계")

    col1, col2 = st.columns(2)

    with col1:
        avg_max = year_df["최고기온(℃)"].mean()
        st.metric(
            "평균 최고기온",
            f"{avg_max:.1f}℃" if pd.notna(avg_max) else "-"
        )

    with col2:
        avg_min = year_df["최저기온(℃)"].mean()
        st.metric(
            "평균 최저기온",
            f"{avg_min:.1f}℃" if pd.notna(avg_min) else "-"
        )

    # -------------------------
    # 11. 데이터 표
    # -------------------------
    st.subheader("📋 연도별 기온 데이터")

    st.dataframe(
        year_df.round(1),
        use_container_width=True,
        hide_index=True
    )

# -------------------------
# 12. 하단 안내
# -------------------------
st.divider()

st.caption(
    "🌱 1907년~2025년 월별 기온 변화 분석 프로그램"
)
```

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
st.write("연도별 최고기온과 최저기온을 비교해 볼 수 있습니다.")

# -------------------------
# 3. CSV 파일 경로 설정
# -------------------------
# 현재 파일은 pages 폴더에 있고
# CSV 파일은 상위 폴더에 있음
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "temperature.csv"

# -------------------------
# 4. CSV 데이터 불러오기
# -------------------------
@st.cache_data
def load_data(file_path):

    for encoding in ["cp949", "utf-8-sig", "euc-kr"]:
        try:
            return pd.read_csv(
                file_path,
                encoding=encoding
            )
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일 인코딩을 확인해 주세요.")


# 파일 존재 확인
if not CSV_FILE.exists():
    st.error("❌ temperature.csv 파일을 찾을 수 없습니다.")
    st.write("CSV 파일을 프로젝트 상위 폴더에 업로드해 주세요.")
    st.stop()

# 데이터 불러오기
df = load_data(CSV_FILE)

# -------------------------
# 5. 데이터 열 확인
# -------------------------
required_columns = [
    "일시",
    "최고기온(℃)",
    "최저기온(℃)"
]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름이 올바르지 않습니다.")
    st.write("현재 열 이름:", df.columns.tolist())
    st.stop()

# -------------------------
# 6. 날짜 데이터 처리
# -------------------------
# 일시에서 연도와 월 추출
date_text = df["일시"].astype(str).str.strip()

df["연도"] = pd.to_numeric(
    date_text.str.extract(r"(\d{4})")[0],
    errors="coerce"
)

df["월"] = pd.to_numeric(
    date_text.str.extract(r"^\s*\d{4}\D+(\d{1,2})")[0],
    errors="coerce"
)

# 기온 데이터 숫자로 변환
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
    df["월"] == selected_month
].copy()

# 기온 결측치 제거
month_df = month_df.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

# 연도별 데이터 정리
year_df = (
    month_df.groupby("연도", as_index=False)
    [["최고기온(℃)", "최저기온(℃)"]]
    .mean()
    .sort_values("연도")
)

# -------------------------
# 9. 그래프 출력
# -------------------------
if year_df.empty:

    st.warning(
        f"{selected_month}월에 해당하는 데이터가 없습니다."
    )

else:

    st.success(
        f"📊 {selected_month}월 연도별 기온 분석 결과입니다!"
    )

    # 꺾은선 그래프를 위한 데이터 변환
    graph_df = year_df.melt(
        id_vars="연도",
        value_vars=[
            "최고기온(℃)",
            "최저기온(℃)"
        ],
        var_name="기온 종류",
        value_name="온도"
    )

    # 그래프 색상 설정
    color_map = {
        "최고기온(℃)": "#FF69B4",
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

    # 그래프 디자인
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
        template="plotly_white"
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    # 그래프 표시
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # 10. 기온 통계
    # -------------------------
    st.divider()

    st.subheader("📈 기온 통계")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "평균 최고기온",
            f"{year_df['최고기온(℃)'].mean():.1f}℃"
        )

    with col2:
        st.metric(
            "평균 최저기온",
            f"{year_df['최저기온(℃)'].mean():.1f}℃"
        )

    # -------------------------
    # 11. 연도별 데이터 표
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
    "🌱 월별 기온 데이터를 활용한 연도별 기온 변화 분석 프로그램"
)
```

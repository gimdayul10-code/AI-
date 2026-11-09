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
st.write("연도별 최고기온과 최저기온을 비교할 수 있습니다.")

# -------------------------
# 3. CSV 파일 경로 설정
# -------------------------
# 현재 파이썬 파일은 pages 폴더에 있음
# CSV 파일은 상위 폴더에 있음

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "temperature.csv"

# -------------------------
# 4. 데이터 불러오기
# -------------------------
@st.cache_data
def load_data(file_path):

    encodings = ["cp949", "utf-8-sig", "euc-kr"]

    for encoding in encodings:
        try:
            data = pd.read_csv(
                file_path,
                encoding=encoding
            )
            return data

        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일의 한글 인코딩을 확인해 주세요.")


# CSV 파일 존재 확인
if not CSV_FILE.exists():
    st.error("❌ temperature.csv 파일을 찾을 수 없습니다.")
    st.write("CSV 파일을 프로젝트 상위 폴더에 넣어 주세요.")
    st.stop()

# 데이터 불러오기
try:
    df = load_data(str(CSV_FILE))

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
    st.stop()


# -------------------------
# 5. 필요한 열 확인
# -------------------------
required_columns = [
    "일시",
    "최고기온(℃)",
    "최저기온(℃)"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error("CSV 파일의 열 이름이 올바르지 않습니다.")
    st.write("없는 열:", missing_columns)
    st.write("현재 열:", df.columns.tolist())
    st.stop()


# -------------------------
# 6. 날짜 데이터 처리
# -------------------------
# 실제 CSV 날짜 형식: Oct-07, Nov-07 등

df["날짜"] = pd.to_datetime(
    df["일시"].astype(str).str.strip(),
    format="%b-%y",
    errors="coerce"
)

# 연도 추출
df["연도"] = df["날짜"].dt.year

# 월 추출
df["월"] = df["날짜"].dt.month

# 기온 데이터 숫자로 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"],
    errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"],
    errors="coerce"
)

# 날짜가 잘못된 행 제거
df = df.dropna(
    subset=["연도", "월"]
)

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)


# -------------------------
# 7. 월 선택 기능
# -------------------------
st.divider()

st.subheader("📅 분석할 월 선택")

selected_month = st.selectbox(
    "원하는 월을 선택하세요.",
    options=list(range(1, 13)),
    format_func=lambda x: str(x) + "월"
)


# -------------------------
# 8. 선택한 월 데이터 추출
# -------------------------
month_df = df[
    df["월"] == selected_month
].copy()

# 최고기온과 최저기온이 모두 없는 행만 제거
month_df = month_df.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"],
    how="all"
)

# 연도별 기온 평균 계산
year_df = (
    month_df.groupby("연도", as_index=False)
    [["최고기온(℃)", "최저기온(℃)"]]
    .mean()
    .sort_values("연도")
)


# -------------------------
# 9. 그래프 출력
# -------------------------
st.divider()

if year_df.empty:

    st.warning(
        str(selected_month) + "월의 기온 데이터가 없습니다."
    )

else:

    st.success(
        "📊 " + str(selected_month) + "월 기온 분석 결과입니다!"
    )

    # 그래프 데이터 변환
    graph_df = year_df.melt(
        id_vars=["연도"],
        value_vars=[
            "최고기온(℃)",
            "최저기온(℃)"
        ],
        var_name="기온 종류",
        value_name="온도"
    )

    # 그래프 색상 설정
    color_map = {
        "최고기온(℃)": "#FF1493",
        "최저기온(℃)": "#1E90FF"
    }

    # 꺾은선 그래프
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

        template="plotly_white",

        font=dict(
            family="Malgun Gothic, sans-serif",
            size=13
        )
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

        avg_max = year_df["최고기온(℃)"].mean()

        st.metric(
            label="평균 최고기온",
            value=f"{avg_max:.1f}℃"
        )

    with col2:

        avg_min = year_df["최저기온(℃)"].mean()

        st.metric(
            label="평균 최저기온",
            value=f"{avg_min:.1f}℃"
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

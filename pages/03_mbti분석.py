
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# 1. 페이지 설정
# -------------------------
st.set_page_config(
    page_title="국가별 MBTI 비율",
    page_icon="🌍",
    layout="wide"
)

# -------------------------
# 2. 제목
# -------------------------
st.title("🌍 국가별 MBTI 비율 분석")
st.write(
    "원하는 국가를 선택하고 MBTI 16가지 유형의 "
    "비율을 확인해 보세요!"
)

# -------------------------
# 3. CSV 데이터 불러오기
# -------------------------
CSV_FILE = Path(__file__).parent / "countriesMBTI_16types.csv"

@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="cp949")

try:
    df = load_data(str(CSV_FILE))

except FileNotFoundError:
    st.error("❌ CSV 파일을 찾을 수 없습니다.")
    st.info(
        "countriesMBTI_16types.csv 파일을 "
        "app.py와 같은 폴더에 업로드해 주세요."
    )
    st.stop()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# -------------------------
# 4. 데이터 확인 및 정리
# -------------------------
if "Country" not in df.columns:
    st.error("CSV 파일에 Country 열이 없습니다.")
    st.stop()

mbti_types = [
    col for col in df.columns
    if col != "Country"
]

if len(mbti_types) != 16:
    st.error(
        f"MBTI 데이터 열이 16개가 아닙니다. "
        f"현재 {len(mbti_types)}개입니다."
    )
    st.stop()

df["Country"] = df["Country"].astype(str).str.strip()

for mbti in mbti_types:
    df[mbti] = pd.to_numeric(
        df[mbti], errors="coerce"
    )

df = df.dropna(subset=["Country"])
df = df.dropna(subset=mbti_types, how="all")

countries = sorted(
    df["Country"].unique().tolist()
)

if len(countries) == 0:
    st.error("표시할 국가 데이터가 없습니다.")
    st.stop()

# -------------------------
# 5. 국가 선택
# -------------------------
selected_country = st.selectbox(
    "🗺️ 국가를 선택하세요!",
    countries
)

# 선택한 국가 데이터
country_data = df[
    df["Country"] == selected_country
].iloc[0]

# -------------------------
# 6. 그래프 데이터 만들기
# -------------------------
chart_data = pd.DataFrame({
    "MBTI": mbti_types,
    "비율": [
        country_data[mbti] * 100
        for mbti in mbti_types
    ]
})

chart_data = chart_data.dropna(
    subset=["비율"]
)

if chart_data.empty:
    st.warning("선택한 국가의 데이터가 없습니다.")
    st.stop()

# 높은 비율부터 정렬
chart_data = chart_data.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)

# -------------------------
# 7. 그래프 색상 설정
# -------------------------
green_colors = [
    "#16834A",
    "#269653",
    "#3DAA64",
    "#55B875",
    "#70C58A",
    "#8BD19F",
    "#A6DDB4",
    "#BCE6C6",
    "#CDEDD4",
    "#D9F2DE",
    "#E3F5E8",
    "#EAF8ED",
    "#F0FAF2",
    "#F4FCF6",
    "#F7FDF8"
]

colors = (
    ["#E53935"]
    + green_colors[:len(chart_data) - 1]
)

# -------------------------
# 8. 최고 비율 정보
# -------------------------
top_mbti = chart_data.iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "선택 국가",
        selected_country
    )

with col2:
    st.metric(
        "가장 높은 MBTI",
        top_mbti["MBTI"]
    )

with col3:
    st.metric(
        "최고 비율",
        f'{top_mbti["비율"]:.2f}%'
    )

st.divider()

# -------------------------
# 9. 막대그래프
# -------------------------
st.subheader(
    f"📊 {selected_country}의 MBTI 비율"
)

fig = px.bar(
    chart_data,
    x="비율",
    y="MBTI",
    orientation="h",
    text=chart_data["비율"].map(
        lambda x: f"{x:.2f}%"
    )
)

fig.update_traces(
    marker_color=colors,
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "비율: %{x:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    yaxis=dict(
        title="MBTI 유형",
        autorange="reversed"
    ),
    xaxis=dict(
        title="비율 (%)",
        rangemode="tozero"
    ),
    showlegend=False,
    height=650,
    margin=dict(
        l=30,
        r=65,
        t=30,
        b=45
    ),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------
# 10. 상세 데이터 표
# -------------------------
with st.expander(
    "📋 MBTI 비율 자세히 보기"
):
    display_data = chart_data.copy()

    display_data["비율"] = display_data[
        "비율"
    ].map(lambda x: f"{x:.2f}%")

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

# -------------------------
# 11. 안내 문구
# -------------------------
st.caption(
    "※ 본 결과는 제공된 CSV 데이터에 기반한 통계입니다."
)


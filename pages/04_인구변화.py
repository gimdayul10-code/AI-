
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re

# --------------------------------
# 1. 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="성북구 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# 2. CSV 파일 경로
# --------------------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "population.csv"

# --------------------------------
# 3. 데이터 불러오기
# --------------------------------
@st.cache_data
def load_data():

    # 한글 인코딩 오류 방지
    encodings = ["cp949", "euc-kr", "utf-8-sig"]

    for encoding in encodings:
        try:
            df = pd.read_csv(
                CSV_FILE,
                encoding=encoding
            )
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("CSV 파일의 인코딩을 확인해주세요.")

    # 인구 데이터를 숫자로 변환
    for col in df.columns:
        if col != "행정구역":
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(
                    ",", "", regex=False
                ),
                errors="coerce"
            )

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("population(2).csv 파일을 찾을 수 없습니다.")
    st.stop()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# --------------------------------
# 4. 제목
# --------------------------------
st.title("📊 성북구 연령별 인구 분석")
st.write("행정구역과 성별, 연도를 선택하여 연령별 인구 분포를 확인해보세요!")

st.divider()


# --------------------------------
# 5. 선택 항목 구성
# --------------------------------

# 행정구역 목록
regions = df["행정구역"].dropna().tolist()

# 연도 목록 추출
years = sorted(
    set(
        re.findall(r"(\d{4})년_", " ".join(df.columns))
    )
)

# 성별 목록
genders = ["계", "남", "여"]

# 선택창을 3개 열로 배치
col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox(
        "🏠 행정구역 선택",
        regions
    )

with col2:
    selected_gender = st.selectbox(
        "👤 성별 선택",
        genders
    )

with col3:
    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=len(years) - 1
    )

st.divider()


# --------------------------------
# 6. 선택한 데이터 추출
# --------------------------------

# 선택한 행정구역 데이터
region_data = df[
    df["행정구역"] == selected_region
]

if region_data.empty:
    st.error("선택한 행정구역의 데이터가 없습니다.")
    st.stop()

# 선택한 연도와 성별에 해당하는 열 찾기
prefix = f"{selected_year}년_{selected_gender}_"

age_columns = [
    col for col in df.columns
    if col.startswith(prefix)
    and re.search(
        r"_(\d+~\d+세|\d+세 이상)$",
        col
    )
]

if not age_columns:
    st.error("선택한 조건에 해당하는 연령별 데이터가 없습니다.")
    st.stop()

# 연령 순서대로 정렬
def age_sort_key(column):
    age = column.replace(prefix, "")
    return int(re.match(r"\d+", age).group())

age_columns = sorted(
    age_columns,
    key=age_sort_key
)

# 연령대 이름
ages = [
    col.replace(prefix, "")
    for col in age_columns
]

# 인구수
population = (
    region_data.iloc[0][age_columns]
    .fillna(0)
    .tolist()
)


# --------------------------------
# 7. 꺾은선 그래프
# --------------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ages,
        y=population,
        mode="lines+markers",
        name="인구수",
        line=dict(
            color="#FF1493",
            width=3
        ),
        marker=dict(
            color="#FF1493",
            size=8
        ),
        hovertemplate=
        "<b>%{x}</b><br>" +
        "인구수: %{y:,.0f}명" +
        "<extra></extra>"
    )
)

# 그래프 디자인
fig.update_layout(
    title=dict(
        text=f"{selected_region} {selected_year}년 {selected_gender} 연령별 인구",
        x=0.5,
        font=dict(size=20)
    ),

    xaxis=dict(
        title="나이",
        type="category",
        categoryorder="array",
        categoryarray=ages,
        tickmode="array",
        tickvals=ages,
        ticktext=ages,
        showgrid=True,
        gridcolor="#F5C6D9",
        gridwidth=1
    ),

    yaxis=dict(
        title="인구수 (명)",
        rangemode="tozero",
        dtick=100,
        tickformat=",",
        showgrid=True,
        gridcolor="#E5E5E5",
        gridwidth=1
    ),

    plot_bgcolor="white",
    paper_bgcolor="white",

    font=dict(
        family="Malgun Gothic, AppleGothic, sans-serif",
        size=13,
        color="#333333"
    ),

    hovermode="x unified",
    height=550,

    margin=dict(
        l=50,
        r=30,
        t=80,
        b=80
    )
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------
# 8. 선택한 데이터 요약
# --------------------------------

st.subheader("📌 인구 데이터 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "행정구역",
        selected_region.split("(")[0]
    )

with col2:
    st.metric(
        "선택한 연도",
        f"{selected_year}년"
    )

with col3:
    st.metric(
        "전체 연령대 인구",
        f"{sum(population):,.0f}명"
    )


# --------------------------------
# 9. 연령별 데이터 표
# --------------------------------

with st.expander("📋 연령별 인구 데이터 확인하기"):
    result_df = pd.DataFrame({
        "연령대": ages,
        "인구수": population
    })

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

st.caption("※ 제공된 CSV 파일의 인구 통계를 바탕으로 작성한 그래프입니다.")

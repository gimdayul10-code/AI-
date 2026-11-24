import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="맞춤형 영양성분 & 음식 추천기",
    page_icon="🥗",
    layout="wide"
)

# 2. 데이터 로드 및 전처리 (한글 깨짐 방지: cp949)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Nutritional Information.csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("Nutritional Information.csv", encoding="utf-8-sig")
    
    # 필요한 컬럼만 추출 및 결측치 처리
    cols = ['식품명', '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)', '영양성분함량기준량']
    df = df[cols].dropna(subset=['식품명', '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)']).copy()
    
    # 디저트 키워드 분류 (식사 vs 디저트)
    dessert_keywords = [
        '케이크', '빵', '쿠키', '초콜릿', '쇼콜라', '아이스크림', '과자', '스낵', 
        '젤리', '사탕', '캔디', '파이', '타르트', '마카롱', '푸딩', '도넛', 
        '와플', '비스킷', '떡', '약과', '한과', '양갱', '카라멜', '캬라멜', 
        '쉐이크', '스무디', '라떼', '주스', '음료', '티', '에이드', '요거트'
    ]
    pattern = '|'.join(dessert_keywords)
    df['카테고리'] = df['식품명'].apply(
        lambda x: '디저트' if pd.Series(x).str.contains(pattern, case=False, na=False).iloc[0] else '식사'
    )
    return df

# 3. 음식 이름에 맞는 귀여운 이모티콘 매핑 함수
def get_food_emoji(food_name):
    emoji_map = {
        '케이크': '🍰', '쇼콜라': '🍫', '초콜릿': '🍫', '쿠키': '🍪', '비스킷': '🍪',
        '빵': '🍞', '식빵': '🍞', '샌드위치': '🥪', '도넛': '🍩', '와플': '🧇',
        '파이': '🥧', '타르트': '🥧', '아이스크림': '🍨', '떡': '🍡', '꿀떡': '🍡',
        '밥': '🍚', '도시락': '🍱', '김밥': '🍙', '죽': '🥣', '스프': '🥣',
        '국': '🍲', '탕': '🍲', '찌개': '🥘', '육개장': '🥘', '볶음': '🍳',
        '면': '🍜', '국수': '🍜', '라면': '🍜', '짬뽕': '🍜', '떡볶이': '🌶️',
        '만두': '🥟', '닭': '🍗', '치킨': '🍗', '고기': '🥩', '불고기': '🥩',
        '갈비': '🍖', '생선': '🐟', '고등어': '🐟', '새우': '🍤', '샐러드': '🥗',
        '과일': '🍎', '딸기': '🍓', '망고': '🥭', '감자': '🥔', '고구마': '🍠',
        '우유': '🥛', '치즈': '🧀', '커피': '☕', '라떼': '☕', '티': '🍵', '차': '🍵',
        '주스': '🧃', '음료': '🥤', '콜라겐': '✨', '캔디': '🍬', '사탕': '🍬', '젤리': '🍮'
    }
    for key, emoji in emoji_map.items():
        if key in str(food_name):
            return emoji
    return '🍽️'  # 기본 이모티콘

# 데이터 불러오기
df = load_data()

# 4. 메인 제목
st.title("🥗 내 입맛대로 찾는 맞춤형 영양성분 음식 추천기")
st.markdown("원하는 영양성분 탭을 선택한 후, **목표 수치**와 **식사/디저트**를 골라보세요!")

# 5. 제목 바로 아래 4개 페이지(탭) 생성
tab1, tab2, tab3, tab4 = st.tabs([
    "🔥 칼로리 페이지", 
    "🍚 탄수화물 페이지", 
    "🥩 단백질 페이지", 
    "🥑 지방 페이지"
])

# 6. 각 페이지별 공통 UI 및 분석 로직 함수
def render_nutrient_page(tab_key, nutrient_col, unit, label_text, default_val, chart_title):
    st.subheader(f"✨ {label_text} 기준 맞춤형 음식 찾기")
    
    # 입력칸(왼쪽)과 선택지(오른쪽) 배치
    col1, col2 = st.columns([1, 1])
    with col1:
        max_val = st.number_input(
            f"원하는 최대 {label_text}({unit})을 입력하세요 (이하 검색)",
            min_value=0.0,
            max_value=2000.0,
            value=float(default_val),
            step=10.0,
            key=f"input_{tab_key}"
        )
    with col2:
        category_choice = st.radio(
            "음식 종류를 선택하세요",
            options=["식사", "디저트"],
            horizontal=True,
            key=f"radio_{tab_key}"
        )
    
    # 조건 필터링 (사용자 입력값 이하 & 카테고리 일치)
    filtered_df = df[
        (df[nutrient_col] <= max_val) & 
        (df['카테고리'] == category_choice)
    ].copy()
    
    # 해당 영양성분이 0인 단순 물/차 등을 제외하고 유의미한 음식 상위 정렬
    filtered_df = filtered_df[filtered_df[nutrient_col] > 0].sort_values(
        by=nutrient_col, ascending=False
    )
    
    st.divider()
    
    if filtered_df.empty:
        st.warning(f"😅 입력하신 {max_val}{unit} 이하의 '{category_choice}' 음식을 찾지 못했어요. 수치를 조금 높여보세요!")
        return
    
    st.success(f"🎉 조건에 맞는 **{category_choice}** 음식 총 **{len(filtered_df):,}개**를 찾았습니다! (상위 15개 표시)")
    
    # 상위 15개 추출 및 귀여운 이모티콘 결합
    top_df = filtered_df.head(15).copy()
    top_df['음식명 (추천)'] = top_df['식품명'].apply(lambda name: f"{get_food_emoji(name)} {name}")
    
    # 화면 구성: 왼쪽(음식 및 탄단지 표), 오른쪽(그래프)
    left_col, right_col = st.columns([1.2, 1])
    
    with left_col:
        st.markdown("#### 📋 추천 음식 및 탄·단·지 영양성분")
        display_df = top_df[[
            '음식명 (추천)', '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)', '영양성분함량기준량'
        ]].rename(columns={
            '에너지(kcal)': '칼로리(kcal)',
            '탄수화물(g)': '탄수화물(g)',
            '단백질(g)': '단백질(g)',
            '지방(g)': '지방(g)',
            '영양성분함량기준량': '기준량'
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    with right_col:
        st.markdown(f"#### 📊 {chart_title}")
        chart_df = top_df.head(10).copy()
        # 그래프 라벨이 너무 길지 않게 축약
        chart_df['짧은이름'] = chart_df['음식명 (추천)'].apply(lambda x: x[:16] + '..' if len(x) > 16 else x)
        
        fig = px.bar(
            chart_df,
            x=['탄수화물(g)', '단백질(g)', '지방(g)'],
            y='짧은이름',
            orientation='h',
            title=chart_title,
            labels={'value': '함량 (g)', '짧은이름': '음식명', 'variable': '영양성분'},
            color_discrete_map={
                '탄수화물(g)': '#FFB347',
                '단백질(g)': '#FF6961',
                '지방(g)': '#77DD77'
            },
            barmode='group'
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=50, b=10),
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

# 7. 4개 탭 각각 렌더링
with tab1:
    render_nutrient_page(
        tab_key="cal",
        nutrient_col="에너지(kcal)",
        unit="kcal",
        label_text="칼로리",
        default_val=300,
        chart_title="🔥 가볍고 맛있게! 칼로리 맞춤 음식 탄·단·지 밸런스"
    )

with tab2:
    render_nutrient_page(
        tab_key="carb",
        nutrient_col="탄수화물(g)",
        unit="g",
        label_text="탄수화물",
        default_val=30,
        chart_title="🍚 든든한 에너지원! 탄수화물 맞춤 음식 영양 비교"
    )

with tab3:
    render_nutrient_page(
        tab_key="prot",
        nutrient_col="단백질(g)",
        unit="g",
        label_text="단백질",
        default_val=25,
        chart_title="🥩 득근을 위한 선택! 단백질 맞춤 음식 영양 구성"
    )

with tab4:
    render_nutrient_page(
        tab_key="fat",
        nutrient_col="지방(g)",
        unit="g",
        label_text="지방",
        default_val=15,
        chart_title="🥑 건강한 지방 섭취! 지방 맞춤 음식 영양 분포"
    )

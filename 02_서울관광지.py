
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

# 페이지 설정
st.set_page_config(
    page_title="서울 외국인 관광 명소 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 관광지 데이터
places = [
    {
        "rank": 1,
        "name": "명동",
        "english": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9850,
        "area": "중구",
        "description": "화장품, 패션 매장과 길거리 음식이 모여 있는 대표적인 쇼핑 거리입니다.",
        "keyword": "쇼핑 · 길거리 음식"
    },
    {
        "rank": 2,
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "area": "마포구",
        "description": "개성 있는 카페와 맛집, 버스킹, 패션 매장 등을 즐길 수 있는 젊고 활기찬 거리입니다.",
        "keyword": "K-팝 · 문화 · 카페"
    },
    {
        "rank": 3,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "area": "종로구",
        "description": "조선 왕조의 대표 궁궐입니다. 전통 건축물과 한복 체험을 통해 한국의 역사를 경험할 수 있습니다.",
        "keyword": "한국 역사 · 한복 체험"
    },
    {
        "rank": 4,
        "name": "성수동",
        "english": "Seongsu-dong",
        "lat": 37.5445,
        "lon": 127.0560,
        "area": "성동구",
        "description": "옛 공장을 개조한 감각적인 카페와 편집숍, 팝업스토어가 많습니다.",
        "keyword": "팝업스토어 · 카페"
    },
    {
        "rank": 5,
        "name": "강남역 일대",
        "english": "Gangnam",
        "lat": 37.4979,
        "lon": 127.0276,
        "area": "강남구",
        "description": "대형 쇼핑 매장과 음식점, 문화 공간이 모여 있는 번화가입니다.",
        "keyword": "쇼핑 · 도심 문화"
    },
    {
        "rank": 6,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "area": "용산구",
        "description": "남산 정상에 있는 서울의 대표 전망 명소로 서울 도심의 풍경을 감상할 수 있습니다.",
        "keyword": "전망 · 야경"
    },
    {
        "rank": 7,
        "name": "코엑스",
        "english": "COEX",
        "lat": 37.5125,
        "lon": 127.0588,
        "area": "강남구",
        "description": "별마당도서관과 다양한 쇼핑 공간, 전시 및 행사를 즐길 수 있습니다.",
        "keyword": "별마당도서관 · 쇼핑"
    },
    {
        "rank": 8,
        "name": "동대문디자인플라자",
        "english": "DDP",
        "lat": 37.5671,
        "lon": 127.0095,
        "area": "중구",
        "description": "독특한 곡선 형태의 건축물로 유명하며 디자인 전시와 패션 행사를 즐길 수 있습니다.",
        "keyword": "건축 · 디자인 · 전시"
    },
    {
        "rank": 9,
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9997,
        "area": "종로구",
        "description": "빈대떡, 마약김밥 등 한국의 다양한 시장 음식을 맛볼 수 있는 전통시장입니다.",
        "keyword": "전통시장 · 한국 음식"
    },
    {
        "rank": 10,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "area": "종로구",
        "description": "전통 한옥이 모여 있는 아름다운 마을로 한국의 전통 주거문화를 살펴볼 수 있습니다.",
        "keyword": "전통문화 · 한옥"
    }
]

# 제목
st.title("🗺️ 서울 외국인 관광 명소 TOP 10")
st.subheader("외국인 관광객에게 인기 있는 서울의 대표 명소를 찾아보세요!")

st.info(
    "2025년 외래관광객 선호 장소 조사와 "
    "서울시 외국인 방문객 분석을 참고한 추천 목록입니다. "
    "공식 단일 순위는 아닙니다."
)

# 지역 선택
areas = ["전체 지역"] + sorted(
    {p["area"] for p in places}
)

selected_area = st.selectbox(
    "📍 지역별 관광지 보기",
    areas
)

# 선택한 지역에 맞는 관광지만 표시
if selected_area == "전체 지역":
    visible_places = places
else:
    visible_places = [
        p for p in places
        if p["area"] == selected_area
    ]

# 서울 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# 전체 화면 버튼
Fullscreen(position="topright").add_to(m)

# 지도에 관광지 마커 표시
for p in visible_places:

    popup_html = f"""
    <div style="font-family: sans-serif; width: 220px;">
        <h4>{p['rank']}. {p['name']}</h4>
        <p>{p['english']} · {p['area']}</p>
        <p>{p['description']}</p>
    </div>
    """

    # 숫자 모양 마커
    icon_html = f"""
    <div style="
        background: #e84b75;
        color: white;
        border: 2px solid white;
        border-radius: 50%;
        width: 31px;
        height: 31px;
        line-height: 27px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 1px 5px rgba(0,0,0,.35);
    ">
        {p['rank']}
    </div>
    """

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"{p['rank']}. {p['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=280
        ),
        icon=folium.DivIcon(
            html=icon_html,
            icon_size=(31, 31),
            icon_anchor=(15, 15)
        )
    ).add_to(m)

# 지도 출력
st.subheader("📌 서울 관광지 지도")

st_folium(
    m,
    use_container_width=True,
    height=570,
    returned_objects=[]
)

# 구분선
st.divider()

# 관광지 설명
st.subheader("✨ 관광지 한눈에 보기")

st.write(
    "관광지 이름을 누르면 간단한 설명을 확인할 수 있어요!"
)

# 관광지별 설명 표시
for p in visible_places:

    with st.expander(
        f"{p['rank']}. {p['name']} | {p['keyword']}"
    ):

        st.markdown(
            f"**영문명:** {p['english']}"
        )

        st.markdown(
            f"**위치:** {p['area']}"
        )

        st.write(p["description"])

        map_url = (
            "https://www.google.com/maps/search/"
            f"?api=1&query={p['lat']},{p['lon']}"
        )

        st.markdown(
            f"[Google 지도에서 위치 보기]({map_url})"
        )

# 하단 안내
st.divider()

st.caption(
    "서울 외국인 관광 명소 TOP 10 | "
    "지도 데이터: OpenStreetMap"
)

st.markdown(
    "[서울시 외국인 관광객 분석]"
    "(https://english.seoul.go.kr/from-k-culture-to-k-hiking-foreign-tourists-venture-beyond-seouls-top-attractions/)"
)

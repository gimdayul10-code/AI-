import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광 명소 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 관광지 데이터
places = [
    {"rank": 1, "name": "명동", "en": "Myeongdong",
     "lat": 37.5636, "lon": 126.9850, "area": "중구",
     "keyword": "쇼핑 · 길거리 음식",
     "desc": "화장품, 패션 매장과 길거리 음식이 모여 있는 대표적인 쇼핑 거리입니다."},

    {"rank": 2, "name": "홍대 거리", "en": "Hongdae",
     "lat": 37.5563, "lon": 126.9236, "area": "마포구",
     "keyword": "K-팝 · 문화 · 카페",
     "desc": "카페와 맛집, 버스킹, 패션 매장 등을 즐길 수 있는 활기찬 거리입니다."},

    {"rank": 3, "name": "경복궁", "en": "Gyeongbokgung Palace",
     "lat": 37.5796, "lon": 126.9770, "area": "종로구",
     "keyword": "한국 역사 · 한복 체험",
     "desc": "조선 왕조의 대표 궁궐로 한국의 역사와 전통 건축물을 경험할 수 있습니다."},

    {"rank": 4, "name": "성수동", "en": "Seongsu-dong",
     "lat": 37.5445, "lon": 127.0560, "area": "성동구",
     "keyword": "팝업스토어 · 카페",
     "desc": "감각적인 카페와 편집숍, 팝업스토어가 많은 트렌디한 거리입니다."},

    {"rank": 5, "name": "강남역", "en": "Gangnam",
     "lat": 37.4979, "lon": 127.0276, "area": "강남구",
     "keyword": "쇼핑 · 도심 문화",
     "desc": "쇼핑 매장과 음식점, 문화 공간이 모여 있는 번화가입니다."},

    {"rank": 6, "name": "N서울타워", "en": "N Seoul Tower",
     "lat": 37.5512, "lon": 126.9882, "area": "용산구",
     "keyword": "전망 · 야경",
     "desc": "남산 정상에서 서울 도심의 아름다운 풍경을 감상할 수 있습니다."},

    {"rank": 7, "name": "코엑스", "en": "COEX",
     "lat": 37.5125, "lon": 127.0588, "area": "강남구",
     "keyword": "별마당도서관 · 쇼핑",
     "desc": "별마당도서관과 다양한 쇼핑 공간, 전시 행사를 즐길 수 있습니다."},

    {"rank": 8, "name": "동대문디자인플라자", "en": "DDP",
     "lat": 37.5671, "lon": 127.0095, "area": "중구",
     "keyword": "건축 · 디자인 · 전시",
     "desc": "독특한 곡선 형태의 건축물로 디자인 전시와 패션 행사가 열립니다."},

    {"rank": 9, "name": "광장시장", "en": "Gwangjang Market",
     "lat": 37.5700, "lon": 126.9997, "area": "종로구",
     "keyword": "전통시장 · 한국 음식",
     "desc": "빈대떡과 다양한 한국 시장 음식을 맛볼 수 있는 전통시장입니다."},

    {"rank": 10, "name": "북촌한옥마을", "en": "Bukchon Hanok Village",
     "lat": 37.5826, "lon": 126.9830, "area": "종로구",
     "keyword": "전통문화 · 한옥",
     "desc": "전통 한옥이 모여 있어 한국의 전통 주거문화를 살펴볼 수 있습니다."}
]

# 제목
st.title("🗺️ 서울 외국인 관광 명소 TOP 10")
st.subheader("외국인 관광객에게 인기 있는 서울의 대표 관광지를 찾아보세요!")

st.info(
    "서울의 대표 관광지를 소개하는 추천 목록입니다. "
    "공식 단일 순위가 아닌 여러 관광 정보를 참고한 목록입니다."
)

# 지역 선택
areas = ["전체 지역"] + sorted(
    set(p["area"] for p in places)
)

selected_area = st.selectbox(
    "📍 지역 선택",
    areas
)

if selected_area == "전체 지역":
    visible_places = places
else:
    visible_places = [
        p for p in places
        if p["area"] == selected_area
    ]

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 관광지 마커 표시
for p in visible_places:

    popup_text = (
        f"<b>{p['rank']}. {p['name']}</b><br>"
        f"{p['en']}<br>"
        f"{p['desc']}"
    )

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"{p['rank']}. {p['name']}",
        popup=folium.Popup(
            popup_text,
            max_width=300
        ),
        icon=folium.DivIcon(
            html=(
                '<div style="background:#e84b75;'
                'color:white;border:2px solid white;'
                'border-radius:50%;width:32px;height:32px;'
                'line-height:28px;text-align:center;'
                'font-weight:bold;">'
                f'{p["rank"]}'
                '</div>'
            ),
            icon_size=(32, 32),
            icon_anchor=(16, 16)
        )
    ).add_to(m)

# 지도 출력
st.subheader("📌 서울 관광지 지도")

st_folium(
    m,
    width=None,
    height=550,
    use_container_width=True
)

st.divider()

# 관광지 설명
st.subheader("✨ 관광지 소개")

for p in visible_places:

    with st.expander(
        f"{p['rank']}. {p['name']} - {p['keyword']}"
    ):

        st.write("영문명:", p["en"])
        st.write("위치:", p["area"])
        st.write(p["desc"])

        url = (
            "https://www.google.com/maps/search/"
            f"?api=1&query={p['lat']},{p['lon']}"
        )

        st.markdown(
            f"[Google 지도에서 위치 보기]({url})"
        )

st.divider()

st.caption(
    "서울 외국인 관광 명소 TOP 10 | "
    "지도 데이터: OpenStreetMap"
)

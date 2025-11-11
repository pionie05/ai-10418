import streamlit as st
from streamlit_folium import st_folium
import folium
import math

st.set_page_config(page_title="서울 관광지 여행 일정", layout="wide")

st.title("🇰🇷 외국인이 사랑하는 서울 명소 Top10 여행 지도")
st.markdown("서울의 주요 관광 명소 10곳을 지도에서 확인하고, 여행 일정을 자동으로 만들어보세요!")

# 서울 중심 좌표
seoul_center = (37.5665, 126.9780)
m = folium.Map(location=seoul_center, zoom_start=12)

# 관광지 데이터 (한국어 설명 + 가까운 전철역)
places = [
    {"name": "경복궁", "coords": (37.579617, 126.977041),
     "desc": "조선시대의 법궁으로 웅장한 건축미와 근정전이 아름다운 서울의 대표 명소입니다.",
     "station": "3호선 경복궁역"},
    {"name": "창덕궁", "coords": (37.579292, 126.991051),
     "desc": "비원(후원)으로 유명한 궁궐로, 자연과 조화를 이룬 정원이 아름답습니다.",
     "station": "3호선 안국역"},
    {"name": "북촌한옥마을", "coords": (37.582552, 126.983139),
     "desc": "전통 한옥과 좁은 골목길이 조화를 이루는 고즈넉한 마을입니다.",
     "station": "3호선 안국역"},
    {"name": "남산서울타워", "coords": (37.551169, 126.988227),
     "desc": "서울의 전경을 한눈에 볼 수 있는 랜드마크이자 야경 명소입니다.",
     "station": "4호선 명동역"},
    {"name": "명동", "coords": (37.563845, 126.986055),
     "desc": "쇼핑과 길거리 음식으로 가득한 서울의 대표적인 번화가입니다.",
     "station": "4호선 명동역"},
    {"name": "홍대거리", "coords": (37.556264, 126.923247),
     "desc": "젊음과 예술의 거리로, 라이브 공연과 개성 있는 카페가 가득합니다.",
     "station": "2호선 홍대입구역"},
    {"name": "인사동", "coords": (37.574362, 126.984847),
     "desc": "전통 공예품과 찻집, 갤러리로 유명한 한국 전통문화 거리입니다.",
     "station": "3호선 안국역"},
    {"name": "동대문디자인플라자(DDP)", "coords": (37.566295, 127.009377),
     "desc": "미래적인 건축물과 전시가 열리는 서울의 디자인 중심지입니다.",
     "station": "2호선 동대문역사문화공원역"},
    {"name": "청계천", "coords": (37.570028, 126.977829),
     "desc": "도심 속을 흐르는 하천으로 산책과 야경 감상에 좋습니다.",
     "station": "5호선 광화문역"},
    {"name": "롯데월드타워", "coords": (37.513081, 127.102513),
     "desc": "초고층 전망대와 쇼핑몰, 석촌호수가 어우러진 복합 명소입니다.",
     "station": "2호선 잠실역"},
]

# 빨간 마커로 지도 표시
for p in places:
    popup_html = f"""
    <b>{p['name']}</b><br>
    🚇 {p['station']}<br>
    {p['desc']}
    """
    folium.Marker(
        location=p["coords"],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=p["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# 지도 표시 (크기 60%)
st.subheader("🗺️ 서울 관광지도")
st_data = st_folium(m, width=660, height=360)

# 관광지 간단 설명 리스트
st.markdown("---")
st.subheader("📍 관광지 간단 안내")

cols = st.columns(2)
half = len(places) // 2
for i, col in enumerate(cols):
    with col:
        subset = places[:half] if i == 0 else places[half:]
        for p in subset:
            st.markdown(f"**{p['name']}**  \n🚇 {p['station']}  \n{p['desc']}")

# 일정 생성 기능
st.markdown("---")
st.subheader("🗓️ 나만의 서울 여행 일정 만들기")

days = st.radio("여행 기간을 선택하세요:", [1, 2, 3], horizontal=True)
st.write(f"👉 {days}일 동안 여행할 수 있는 일정표를 만들어드릴게요.")

places_per_day = math.ceil(len(places) / days)
schedule = [places[i:i+places_per_day] for i in range(0, len(places), places_per_day)]

for d, day_places in enumerate(schedule, start=1):
    if d > days:
        break
    with st.expander(f"📅 Day {d} 일정 보기"):
        for p in day_places:
            st.markdown(f"- **{p['name']}** (🚇 {p['station']}) — {p['desc']}")

st.success("💡 일정은 단순한 예시입니다. 실제 동선은 교통시간을 고려해 조정하세요!")

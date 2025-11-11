import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="서울 관광지 Top10 (Folium)", layout="wide")

st.title("🇰🇷 외국인이 좋아하는 서울 관광지 Top 10")
st.markdown("**지도에서 마커를 클릭하면 간단한 설명과 링크를 볼 수 있습니다.**")

# 지도 중심 좌표
seoul_center = (37.5665, 126.9780)
m = folium.Map(location=seoul_center, zoom_start=12)

# 관광지 데이터
places = [
    {"name": "Gyeongbokgung Palace (경복궁)", "coords": (37.579617, 126.977041),
     "desc": "조선 시대의 대표 궁궐. 한복 입고 사진 찍기 좋아요.",
     "link": "https://english.visitseoul.net/attractions/Gyeongbokgung-Palace_/77"},
    {"name": "Changdeokgung Palace (창덕궁)", "coords": (37.579292, 126.991051),
     "desc": "후원이 아름다운 유네스코 세계유산 궁궐.",
     "link": "https://english.visitseoul.net/attractions/Changdeokgung-Palace_/78"},
    {"name": "Bukchon Hanok Village (북촌한옥마을)", "coords": (37.582552, 126.983139),
     "desc": "전통 한옥과 골목길이 매력적인 사진 명소.",
     "link": "https://english.visitseoul.net/attractions/Bukchon-Hanok-Village_/80"},
    {"name": "N Seoul Tower (남산서울타워)", "coords": (37.551169, 126.988227),
     "desc": "서울을 한눈에 볼 수 있는 전망 명소.",
     "link": "https://english.visitseoul.net/attractions/N-Seoul-Tower_/86"},
    {"name": "Myeongdong (명동)", "coords": (37.563845, 126.986055),
     "desc": "쇼핑과 길거리음식의 중심가.",
     "link": "https://english.visitseoul.net/shopping/Myeongdong_/100"},
    {"name": "Hongdae (홍대)", "coords": (37.556264, 126.923247),
     "desc": "젊음의 거리, 자유로운 분위기와 공연의 거리.",
     "link": "https://english.visitseoul.net/attractions/Hongdae_/574"},
    {"name": "Insadong (인사동)", "coords": (37.574362, 126.984847),
     "desc": "전통 공예품과 찻집이 가득한 거리.",
     "link": "https://english.visitseoul.net/shopping/Insadong_/101"},
    {"name": "Dongdaemun Design Plaza (DDP)", "coords": (37.566295, 127.009377),
     "desc": "야경이 아름다운 서울의 디자인 랜드마크.",
     "link": "https://english.visitseoul.net/attractions/Dongdaemun-Design-Plaza-DDP_/1803"},
    {"name": "Cheonggyecheon Stream (청계천)", "coords": (37.570028, 126.977829),
     "desc": "도심 속 산책로, 야경이 특히 예쁜 장소.",
     "link": "https://english.visitseoul.net/nature/Cheonggyecheon_/2635"},
    {"name": "Lotte World Tower (롯데월드타워)", "coords": (37.513081, 127.102513),
     "desc": "초고층 전망대와 석촌호수 산책로로 유명.",
     "link": "https://english.visitseoul.net/attractions/Lotte-World-Tower_/2742"},
]

# 빨간색 마커로 지도에 표시
for p in places:
    popup_html = f"""
    <h4>{p['name']}</h4>
    <p>{p['desc']}</p>
    <a href="{p['link']}" target="_blank">🔗 자세히 보기</a>
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

# 지도 하단에 관광지 요약 리스트
st.markdown("---")
st.subheader("📍 관광지 간단 설명")

cols = st.columns(2)
half = len(places) // 2

# 왼쪽 / 오른쪽 두 칸에 나눠서 출력
with cols[0]:
    for p in places[:half]:
        st.markdown(f"**{p['name']}** — {p['desc']}")

with cols[1]:
    for p in places[half:]:
        st.markdown(f"**{p['name']}** — {p['desc']}")

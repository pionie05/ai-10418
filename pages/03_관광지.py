# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="서울 관광지 Top10 (Folium)", layout="wide")

st.title("🇰🇷 서울 주요관광지 Top 10 — Folium 지도")
st.markdown("사이드바에서 항목을 선택하면 지도에 마커가 표시됩니다. 마커를 클릭하면 간단한 설명과 링크가 뜹니다.")

# 기본 위치: 서울 중심
seoul_center = (37.5665, 126.9780)
m = folium.Map(location=seoul_center, zoom_start=12)

# 관광지 데이터: 이름, 좌표, 간단설명, 링크
places = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "coords": (37.579617, 126.977041),
        "desc": "조선 시대의 대표 궁궐. 한복 대여해서 사진 찍기 좋아요.",
        "link": "https://english.visitseoul.net/attractions/Gyeongbokgung-Palace_/77"
    },
    {
        "name": "Changdeokgung Palace (창덕궁)",
        "coords": (37.579292, 126.991051),
        "desc": "후원이 유명한 유네스코 세계유산 궁궐.",
        "link": "https://english.visitseoul.net/attractions/Changdeokgung-Palace_/78"
    },
    {
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "coords": (37.582552, 126.983139),
        "desc": "전통 한옥이 모여 있는 인기 사진 스팟.",
        "link": "https://english.visitseoul.net/attractions/Bukchon-Hanok-Village_/80"
    },
    {
        "name": "N Seoul Tower (남산서울타워)",
        "coords": (37.551169, 126.988227),
        "desc": "서울 전경을 한눈에 보는 전망 스팟.",
        "link": "https://english.visitseoul.net/attractions/N-Seoul-Tower_/86"
    },
    {
        "name": "Myeongdong (명동)",
        "coords": (37.563845, 126.986055),
        "desc": "쇼핑·길거리음식으로 유명한 번화가.",
        "link": "https://english.visitseoul.net/shopping/Myeongdong_/100"
    },
    {
        "name": "Hongdae (홍대)",
        "coords": (37.556264, 126.923247),
        "desc": "젊음의 거리, 스트리트 퍼포먼스와 카페들.",
        "link": "https://english.visitseoul.net/attractions/Hongdae_/574"
    },
    {
        "name": "Insadong (인사동)",
        "coords": (37.574362, 126.984847),
        "desc": "전통 공예품·찻집이 많은 문화의 거리.",
        "link": "https://english.visitseoul.net/shopping/Insadong_/101"
    },
    {
        "name": "Dongdaemun Design Plaza (DDP, 동대문디자인플라자)",
        "coords": (37.566295, 127.009377),
        "desc": "현대 디자인과 야간 조명이 멋진 DDP.",
        "link": "https://english.visitseoul.net/attractions/Dongdaemun-Design-Plaza-DDP_/1803"
    },
    {
        "name": "Cheonggyecheon Stream (청계천)",
        "coords": (37.570028, 126.977829),
        "desc": "도심 속 산책로, 야간에 특히 아름다움.",
        "link": "https://english.visitseoul.net/nature/Cheonggyecheon_/2635"
    },
    {
        "name": "Lotte World Tower (롯데월드타워 / 석촌호수)",
        "coords": (37.513081, 127.102513),
        "desc": "한국에서 손꼽히는 초고층 타워와 전망대.",
        "link": "https://english.visitseoul.net/attractions/Lotte-World-Tower_/2742"
    },
]

# 사이드바: 표시할 장소 선택
st.sidebar.header("지도 표시 항목")
selected = {}
for p in places:
    selected[p["name"]] = st.sidebar.checkbox(p["name"], value=True)

# 마커 추가
for p in places:
    if selected.get(p["name"], False):
        # 팝업 HTML (간단)
        html = f"""
        <h4>{p['name']}</h4>
        <p>{p['desc']}</p>
        <a href="{p['link']}" target="_blank">공식 정보 보기</a>
        """
        folium.Marker(
            location=p["coords"],
            popup=folium.Popup(html, max_width=300),
            tooltip=p["name"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# Folium 지도를 Streamlit에 표시
st.subheader("지도 (Folium)")
st.caption("마커를 클릭하면 팝업으로 간단 설명과 링크가 뜹니다.")
st_data = st_folium(m, width=1100, height=600)

# 오른쪽 패널에 장소 목록과 설명을 보기 좋게
with st.expander("📍 Top10 리스트 (간단 설명) — 펼치기"):
    for p in places:
        checked = "✅" if selected.get(p["name"], False) else "⬜"
        st.write(f"{checked} **{p['name']}** — {p['desc']} — [더보기]({p['link']})")

# 하단: requirements 파일 내용 보여주기 및 다운로드
requirements_text = """streamlit==1.26.0
folium==0.14.0
streamlit-folium==0.12.0
"""
st.markdown("---")
st.subheader("설치용 requirements.txt")
st.code(requirements_text, language="text")
st.download_button("requirements.txt 다운로드", requirements_text, file_name="requirements.txt")
st.info("Streamlit Cloud에 업로드할 때는 이 파일과 app.py를 같은 리포지토리에 넣어 배포하세요.")

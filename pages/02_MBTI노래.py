# app.py
import streamlit as st
import random

st.set_page_config(page_title="MBTI 노래 추천 🎶", page_icon="🎵", layout="centered")

st.title("MBTI로 K-POP & POP 추천 🎧")
st.markdown("너의 **MBTI**를 선택하면 K-POP 한 곡, POP 한 곡을 추천해줄게! 💿<br>둘 다 실제로 존재하는 곡들이야 🎶", unsafe_allow_html=True)

MBTI_LIST = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# MBTI별 KPOP & POP 노래 목록
MBTI_RECOMMEND = {
    "ISTJ": {
        "kpop": {"title": "Love Dive", "artist": "IVE", "year": 2022, "genre": "K-Pop",
                 "reason": "깔끔하고 정돈된 비트, 차분한 완벽주의자 느낌의 ISTJ에게 찰떡 ✨"},
        "pop": {"title": "Blinding Lights", "artist": "The Weeknd", "year": 2019, "genre": "Pop / Synthwave",
                "reason": "규칙적인 리듬과 세련된 사운드가 체계적인 ISTJ 감성에 잘 맞아요 💡"}
    },
    "ISFJ": {
        "kpop": {"title": "Spring Day", "artist": "BTS", "year": 2017, "genre": "K-Pop / Ballad",
                 "reason": "따뜻하고 감성적인 분위기가 배려심 깊은 ISFJ에게 잘 어울려요 🤍"},
        "pop": {"title": "Someone Like You", "artist": "Adele", "year": 2011, "genre": "Pop / Soul",
                "reason": "잔잔하고 진심 어린 감정선이 따뜻한 ISFJ 마음에 쏙 들어요 🌷"}
    },
    "INFJ": {
        "kpop": {"title": "Blue & Grey", "artist": "BTS", "year": 2020, "genre": "K-Pop / Ballad",
                 "reason": "감정이 섬세하고 사색적인 INFJ의 내면에 닿는 위로곡 🌙"},
        "pop": {"title": "Hallelujah", "artist": "Leonard Cohen", "year": 1984, "genre": "Folk / Pop",
                "reason": "깊은 의미의 가사와 서정적인 멜로디가 INFJ의 감성에 찰떡 ✨"}
    },
    "INTJ": {
        "kpop": {"title": "Next Level", "artist": "aespa", "year": 2021, "genre": "K-Pop",
                 "reason": "논리적이고 목표 지향적인 INTJ에게 도전적인 분위기의 곡이 잘 어울려요 ⚡"},
        "pop": {"title": "Believer", "artist": "Imagine Dragons", "year": 2017, "genre": "Alternative Rock / Pop",
                "reason": "강렬한 메시지와 완성도 높은 사운드, 분석적 INTJ에게 찰떡 💥"}
    },
    "ISTP": {
        "kpop": {"title": "God’s Menu", "artist": "Stray Kids", "year": 2020, "genre": "K-Pop / Hip-hop",
                 "reason": "쿨하고 즉흥적인 ISTP가 좋아할 리듬감 넘치는 트랙 🎧"},
        "pop": {"title": "Billie Jean", "artist": "Michael Jackson", "year": 1982, "genre": "Pop / R&B",
                "reason": "세련된 비트와 자유로운 느낌이 ISTP의 스타일과 딱 맞아요 😎"}
    },
    "ISFP": {
        "kpop": {"title": "Palette", "artist": "IU ft. G-DRAGON", "year": 2017, "genre": "K-Pop / Pop",
                 "reason": "자신만의 색깔을 찾는 ISFP의 예술적인 감성과 어울려요 🎨"},
        "pop": {"title": "Summertime Sadness", "artist": "Lana Del Rey", "year": 2012, "genre": "Indie Pop",
                "reason": "감성적이고 부드러운 분위기가 예술적인 ISFP에게 잘 맞아요 🌸"}
    },
    "INFP": {
        "kpop": {"title": "Eight", "artist": "IU ft. SUGA", "year": 2020, "genre": "K-Pop / Indie",
                 "reason": "몽글몽글한 가사와 멜로디가 이상주의자 INFP의 마음에 와닿아요 🌈"},
        "pop": {"title": "Imagine", "artist": "John Lennon", "year": 1971, "genre": "Soft Rock / Pop",
                "reason": "평화롭고 희망적인 메시지가 INFP의 이상주의적 성향에 딱이에요 ☁️"}
    },
    "INTP": {
        "kpop": {"title": "LOVE DIVE", "artist": "IVE", "year": 2022, "genre": "K-Pop",
                 "reason": "새로운 시도와 개성 있는 사운드가 호기심 많은 INTP에게 어울려요 💫"},
        "pop": {"title": "Clocks", "artist": "Coldplay", "year": 2002, "genre": "Alternative Rock",
                "reason": "반복적이지만 복잡한 구조가 INTP의 사고를 자극해요 🔍"}
    },
    "ESTP": {
        "kpop": {"title": "MIC Drop", "artist": "BTS", "year": 2017, "genre": "K-Pop / Hip-hop",
                 "reason": "자신감 넘치고 도전적인 ESTP에게 에너지 넘치는 곡 💥"},
        "pop": {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "year": 2014, "genre": "Funk / Pop",
                "reason": "흥 많고 즉흥적인 ESTP에게 신나는 파티 느낌 가득 🎉"}
    },
    "ESFP": {
        "kpop": {"title": "Dynamite", "artist": "BTS", "year": 2020, "genre": "K-Pop / Disco Pop",
                 "reason": "밝고 흥 넘치는 ESFP에게 찰떡! 기분 업되는 노래 🌟"},
        "pop": {"title": "Shake It Off", "artist": "Taylor Swift", "year": 2014, "genre": "Pop",
                "reason": "긍정적인 에너지 뿜뿜! 모두를 즐겁게 하는 ESFP에게 잘 어울려요 🎤"}
    },
    "ENFP": {
        "kpop": {"title": "LILAC", "artist": "IU", "year": 2021, "genre": "K-Pop / Pop",
                 "reason": "감성적이면서도 밝은 분위기가 자유로운 ENFP에게 딱 🌸"},
        "pop": {"title": "Dog Days Are Over", "artist": "Florence + The Machine", "year": 2008, "genre": "Indie Pop",
                "reason": "희망차고 활기찬 에너지가 ENFP의 낙천적인 성향과 찰떡 🌈"}
    },
    "ENTP": {
        "kpop": {"title": "Zzz", "artist": "SEVENTEEN", "year": 2023, "genre": "K-Pop / R&B",
                 "reason": "장난기 많고 유쾌한 ENTP의 자유로운 에너지에 어울려요 😏"},
        "pop": {"title": "Seven Nation Army", "artist": "The White Stripes", "year": 2003, "genre": "Rock / Alternative",
                "reason": "도전적이고 반항적인 무드가 ENTP의 기질과 잘 맞아요 ⚡"}
    },
    "ESTJ": {
        "kpop": {"title": "Nxde", "artist": "(G)I-DLE", "year": 2022, "genre": "K-Pop / Pop",
                 "reason": "당당하고 자기주장 강한 ESTJ의 리더십과 찰떡 💪"},
        "pop": {"title": "Don't Stop Believin'", "artist": "Journey", "year": 1981, "genre": "Rock",
                "reason": "목표 지향적인 ESTJ에게 힘을 주는 명곡 🚀"}
    },
    "ESFJ": {
        "kpop": {"title": "TT", "artist": "TWICE", "year": 2016, "genre": "K-Pop / Pop",
                 "reason": "사람들과 공감 잘하는 ESFJ에게 귀엽고 친근한 분위기의 곡 💕"},
        "pop": {"title": "Perfect", "artist": "Ed Sheeran", "year": 2017, "genre": "Pop / Ballad",
                "reason": "사랑스럽고 따뜻한 가사가 ESFJ의 다정한 성향에 어울려요 🌹"}
    },
    "ENFJ": {
        "kpop": {"title": "Love Scenario", "artist": "iKON", "year": 2018, "genre": "K-Pop / Pop",
                 "reason": "사람과의 관계를 중요하게 생각하는 ENFJ에게 감정선이 찰떡 🎬"},
        "pop": {"title": "Count on Me", "artist": "Bruno Mars", "year": 2010, "genre": "Pop / Acoustic",
                "reason": "의리 있고 따뜻한 ENFJ에게 어울리는 메시지 🤝"}
    },
    "ENTJ": {
        "kpop": {"title": "Tomboy", "artist": "(G)I-DLE", "year": 2022, "genre": "K-Pop / Rock",
                 "reason": "자신감 넘치는 ENTJ의 카리스마와 완벽 매치 🔥"},
        "pop": {"title": "Eye of the Tiger", "artist": "Survivor", "year": 1982, "genre": "Rock",
                "reason": "도전과 승부욕의 상징! ENTJ의 리더십을 자극하는 곡 🦁"}
    }
}

# UI 구성
selected = st.selectbox("너의 MBTI를 골라줘 👇", MBTI_LIST)

if st.button("노래 추천받기 🎵"):
    data = MBTI_RECOMMEND.get(selected)
    if data:
        st.markdown("---")
        st.subheader("🎤 K-POP 추천")
        k = data["kpop"]
        st.write(f"**{k['title']}** — {k['artist']} ({k['year']})")
        st.write(f"**장르:** {k['genre']}")
        st.write(f"**추천 이유:** {k['reason']}")
        st.markdown("🎶✨🌈")
        
        st.markdown("---")
        st.subheader("🎧 POP 추천")
        p = data["pop"]
        st.write(f"**{p['title']}** — {p['artist']} ({p['year']})")
        st.write(f"**장르:** {p['genre']}")
        st.write(f"**추천 이유:** {p['reason']}")
        st.markdown("💫🎵🌍")
    else:
        st.error("MBTI를 잘못 선택했어요 😅 다시 골라줘!")

st.caption("모든 노래는 실제로 존재하는 1900년 이후의 곡들이에요 🎼")

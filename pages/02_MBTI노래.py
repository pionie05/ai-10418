# app.py
import streamlit as st
import random

st.set_page_config(page_title="MBTI 노래 추천 🎧", page_icon="🎵", layout="centered")

st.title("MBTI로 골라주는 노래 추천 🎶")
st.markdown("원하는 **MBTI**를 골라보자! 그 성격에 어울리는 실제 존재하는 노래(1900년 이후)를 한 곡 추천해줄게 — 장르랑 왜 추천하는지도 같이 알려줄게요 🙂")

MBTI_LIST = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 각 MBTI에 대응하는 여러 곡(곡정보: title, artist, year, genre, reason)
MBTI_SONGS = {
    "ISTJ": [
        {"title":"Bohemian Rhapsody", "artist":"Queen", "year":1975, "genre":"Rock",
         "reason":"구성과 완성도가 높아서 차분히 분석하고 규칙을 좋아하는 ISTJ에게 딱 맞아. 클래식한 락의 위엄 ✨"}
    ],
    "ISFJ": [
        {"title":"Fix You", "artist":"Coldplay", "year":2005, "genre":"Alternative / Pop Rock",
         "reason":"따뜻하고 위로가 되는 분위기라서 누군가를 돌보는 ISFJ의 감성에 잘 어울려요. 포근한 위로곡 🤍"}
    ],
    "INFJ": [
        {"title":"Hallelujah", "artist":"Leonard Cohen", "year":1984, "genre":"Folk / Singer-Songwriter",
         "reason":"심오하고 서정적인 가사가 INFJ의 내면적인 깊이와 공명해요. 조용히 곱씹기 좋은 곡 🌙"}
    ],
    "INTJ": [
        {"title":"The Sound of Silence", "artist":"Simon & Garfunkel", "year":1964, "genre":"Folk Rock",
         "reason":"지적인 분위기와 사색을 불러오는 멜로디가 INTJ의 분석적이고 내향적인 면과 잘 맞아요. 생각할 때 듣기 좋아요 🧠"}
    ],
    "ISTP": [
        {"title":"Billie Jean", "artist":"Michael Jackson", "year":1982, "genre":"Pop / R&B",
         "reason":"리듬감 있고 쿨한 트랙이라 행동파 ISTP가 즉흥적으로 즐기기 좋아요. 비트가 몸을 움직이게 함 🎧"}
    ],
    "ISFP": [
        {"title":"Summertime Sadness", "artist":"Lana Del Rey", "year":2012, "genre":"Indie Pop / Dream Pop",
         "reason":"감성적이고 이미지가 강한 사운드가 ISFP의 예술적 감수성과 잘 맞아요. 감정에 몰입하기 좋은 곡 🎨"}
    ],
    "INFP": [
        {"title":"Imagine", "artist":"John Lennon", "year":1971, "genre":"Soft Rock / Pop",
         "reason":"이상주의적이고 공감 능력이 높은 INFP에게 메시지와 평화로운 멜로디가 깊게 와닿을 거예요 ✨"}
    ],
    "INTP": [
        {"title":"Clocks", "artist":"Coldplay", "year":2002, "genre":"Alternative Rock",
         "reason":"복잡한 패턴과 반복되는 피아노 리프로 사고를 자극하는 편이라 INTP의 호기심을 만족시켜요 🔎"}
    ],
    "ESTP": [
        {"title":"Lose Yourself", "artist":"Eminem", "year":2002, "genre":"Hip Hop / Rap",
         "reason":"에너지 넘치고 몰아치는 느낌이 강해서 모험적이고 즉흥적인 ESTP가 힘낼 때 듣기 좋아요 💥"}
    ],
    "ESFP": [
        {"title":"Uptown Funk", "artist":"Mark Ronson ft. Bruno Mars", "year":2014, "genre":"Funk / Pop",
         "reason":"파티 분위기 최고! 밝고 신나는 트랙이라 사람들과 즐기길 좋아하는 ESFP한테 찰떡 👯‍♀️"}
    ],
    "ENFP": [
        {"title":"Dog Days Are Over", "artist":"Florence + The Machine", "year":2008, "genre":"Indie Pop / Indie Rock",
         "reason":"에너지 넘치고 희망찬 전개가 ENFP의 긍정적이고 창의적인 성향에 딱이에요. 기분 업! 🌈"}
    ],
    "ENTP": [
        {"title":"Seven Nation Army", "artist":"The White Stripes", "year":2003, "genre":"Rock / Alternative",
         "reason":"강렬하고 반복되는 리프가 도전적 사고와 장난기 많은 ENTP의 성향과 잘 맞아요. 신나는 반항기 😏"}
    ],
    "ESTJ": [
        {"title":"Don't Stop Believin'", "artist":"Journey", "year":1981, "genre":"Rock",
         "reason":"목표 지향적이고 단단한 메시지가 있어 ESTJ의 추진력과 어울려요. 다같이 따라 부르기 좋아요 🎤"}
    ],
    "ESFJ": [
        {"title":"Shake It Off", "artist":"Taylor Swift", "year":2014, "genre":"Pop",
         "reason":"밝고 긍정적인 에너지가 사람들 챙기기를 좋아하는 ESFJ에게 딱이에요. 기분 전환용으로 굿 ✨"}
    ],
    "ENFJ": [
        {"title":"Count on Me", "artist":"Bruno Mars", "year":2010, "genre":"Pop / Acoustic",
         "reason":"사람을 돕고 끌어주는 ENFJ의 따뜻한 면을 보여주는 가사와 멜로디가 잘 어울려요. 친구에게 추천하고픈 곡 🤝"}
    ],
    "ENTJ": [
        {"title":"Eye of the Tiger", "artist":"Survivor", "year":1982, "genre":"Rock",
         "reason":"강한 추진력과 승부욕을 자극하는 곡이라 ENTJ의 리더십과 목표 지향적인 태도에 맞아요 🔥"}
    ]
}

def recommend(mbti):
    choices = MBTI_SONGS.get(mbti, [])
    if not choices:
        return None
    return random.choice(choices)

# UI
selected = st.selectbox("너의 MBTI를 골라줘", MBTI_LIST)
if "last" not in st.session_state:
    st.session_state.last = None

if st.button("노래 추천받기 🎵"):
    song = recommend(selected)
    st.session_state.last = song

if st.session_state.last:
    s = st.session_state.last
    st.markdown("---")
    st.subheader(f"추천 곡 — {s['title']}  ·  {s['artist']} ({s['year']})")
    st.write(f"**장르:** {s['genre']}")
    # 감성적인 이유 설명 (친근한 말투)
    st.write(f"**추천 이유:** {s['reason']}")
    # 센스 있는 이모지 몇 개
    emoji_line = {
        "Rock": "🎸",
        "Pop": "🎤",
        "Hip Hop": "🎧",
        "Folk": "🌾",
        "Indie": "✨",
        "Funk": "🕺",
        "Alternative": "🎚️"
    }
    # 한두개 이모지를 추가로 보여주기 (장르 키워드로 매칭 시도)
    genre_tag = s['genre'].lower()
    extras = []
    if "rock" in genre_tag:
        extras.append("🎸")
    if "pop" in genre_tag:
        extras.append("🎤")
    if "hip" in genre_tag or "rap" in genre_tag:
        extras.append("🔥")
    if "folk" in genre_tag or "singer" in genre_tag:
        extras.append("🌙")
    if "indie" in genre_tag or "dream" in genre_tag:
        extras.append("✨")
    if not extras:
        extras.append("🎵")
    # 보여주기
    st.markdown("".join(extras) + "  즐겨봐~")
    st.markdown("---")
    if st.button("다른 곡으로 바꿔볼래"):
        st.session_state.last = recommend(selected)
        st.experimental_rerun()
else:
    st.info("MBTI를 선택하고 '노래 추천받기' 버튼을 눌러줘 — 재밌는 곡들 준비되어 있어요 😊")

st.caption("참고: 추천 곡은 모두 실제로 존재하는(1900년 이후 발표) 곡들입니다.")

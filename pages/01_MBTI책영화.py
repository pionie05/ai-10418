# app.py
# Streamlit만 사용합니다 (추가 라이브러리 설치 금지).
import streamlit as st

st.set_page_config(page_title="MBTI 추천 북&무비", page_icon="📚🎬", layout="centered")

st.title("MBTI 기반 책 & 영화 추천 💡")
st.caption("MBTI를 고르면 어울리는 책 2권과 영화 2편을 추천해줄게 — 짧은 줄거리와 함께! 😊")

mbti_list = [
    "ISTJ","ISFJ","INFJ","INTJ","ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP","ESTJ","ESFJ","ENFJ","ENTJ"
]

recommendations = {
    "ISTJ": {
        "books": [
            ("The Remains of the Day (가즈오 이시구로)", "과거를 되돌아보며 책임과 직무에 대해 성찰하는 중년 집사의 이야기. 책임감 강한 타입에게 공감 갈 거예요. 📖"),
            ("1984 (조지 오웰)", "감시와 통제의 사회를 그린 디스토피아 소설. 논리적으로 세상을 보는 ISTJ에게 자극적일 수 있어요. 🔍")
        ],
        "movies": [
            ("A Few Good Men (1992)", "법정 드라마로 규칙과 의무, 진실에 대한 갈등을 그려요. 군기와 규율을 중요시하는 분들 추천. ⚖️"),
            ("Bridge of Spies (2015)", "냉전 시대 협상과 신중한 전략을 다룬 실화 기반 영화. 계획적이고 신중한 성향에 잘 맞아요. 🕊️")
        ]
    },
    "ISFJ": {
        "books": [
            ("Little Women (루이자 메이 올컷)", "가족과 사랑, 성장 이야기를 따뜻하게 그려요. 배려심 많은 ISFJ에게 포근한 위로가 됩니다. 🧶"),
            ("The Help (캐스린 스토켓트)", "인간관계와 연대를 다룬 소설로, 타인을 돌보는 마음이 큰 분들에게 울림을 줘요. ☕")
        ],
        "movies": [
            ("Pride & Prejudice (2005)", "감정 표현과 배려가 중요한 계층·사랑 이야기를 아름답게 담았어요. 💃"),
            ("The King's Speech (2010)", "책임과 타인을 돕는 용기에 관한 실화. 따뜻하고 감동적이죠. 🎙️")
        ]
    },
    "INFJ": {
        "books": [
            ("The Little Prince (생택쥐페리)", "사소한 것들에 담긴 의미를 깊게 생각하게 하는 철학적 동화. 내면을 중요시하는 INFJ와 딱 맞아요. 🌟"),
            ("The Alchemist (파울로 코엘료)", "자기 발견과 운명에 관한 이야기로 영감과 의미를 찾는 분들께 추천. ✨")
        ],
        "movies": [
            ("Eternal Sunshine of the Spotless Mind (2004)", "기억과 관계, 정체성에 대해 섬세하게 탐구하는 영화예요. 감성적인 INFJ에게 강하게 와닿을 거예요. 💭"),
            ("Good Will Hunting (1997)", "내적 갈등과 성장, 타인의 이해를 다룬 드라마. 치유와 통찰을 좋아한다면 추천해요. 🧠")
        ]
    },
    "INTJ": {
        "books": [
            ("Foundation (아이작 아시모프)", "거대한 계획과 장기 전략을 다룬 SF 대작. 체계적이고 미래 지향적인 INTJ에게 추천. 🚀"),
            ("The Fountainhead (아인 랜드)", "개인의 원칙과 창조성, 논리적 주장에 집중하는 작품입니다. 💡")
        ],
        "movies": [
            ("Inception (2010)", "복잡한 구조와 전략을 즐길 줄 아는 사람에게 완벽한 영화. 꿈과 현실을 계산적으로 다뤄요. 🌀"),
            ("The Social Network (2010)", "전략과 야망, 체계적 사고의 드라마 — 비즈니스적 사고를 자극해요. 💻")
        ]
    },
    "ISTP": {
        "books": [
            ("The Martian (앤디 위어)", "문제 해결 능력이 돋보이는 생존 SF. 실용적이고 즉흥적인 ISTP에게 딱 맞아요. 🛠️"),
            ("Into the Wild (존 크라카어)", "자유와 모험을 찾아 떠난 실화로, 행동 중심의 삶을 이해하게 해줘요. 🏕️")
        ],
        "movies": [
            ("Mad Max: Fury Road (2015)", "액션과 순간 판단, 실전 감각을 좋아하는 분들에게 추천. 속도감이 짜릿해요. 🔥"),
            ("Drive (2011)", "묵묵히 행동으로 말하는 주인공과 스타일리시한 액션이 매력적이에요. 🚗")
        ]
    },
    "ISFP": {
        "books": [
            ("Norwegian Wood (무라카미 하루키)", "감성적이고 섬세한 내면 묘사 — 아름답고 쓸쓸한 감정을 좋아한다면 추천. 🌲"),
            ("The Secret Garden (프랜시스 호지슨 버넷)", "자연과 치유, 감성적 성장을 따뜻하게 그린 이야기예요. 🌸")
        ],
        "movies": [
            ("Amélie (2001)", "작은 친절과 감성으로 세상을 비추는 따뜻한 영화. 감성적인 경험을 좋아할 거예요. 🥐"),
            ("Call Me By Your Name (2017)", "섬세한 감정선과 아름다운 분위기를 담은 작품. 예술적 감수성에 호소해요. ☀️")
        ]
    },
    "INFP": {
        "books": [
            ("The Little Prince (생택쥐페리)", "순수한 시선으로 의미를 묻는 이야기 — 이상과 가치를 중시하는 INFP에게 추천. 🌙"),
            ("The Perks of Being a Wallflower (스티븐 최보스키)", "내성적 성장과 우정, 감정의 진폭을 섬세히 다룹니다. 💌")
        ],
        "movies": [
            ("Eternal Sunshine of the Spotless Mind (2004)", "사랑과 기억, 내면의 상처를 예민하게 다루는 작품. 감성적 성찰을 좋아하면 강추. 💔"),
            ("Her (2013)", "감정과 연결, 인간관계의 의미를 부드럽게 묻는 SF 로맨스. 감수성 높은 분들 환영. 🤖❤️")
        ]
    },
    "INTP": {
        "books": [
            ("Gödel, Escher, Bach (더글라스 호프스태터)", "논리·창의·인지의 연결을 깊게 파는 책. 분석적 호기심이 많은 INTP에게 매력적이에요. 🧩"),
            ("The Name of the Rose (움베르토 에코)", "지성적인 미스터리와 철학적 질문이 섞인 역사 소설. 사고의 즐거움을 줍니다. 📜")
        ],
        "movies": [
            ("The Imitation Game (2014)", "논리와 퍼즐 해결을 즐기는 이들에게 맞는 실화 기반 드라마. 🧠"),
            ("Primer (2004)", "초저예산 시간여행 영화지만 논리와 퍼즐이 빽빽해서 골똘히 생각하게 해요. ⏳")
        ]
    },
    "ESTP": {
        "books": [
            ("The Outsiders (S.E. Hinton)", "행동 중심의 에너지와 충동, 현실적 갈등을 담은 소설. 빠른 전개 좋아하는 분에게 추천. ⚡"),
            ("The Bourne Identity (로버트 래들럼)", "액션과 기민한 대처가 주된 스파이 스릴러예요. 스릴을 좋아하면 딱! 🧭")
        ],
        "movies": [
            ("Ocean's Eleven (2001)", "속도감 있고 기민한 플랜과 팀워크를 즐길 수 있는 재밌는 범죄 영화. 💼"),
            ("Baby Driver (2017)", "리듬감 있는 액션과 직관적 판단이 매력적인 작품. 음악과 속도 좋아하면 추천. 🎧")
        ]
    },
    "ESFP": {
        "books": [
            ("The Hitchhiker's Guide to the Galaxy (더글라스 애덤스)", "유머와 즉흥성이 가득한 SF 코미디. 즐거운 분위기 좋아하는 ESFP에게 딱! 🚀"),
            ("Eat Pray Love (엘리자베스 길버트)", "여행과 즐거움, 자기 발견의 이야기가 가볍게 다가와요. ✈️")
        ],
        "movies": [
            ("La La Land (2016)", "음악·꿈·사랑을 밝고 화려하게 담아낸 뮤지컬 영화. 에너지 넘치는 취향에 추천. 🎶"),
            ("The Greatest Showman (2017)", "쇼맨십과 퍼포먼스, 화려함을 좋아하는 분께 즐거운 영화예요. 🎪")
        ]
    },
    "ENFP": {
        "books": [
            ("The Alchemist (파울로 코엘료)", "모험과 내적 탐색, 가능성을 꿈꾸는 이야기. 창의적이고 열정적인 ENFP에게 추천. 🌈"),
            ("The Perks of Being a Wallflower (스티븐 최보스키)", "감정과 우정, 자기 발견이 생생하게 그려져 공감 가요. 💫")
        ],
        "movies": [
            ("Amélie (2001)", "작은 기쁨을 찾아 세상을 바꾸려는 밝은 에너지의 영화. 창의적 감수성에 잘 맞아요. 🎨"),
            ("Inside Out (2015)", "감정의 다양성을 유쾌하고 창의적으로 보여주는 애니메이션. 감정 표현을 좋아하면 추천. 😊")
        ]
    },
    "ENTP": {
        "books": [
            ("The Innovators (월터 아이작슨)", "아이디어와 발명, 토론을 즐기는 사람들에게 영감을 주는 책이에요. 🔧"),
            ("The Hitchhiker's Guide to the Galaxy (더글라스 애덤스)", "기발한 유머와 아이디어 폭발 — 토론과 반전 좋아하면 추천. 🛸")
        ],
        "movies": [
            ("The Social Network (2010)", "아이디어와 논쟁, 창업 드라마로 빠른 사고를 즐기는 타입에 맞아요. 🧩"),
            ("Catch Me If You Can (2002)", "재치와 순간 판단, 말발로 상황을 바꾸는 주인공이 매력적이에요. 🎭")
        ]
    },
    "ESTJ": {
        "books": [
            ("The Prince (마키아벨리)", "리더십과 권력의 현실적 전략을 냉정하게 다루는 고전. 조직적이고 실무적인 ESTJ에게 추천. 🏛️"),
            ("To Kill a Mockingbird (하퍼 리)", "정의와 규범, 책임에 관한 이야기로 도덕적 판단을 자극해요. ⚖️")
        ],
        "movies": [
            ("A Few Good Men (1992)", "규율·의무·정의를 중심으로 한 강렬한 법정 드라마. 군기와 규칙을 중시한다면 추천. 🪖"),
            ("The Big Short (2015)", "시스템을 파악하고 실무적으로 문제를 풀어내는 이야기. 현실적 분석을 즐긴다면 좋아요. 💼")
        ]
    },
    "ESFJ": {
        "books": [
            ("Pride and Prejudice (제인 오스틴)", "관계와 사회적 규범, 따뜻한 유머를 담은 고전. 사람을 돌보는 ESFJ에게 잘 맞아요. 🎩"),
            ("To Kill a Mockingbird (하퍼 리)", "공감과 정의, 공동체를 생각하게 하는 작품이에요. 🤝")
        ],
        "movies": [
            ("The Help (2011)", "사람 사이의 연대와 배려를 다룬 드라마로 따뜻한 감동을 줍니다. ☕"),
            ("Forrest Gump (1994)", "순수한 마음과 타인을 향한 배려가 중심인 이야기예요. 마음이 따뜻해져요. 🏃‍♂️")
        ]
    },
    "ENFJ": {
        "books": [
            ("To Kill a Mockingbird (하퍼 리)", "리더십, 정의, 타인에 대한 이해를 강조하는 감동적인 소설. 사람을 이끄는 ENFJ에게 추천. 🌱"),
            ("The Kite Runner (칼레드 호세이니)", "우정과 속죄, 감정적 울림이 큰 드라마틱한 이야기예요. 🤲")
        ],
        "movies": [
            ("Dead Poets Society (1989)", "영감을 주고 이끄는 리더십과 가르침이 주제인 영화. 사람을 돕는 ENFJ에겐 울림이 큽니다. 📚"),
            ("The Pursuit of Happyness (2006)", "희망과 타인을 이끄는 힘에 관한 실화 기반 이야기. 감동과 동기 부여가 있어요. 💼")
        ]
    },
    "ENTJ": {
        "books": [
            ("The Prince (마키아벨리)", "권력과 전략, 리더십의 현실적 기술을 다룬 책으로 추진력 있는 ENTJ에게 잘 맞아요. ♟️"),
            ("Atlas Shrugged (아인 랜드)", "체계적 사상과 강한 주장을 담은 소설—리더십과 비전 추구에 맞는 작품. 🏗️")
        ],
        "movies": [
            ("The Wolf of Wall Street (2013)", "야망과 리더십, 추진력을 극단적으로 보여주는 실화 기반 영화. ⚡"),
            ("The Big Short (2015)", "시장을 분석하고 전략을 세우는 능력을 자극하는 영화예요. 📈")
        ]
    }
}

selected = st.selectbox("당신의 MBTI를 골라줘 ✨", mbti_list)

st.markdown("---")
st.header(f"{selected}님을 위한 추천 목록 📝")

data = recommendations.get(selected)
if data:
    st.subheader("📚 책 추천 (2권)")
    for title, summary in data["books"]:
        st.markdown(f"**{title}**  {summary}")
    st.subheader("🎬 영화 추천 (2편)")
    for title, summary in data["movies"]:
        st.markdown(f"**{title}**  {summary}")
else:
    st.write("아직 추천이 준비되지 않았어요 😅")

st.markdown("---")
st.caption("※ 추천은 성격 유형을 참고한 제안이에요 — 기분 따라 골라보는 것도 재밌습니다! 😄")

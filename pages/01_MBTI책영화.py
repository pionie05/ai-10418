import streamlit as st

st.set_page_config(page_title="MBTI 추천북&영화", page_icon="📚🎬", layout="centered")

MBTI_OPTIONS = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ",
]

# 추천 데이터: 각 항목은 (책1, 저자1, 요약1), (책2,...), (영화1,년도,요약1), (영화2,...)
RECOMMENDATIONS = {
    "ISTJ": {
        "books":[
            ("The Remains of the Day","Kazuo Ishiguro","내면의 책임감과 성찰을 다룬 소설로, 한 집사의 삶을 통해 의무와 후회의 감정을 보여줘요."),
            ("Great Expectations","Charles Dickens","성장과 사회적 기대를 다룬 고전 — 인물의 변화와 현실의 단면을 그려요."),
        ],
        "movies":[
            ("The King's Speech",2010,"한 국왕의 말을 다루는 이야기로, 책임감과 극복을 담은 드라마예요."),
            ("Spotlight",2015,"기자들이 진실을 추적하는 실제 이야기를 바탕으로 한 사회 드라마예요."),
        ]
    },
    "ISFJ": {
        "books":[
            ("Little Women","Louisa May Alcott","가족과 성장, 서로를 돕는 따뜻한 이야기예요 — 감성 충만!"),
            ("The Secret Garden","Frances Hodgson Burnett","치유와 우정이 중심인 동심 가득한 소설이에요."),
        ],
        "movies":[
            ("Amélie",2001,"작고 섬세한 행복을 찾아가는 프랑스 영화 — 마음이 따뜻해져요."),
            ("Paddington",2014,"다정한 모험과 가족애가 돋보이는 가족 영화예요."),
        ]
    },
    "INFJ": {
        "books":[
            ("The Alchemist","Paulo Coelho","꿈과 운명을 찾아 떠나는 은유 가득한 이야기 — 영감을 주는 책이에요."),
            ("Never Let Me Go","Kazuo Ishiguro","기억과 정체성을 담담히 탐구하는 묵직한 소설이에요."),
        ],
        "movies":[
            ("Her",2013,"연애와 고독, 기술 시대의 관계를 섬세하게 그린 영화예요."),
            ("The Pursuit of Happyness",2006,"희망과 인내를 보여주는 실제 이야기를 바탕으로 한 감동 실화예요."),
        ]
    },
    "INTJ": {
        "books":[
            ("1984","George Orwell","감시와 권력을 경고하는 디스토피아 고전 — 생각할 거리를 많이 줘요."),
            ("The Name of the Wind","Patrick Rothfuss","대서사 판타지로 지적 호기심을 자극하는 이야기예요."),
        ],
        "movies":[
            ("Inception",2010,"꿈과 현실의 경계를 뒤흔드는 뇌절(?)스러운 스릴러예요."),
            ("The Imitation Game",2014,"천재의 고뇌와 역사적 문제를 담은 전기 드라마예요."),
        ]
    },
    "ISTP": {
        "books":[
            ("Into the Wild","Jon Krakauer","자유를 찾아 떠난 실제 인물의 이야기 — 모험과 자기 탐색의 기록이에요."),
            ("The Martian","Andy Weir","실용적 문제 해결과 위트가 돋보이는 SF 서바이벌 소설이에요."),
        ],
        "movies":[
            ("Mad Max: Fury Road",2015,"속도감과 액션이 압도적인 포스트아포칼립스 영화예요."),
            ("Ford v Ferrari",2019,"레이싱과 도전, 실화를 바탕으로 한 스릴 넘치는 드라마예요."),
        ]
    },
    "ISFP": {
        "books":[
            ("The Little Prince","Antoine de Saint-Exup\u00e9ry","순수함과 철학이 어우러진 짧은 우화 — 마음이 편해져요."),
            ("Eat Pray Love","Elizabeth Gilbert","자기 발견의 여행기 — 감각적이고 솔직한 에세이예요."),
        ],
        "movies":[
            ("La La Land",2016,"예술과 사랑, 꿈 사이에서 갈등하는 청춘의 뮤지컬 영화예요."),
            ("The Secret Life of Walter Mitty",2013,"일상을 벗어나 모험을 찾는 따뜻한 성장 영화예요."),
        ]
    },
    "INFP": {
        "books":[
            ("The Book Thief","Markus Zusak","전쟁 속에서 책과 이야기가 가진 힘을 그린 감성 소설이에요."),
            ("The Bell Jar","Sylvia Plath","내면의 감정과 정체성을 솔직하게 들여다보는 작품이에요."),
        ],
        "movies":[
            ("Into the Wild",2007,"자연과 자유, 자기 발견을 그린 실화 기반 영화예요."),
            ("Pan's Labyrinth",2006,"환상과 현실이 뒤섞인 어두운 동화 같은 영화예요."),
        ]
    },
    "INTP": {
        "books":[
            ("Gödel, Escher, Bach","Douglas Hofstadter","아이디어의 연결과 사고 실험이 가득한 지적 도전서예요."),
            ("Flatland","Edwin A. Abbott","수학적 상상력을 자극하는 짧은 풍자 소설이에요."),
        ],
        "movies":[
            ("The Social Network",2010,"창업과 인간관계를 날카롭게 그린 드라마예요."),
            ("Good Will Hunting",1997,"천재와 치유, 성장의 이야기를 담은 감동 영화예요."),
        ]
    },
    "ESTP": {
        "books":[
            ("On the Road","Jack Kerouac","즉흥적 모험과 자유를 좇는 전형적 로드 무비격 소설이에요."),
            ("The Art of War","Sun Tzu","전략적 사고와 실용적 조언이 담긴 고전에서 배울 점이 많아요."),
        ],
        "movies":[
            ("The Fast and the Furious",2001,"액션과 스피드를 좋아한다면 바로 이 시리즈!"),
            ("Die Hard",1988,"클래식 액션의 정석 — 긴장감 넘치는 스릴러예요."),
        ]
    },
    "ESFP": {
        "books":[
            ("The Perks of Being a Wallflower","Stephen Chbosky","청춘의 고민과 우정을 솔직하게 담은 성장소설이에요."),
            ("Where'd You Go, Bernadette","Maria Semple","유머와 가족애가 섞인 현대 소설로 가볍게 읽기 좋아요."),
        ],
        "movies":[
            ("Mean Girls",2004,"학교 생활과 우정, 웃음이 공존하는 팝 컬처 영화예요."),
            ("Mamma Mia!",2008,"신나는 노래와 축제 같은 기분을 주는 뮤지컬 영화예요."),
        ]
    },
    "ENFP": {
        "books":[
            ("The Hitchhiker's Guide to the Galaxy","Douglas Adams","유머와 상상력이 폭발하는 SF 모험소설이에요."),
            ("The Alchemist","Paulo Coelho","꿈을 좇는 모험과 은유가 많은 책 — 영감 충전용!"),
        ],
        "movies":[
            ("Big Fish",2003,"환상과 가족 이야기가 어우러진 따뜻한 영화예요."),
            ("The Secret Life of Walter Mitty",2013,"모험을 통해 성장하는 설레는 이야기예요."),
        ]
    },
    "ENTP": {
        "books":[
            ("Freakonomics","Steven D. Levitt & Stephen J. Dubner","일상의 숨은 인과를 재미있게 파헤치는 책이에요."),
            ("The Hitchhiker's Guide to the Galaxy","Douglas Adams","기상천외한 유머와 아이디어가 가득해요."),
        ],
        "movies":[
            ("The Big Short",2015,"시사적 사건을 재치 있게 풀어낸 똑똑한 다큐드라마예요."),
            ("Catch Me If You Can",2002,"사기와 추적의 쫓고 쫓기는 이야기 — 유쾌하고 빠른 전개가 특징이에요."),
        ]
    },
    "ESTJ": {
        "books":[
            ("The Prince","Niccol\u00f2 Machiavelli","리더십과 권력의 현실적인 조언이 담긴 고전이에요."),
            ("The 7 Habits of Highly Effective People","Stephen R. Covey","실용적 자기관리와 리더십 팁을 얻기 좋아요."),
        ],
        "movies":[
            ("12 Angry Men",1957,"합리적 토론과 정의를 다룬 명작 드라마예요."),
            ("The Social Network",2010,"조직과 리더십, 갈등을 다룬 현대 드라마예요."),
        ]
    },
    "ESFJ": {
        "books":[
            ("Pride and Prejudice","Jane Austen","사랑과 사회적 관습을 가볍게, 그러나 예리하게 그린 소설이에요."),
            ("The Help","Kathryn Stockett","우정과 용기를 다룬 감동적인 현대 소설이에요."),
        ],
        "movies":[
            ("The Holiday",2006,"로맨틱 코미디로 편안하고 기분 좋은 영화예요."),
            ("Little Women",2019,"가족과 우정, 성장을 다채롭게 그린 영화예요."),
        ]
    },
    "ENFJ": {
        "books":[
            ("To Kill a Mockingbird","Harper Lee","정의와 공감, 성장의 이야기를 담은 고전이에요."),
            ("Man's Search for Meaning","Viktor E. Frankl","삶의 의미를 찾는 강렬한 에세이형 회고록이에요."),
        ],
        "movies":[
            ("Dead Poets Society",1989,"영감과 리더십을 주는 교실 드라마예요."),
            ("The King's Speech",2010,"리더의 고뇌와 극복을 담은 감동 실화예요."),
        ]
    },
    "ENTJ": {
        "books":[
            ("Atlas Shrugged","Ayn Rand","야망과 시스템을 다루는 대서사 소설 — 논쟁적이지만 생각거리 많음."),
            ("The Lean Startup","Eric Ries","실용적 리더와 창업가 정신에 관한 필독서예요."),
        ],
        "movies":[
            ("The Godfather",1972,"권력과 가족, 전략이 만나는 걸작 드라마예요."),
            ("The Imitation Game",2014,"천재성과 리더십, 역사적 선택을 다룬 영화예요."),
        ]
    },
}

st.title("📚🎬 MBTI별 책 & 영화 추천기")
st.write("너의 MBTI를 골라줘! 각 유형에 딱 맞는 책 2권과 영화 2편을 골라줄게 — 줄거리도 짧게 알려줘 🙂")

mbti = st.selectbox("MBTI 선택", options=MBTI_OPTIONS)

if mbti:
    data = RECOMMENDATIONS.get(mbti)
    st.markdown(f"### ✅ {mbti}에게 추천하는 책 2권")
    for title, author, summary in data["books"]:
        st.markdown(f"**{title}** — *{author}*  
> {summary} 🔖")

    st.markdown(f"### ✅ {mbti}에게 추천하는 영화 2편")
    for title, year, summary in data["movies"]:
        st.markdown(f"**{title}** ({year})  
> {summary} 🎬")

    st.info("추천은 가벼운 제안이야 — 마음에 드는 걸 골라서 읽어봐!")

st.write("---")
st.write("앱은 Streamlit으로 제작되었어요. 추가로 바꾸고 싶은 문구나 추천 스타일이 있으면 알려줘~")

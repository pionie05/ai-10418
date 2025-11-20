import streamlit as st
import pandas as pd
from io import StringIO

# 1. 데이터 준비 (CSV 파일을 코드로 직접 가져옴)
# 별도의 파일 업로드 과정 없이 코드가 바로 실행되도록 문자열로 데이터를 저장했어!
csv_data = """
연령대,1위 음료,2위 음료,3위 음료,4위 음료,5위 음료
10대,아메리카노,카페 라떼,자바 칩 프라푸치노,카라멜 마끼아또,화이트 초콜릿 모카
20대,아메리카노,카페 라떼,자몽 허니 블랙 티,돌체 콜드 브루,카페 모카
30~40대,아메리카노,카페 라떼,돌체 콜드 브루 / 돌체 라떼,카페 모카,자바 칩 프라푸치노
50대 이상,디카페인 아메리카노,카페 라떼,카페 모카,자몽 허니 블랙 티,돌체 콜드 브루
"""

# StringIO를 이용해 문자열 데이터를 Pandas DataFrame으로 변환
df = pd.read_csv(StringIO(csv_data))

# 2. Streamlit 앱 설정
def run_app():
    # 제목 설정 - 이모지 센스있게!
    st.title("🌟 나의 취향은? 스타벅스 TOP 5 음료 분석! ☕️")
    st.markdown("---")
    
    # 청소년에게 친근한 말투로 안내 메시지!
    st.header("😎 너의 연령대를 골라봐!")
    st.subheader("가장 핫한 음료들을 알려줄게!")

    # 연령대 선택 드롭다운 메뉴
    age_groups = df['연령대'].unique().tolist()
    
    # '연령대 선택'을 기본값으로 설정하고 사용자가 선택하도록 유도
    selected_age = st.selectbox(
        '👇 아래에서 너에게 해당하는 연령대를 선택해줘!',
        options=['연령대 선택'] + age_groups,
        index=0  # 기본값으로 '연령대 선택'이 보이도록 설정
    )

    # 3. 결과 표시
    if selected_age == '연령대 선택':
        st.info("👈 왼쪽에서 연령대를 골라야 결과를 볼 수 있어! 고고씽! 🚀")
        
    else:
        # 선택된 연령대의 데이터 필터링
        result = df[df['연령대'] == selected_age].iloc[0]
        
        # 결과 메시지
        st.success(f"🎉 **{selected_age}**의 취향은 바로 이거였어! 대박! 🤩")
        st.markdown("### 🏆 TOP 5 인기 음료 랭킹")

        # 음료 리스트를 예쁘게 정리
        drinks = {
            '🥇 1위': result['1위 음료'],
            '🥈 2위': result['2위 음료'],
            '🥉 3위': result['3위 음료'],
            '4️⃣ 4위': result['4위 음료'],
            '5️⃣ 5위': result['5위 음료'],
        }
        
        # Markdown을 사용하여 순위별로 출력
        for rank, drink in drinks.items():
            st.markdown(f"**{rank}**: **{drink}**")
            
        st.balloons() # 결과가 나오면 풍선 효과 추가! 🎈

# 앱 실행
if __name__ == "__main__":
    run_app()

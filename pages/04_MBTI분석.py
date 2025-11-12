import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from plotly.colors import n_colors

# 페이지 설정
st.set_page_config(page_title="MBTI 국가별 분석", layout="wide")

# -------------------------------
# 1️⃣ 데이터 불러오기 함수
# -------------------------------
@st.cache_data
def load_data():
    # ✅ CSV 파일은 상위 폴더에 있음
    csv_path = Path(__file__).resolve().parent.parent / "countriesMBTI_16types.csv"

    if not csv_path.exists():
        st.error(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
        st.stop()

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        st.error("❌ CSV 파일이 비어있습니다. 데이터를 확인하세요.")
        st.stop()
    except Exception as e:
        st.error(f"❌ CSV 파일을 불러오는 중 오류 발생: {e}")
        st.stop()

    # 컬럼 정리
    df.columns = df.columns.str.strip()
    if "Country" not in df.columns:
        st.error("❌ CSV에 'Country' 컬럼이 없습니다.")
        st.stop()

    df["Country"] = df["Country"].astype(str)
    mbti_cols = [c for c in df.columns if c != "Country"]
    return df, mbti_cols

# -------------------------------
# 2️⃣ 색상 생성 함수
# -------------------------------
def make_colors(values):
    """1등은 하늘색, 나머지는 검정~회색 그라데이션"""
    n = len(values)
    if n == 0:
        return []

    top_color = "rgb(135,206,250)"       # 하늘색 (1등)
    gradient_from = "rgb(0,0,0)"         # 검정
    gradient_to = "rgb(180,180,180)"     # 회색

    grad_colors = n_colors(gradient_from, gradient_to, n, colortype="rgb")
    grad_colors[0] = top_color  # 1등 색상 강조
    return grad_colors

# -------------------------------
# 3️⃣ 데이터 로드
# -------------------------------
df, mbti_cols = load_data()

# -------------------------------
# 4️⃣ UI 구성
# -------------------------------
st.title("🌍 국가별 MBTI 분포 분석")
st.markdown("선택한 국가의 MBTI 유형 비율을 시각적으로 확인하세요 💡")

country = st.selectbox("국가를 선택하세요 🌎", sorted(df["Country"].unique()))

# -------------------------------
# 5️⃣ 선택한 국가 데이터 처리
# -------------------------------
country_data = df[df["Country"] == country].iloc[0]
values = [country_data[col] for col in mbti_cols]

# 내림차순 정렬
sorted_data = sorted(zip(mbti_cols, values), key=lambda x: x[1], reverse=True)
mbti_sorted, values_sorted = zip(*sorted_data)

colors = make_colors(values_sorted)

# -------------------------------
# 6️⃣ Plotly 시각화
# -------------------------------
fig = px.bar(
    x=mbti_sorted,
    y=values_sorted,
    title=f"🇨🇭 {country}의 MBTI 유형 비율",
    labels={"x": "MBTI 유형", "y": "비율(%)"},
)

fig.update_traces(marker_color=colors, hovertemplate="%{x}: %{y}%")

fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율(%)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font=dict(size=22, color="black"),
)

st.plotly_chart(fig, use_container_width=True)

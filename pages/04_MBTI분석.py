import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from plotly.colors import n_colors

# 페이지 설정
st.set_page_config(page_title="MBTI 국가별 분석", layout="wide")

@st.cache_data
def load_data():
    # ✅ 상위 폴더의 CSV 파일 경로 지정
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

    # 컬럼 이름 및 데이터 확인
    df.columns = df.columns.str.strip()
    if "Country" not in df.columns:
        st.error("❌ CSV에 'Country' 컬럼이 없습니다.")
        st.stop()

    df["Country"] = df["Country"].astype(str)
    mbti_cols = [c for c in df.columns if c != "Country"]
    return df, mbti_cols


def make_colors(values, top_color="rgb(255,182,193)", gradient_from="rgb(144,238,144)", gradient_to="rgb(224,255,224)"):
    """1등은 핑크, 나머지는 연두색 그라데이션"""
    n = len(values)
    if n == 0:
        return []
    grad_colors = n_colors(gradient_from, gradient_to, n, colortype="rgb")
    grad_colors[0] = top_color
    return grad_colors


# ✅ 데이터 불러오기
df, mbti_cols = load_data()

# UI 구성
st.title("🌍 국가별 MBTI 분포 분석")
st.markdown("각 국가별 MBTI 유형 비율을 시각적으로 확인해보세요.")

# 국가 선택
country = st.selectbox("국가를 선택하세요 🌎", sorted(df["Country"].unique()))

# 선택한 국가 데이터
country_data = df[df["Country"] == country].iloc[0]
values = [country_data[col] for col in mbti_cols]

# 비율 순 정렬
sorted_data = sorted(zip(mbti_cols, values), key=lambda x: x[1], reverse=True)
mbti_sorted, values_sorted = zip(*sorted_data)

# 색상 생성
colors = make_colors(values_sorted)

# Plotly 막대 그래프
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
)

st.plotly_chart(fig, use_container_width=True)

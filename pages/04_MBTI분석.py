import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import n_colors, hex_to_rgb
from pathlib import Path

st.set_page_config(page_title="MBTI by Country", layout="wide")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parent.parent / "countriesMBTI_16types.csv"
    if not csv_path.exists():
        st.error(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path.name} 파일을 루트 폴더에 두세요.")
        st.stop()
    df = pd.read_csv(csv_path)
    df["Country"] = df["Country"].astype(str)
    mbti_cols = [c for c in df.columns if c != "Country"]
    return df, mbti_cols


# -----------------------------
# HEX → RGB 변환 + 색상 그라데이션 함수
# -----------------------------
def make_colors(values, top_color="#FF69B4", gradient_from="#E6F9D5", gradient_to="#4CAF50"):
    vals = list(values)
    max_idx = int(pd.Series(vals).idxmax())

    def hex_to_rgb_str(h):
        rgb = hex_to_rgb(h)
        return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"

    n_non_top = max(0, len(vals) - 1)
    grad_colors = n_colors(
        hex_to_rgb_str(gradient_from),
        hex_to_rgb_str(gradient_to),
        n_non_top if n_non_top > 1 else 2,
        colortype="rgb"
    )

    colors = []
    gi = 0
    for i in range(len(vals)):
        if i == max_idx:
            colors.append(top_color)
        else:
            colors.append(grad_colors[min(gi, len(grad_colors) - 1)])
            gi += 1
    return colors


# -----------------------------
# 메인 화면
# -----------------------------
st.title("🌍 국가별 MBTI 비율 시각화")
st.markdown("""
전 세계 **각 국가의 MBTI 16유형 비율**을 시각화합니다.  
- 선택한 국가의 MBTI 분포를 막대그래프로 표시합니다.  
- **1등은 핑크색**, 나머지는 **연두 → 초록 그라데이션**으로 보여줍니다.
""")

# 데이터 로드
df, mbti_cols = load_data()

# -----------------------------
# 사이드바 설정
# -----------------------------
with st.sidebar:
    st.header("⚙️ 설정")
    selected_country = st.selectbox("국가 선택", sorted(df["Country"].unique()))
    st.markdown("---")
    st.subheader("🎨 색상 설정")
    top_color = st.color_picker("1등 색상", "#FF69B4")
    grad_from = st.color_picker("그라데이션 시작 (연두)", "#E6F9D5")
    grad_to = st.color_picker("그라데이션 끝 (초록)", "#4CAF50")
    st.markdown("---")
    st.info("※ CSV 파일은 루트 폴더에 있어야 합니다 (`countriesMBTI_16types.csv`).")

# -----------------------------
# 데이터 선택
# -----------------------------
row = df[df["Country"] == selected_country]
values = row[mbti_cols].iloc[0].tolist()
colors = make_colors(values, top_color=top_color, gradient_from=grad_from, gradient_to=grad_to)

# -----------------------------
# Plotly 그래프
# -----------------------------
fig = go.Figure(
    go.Bar(
        x=mbti_cols,
        y=values,
        marker_color=colors,
        hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>"
    )
)

fig.update_layout(
    title=f"🇨🇴 {selected_country} MBTI 유형 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    yaxis_tickformat="%",
    template="simple_white",
    height=550,
    margin=dict(l=40, r=40, t=80, b=40)
)

# 1등 표시
top_idx = int(pd.Series(values).idxmax())
top_label = mbti_cols[top_idx]
top_value = values[top_idx]
fig.add_annotation(
    x=top_label,
    y=top_value,
    text=f"🏆 {top_label} ({top_value:.2%})",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color="black", size=13, bold=True)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 데이터 미리보기 및 다운로드
# -----------------------------
st.markdown("---")
st.subheader("📋 선택한 국가 데이터 미리보기")
st.dataframe(row.set_index("Country").T)

csv_bytes = row.to_csv(index=False).encode("utf-8")
st.download_button(
    label="💾 CSV 다운로드",
    data=csv_bytes,
    file_name=f"{selected_country}_MBTI.csv",
    mime="text/csv"
)

st.success("✅ 시각화 완료! 사이드바에서 국가와 색상을 바꿔보세요 🎨")

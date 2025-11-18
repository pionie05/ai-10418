import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------------------------------
# 1) 페이지 기본 설정
# -------------------------------------------------------
st.set_page_config(page_title="지하철 혼잡도 분석", layout="wide")

st.title("🚇 2025년 11월 서울 지하철 혼잡도 분석")
st.write("날짜와 호선을 선택하면 승차+하차 인원이 가장 많은 역 순서로 시각화됩니다.")


# -------------------------------------------------------
# 2) CSV 불러오기 (파일은 루트 폴더에 존재)
# -------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("subway.csv", encoding="cp949")

df = load_data()

# 날짜 컬럼이 int라면 문자열로 변환
df["사용일자"] = df["사용일자"].astype(str)


# -------------------------------------------------------
# 3) 날짜 및 노선 선택 UI
# -------------------------------------------------------
available_dates = sorted([d for d in df["사용일자"].unique() if d.startswith("202511")])
selected_date = st.selectbox("📅 날짜 선택 (2025년 11월)", available_dates)

available_lines = sorted(df["노선명"].unique())
selected_line = st.selectbox("🚇 호선 선택", available_lines)


# -------------------------------------------------------
# 4) 데이터 필터링
# -------------------------------------------------------
filtered = df[(df["사용일자"] == selected_date) & (df["노선명"] == selected_line)].copy()

# 승차+하차 총합
filtered["총승객수"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승객수", ascending=False)

st.subheader(f"📊 {selected_date} | {selected_line} 승하차 합계 순위 TOP 역")


# -------------------------------------------------------
# 5) 색상 설정 (1등 핑크, 나머지는 노랑 → 오른쪽으로 갈수록 밝아지는 그라데이션)
# -------------------------------------------------------
colors = []

if len(filtered) > 0:
    # 1등은 핑크
    colors.append("#ff4da6")

    # 나머지는 노랑 → 밝은 노랑으로 그라데이션
    yellow_base = np.array([255, 230, 0])  # 강한 노랑
    yellow_light = np.array([255, 255, 150])  # 밝은 노랑

    n = len(filtered) - 1
    if n > 0:
        for i in range(n):
            ratio = i / max(1, (n - 1))  # 0~1 스케일
            color = yellow_base * (1 - ratio) + yellow_light * ratio
            colors.append(f"rgb({int(color[0])},{int(color[1])},{int(color[2])})")

else:
    st.warning("해당 날짜와 노선의 데이터가 없습니다.")
    st.stop()


# -------------------------------------------------------
# 6) Plotly 막대차트
# -------------------------------------------------------
fig = px.bar(
    filtered,
    x="역명",
    y="총승객수",
    color=filtered.index,  # index 기반 색 적용
    color_discrete_sequence=colors,
    title=f"{selected_date} {selected_line} 승하차 총합 상위역",
)

fig.update_layout(
    xaxis_title="역명",
    yaxis_title="총 승객수",
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=20),
)


st.plotly_chart(fig, use_container_width=True)

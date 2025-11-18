import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="지하철 혼잡도 분석", layout="wide")
st.title("🚇 2025년 11월 서울 지하철 혼잡도 분석")
st.write("날짜와 호선을 선택하면 승차+하차 인원이 가장 많은 역 순서로 시각화됩니다.")

@st.cache_data
def load_data():
    # 파일은 루트 폴더에 있다고 가정
    df = pd.read_csv("subway.csv", encoding="cp949")
    # 안전하게 문자열로 변환 후 datetime으로 파싱
    df["사용일자_str"] = df["사용일자"].astype(str).str.strip()
    df["사용일자_dt"] = pd.to_datetime(df["사용일자_str"], format="%Y%m%d", errors="coerce")
    # 일부 파일이 'YYYY-MM-DD' 같은 형식일 수 있으니 추가 파싱 시도
    mask_na = df["사용일자_dt"].isna()
    if mask_na.any():
        df.loc[mask_na, "사용일자_dt"] = pd.to_datetime(df.loc[mask_na, "사용일자_str"], errors="coerce")
    return df

df = load_data()

# 2025년 11월 날짜들 추출 (있으면)
dates_202511 = df.loc[
    (df["사용일자_dt"].notna()) & 
    (df["사용일자_dt"].dt.year == 2025) & 
    (df["사용일자_dt"].dt.month == 11),
    "사용일자_dt"
].dt.strftime("%Y-%m-%d").sort_values().unique().tolist()

# 만약 2025-11 데이터가 없으면 파일에 있는 다른 이용 가능한 '년-월'을 보여주기
if len(dates_202511) > 0:
    selected_date = st.selectbox("📅 날짜 선택 (2025년 11월)", dates_202511)
else:
    st.warning("데이터에 2025년 11월 날짜가 없습니다. 파일에 있는 이용 가능한 날짜(년-월)로 대체합니다.")
    available_months = (
        df.loc[df["사용일자_dt"].notna(), "사용일자_dt"]
        .dt.to_period("M")
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )
    if len(available_months) == 0:
        st.error("사용 가능한 날짜가 전혀 없습니다. CSV의 '사용일자' 컬럼을 확인해 주세요.")
        st.stop()
    # 사용자가 선택할 수 있게 하되, 기본값은 가장 최신 월
    chosen_month = st.selectbox("📅 사용 가능한 연-월 선택", available_months, index=len(available_months)-1)
    # 그 월에서 날짜들만 추출
    dates_in_month = df.loc[
        df["사용일자_dt"].notna() & (df["사용일자_dt"].dt.to_period("M").astype(str) == chosen_month),
        "사용일자_dt"
    ].dt.strftime("%Y-%m-%d").sort_values().unique().tolist()
    if len(dates_in_month) == 0:
        st.error("선택된 월에 사용할 수 있는 날짜가 없습니다.")
        st.stop()
    selected_date = st.selectbox("📅 날짜 선택 (해당 월)", dates_in_month)

# 노선 선택
available_lines = sorted(df["노선명"].dropna().unique().tolist())
if len(available_lines) == 0:
    st.error("CSV에 '노선명' 데이터가 없습니다.")
    st.stop()
selected_line = st.selectbox("🚇 호선 선택", available_lines)

# 필터링
# selected_date은 'YYYY-MM-DD' 형식 (문제가 생길 수 있으므로 다시 파싱)
selected_dt = pd.to_datetime(selected_date)
filtered = df[(df["사용일자_dt"] == selected_dt) & (df["노선명"] == selected_line)].copy()

if filtered.empty:
    st.warning("선택한 날짜와 노선에 해당하는 데이터가 없습니다.")
    st.stop()

# 합계 계산 및 정렬
filtered["총승객수"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승객수", ascending=False).reset_index(drop=True)

st.subheader(f"📊 {selected_date} | {selected_line} 승하차 합계 순위")

# 색상: 1등 핑크, 나머지 노랑->밝은 노랑 그라데이션
n_bars = len(filtered)
colors = []
if n_bars >= 1:
    colors.append("#ff4da6")  # 1등 핑크
if n_bars > 1:
    yellow_base = np.array([255, 230, 0])
    yellow_light = np.array([255, 255, 150])
    n = n_bars - 1
    for i in range(n):
        ratio = i / max(1, n - 1)
        color = yellow_base * (1 - ratio) + yellow_light * ratio
        colors.append(f"rgb({int(color[0])},{int(color[1])},{int(color[2])})")

# Plotly 그리기 - color="역명"으로 하면 막대 개수에 맞게 색을 할당
fig = px.bar(
    filtered,
    x="역명",
    y="총승객수",
    color="역명",
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

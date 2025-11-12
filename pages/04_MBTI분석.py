# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import n_colors
from functools import lru_cache

st.set_page_config(page_title="Country MBTI Rates", layout="wide")

# -------------------------
# 유틸: 데이터 로드
# -------------------------
@st.cache_data
def load_data(path="countriesMBTI_16types.csv"):
    df = pd.read_csv(path)
    # 보장: Country 컬럼 문자열, 나머지 숫자
    df['Country'] = df['Country'].astype(str)
    # MBTI 컬럼 순서: 파일의 순서를 따르거나 명시적으로 정렬
    mbti_cols = [c for c in df.columns if c != "Country"]
    return df, mbti_cols

# -------------------------
# 유틸: 색상 생성
# 1등은 핑크(#FF69B4), 나머지는 연두-녹색 그라데이션
# -------------------------
def make_colors(values, top_color="#FF69B4", gradient_from="#E6F9D5", gradient_to="#4CAF50"):
    """
    values: list/array of numeric values in the same order as bars
    returns: list of hex colors same length
    """
    # 안전: copy
    vals = list(values)
    # find index(es) of top value(s) — tie가 생기면 첫번째를 top으로 사용
    max_idx = int(pd.Series(vals).idxmax())

    # generate gradient colors for non-top bars
    n_non_top = max(0, len(vals) - 1)
    if n_non_top > 0:
        grad_colors = n_colors(gradient_from, gradient_to, n_non_top, colortype="rgb")
    else:
        grad_colors = []

    colors = []
    gi = 0
    for i in range(len(vals)):
        if i == max_idx:
            colors.append(top_color)
        else:
            colors.append(grad_colors[gi])
            gi += 1
    return colors

# -------------------------
# 데이터 로드 시도
# -------------------------
st.title("🌍 국가별 MBTI 비율 시각화 (Interactive)")
st.markdown(
    """
    - 왼쪽에서 국가를 선택하면 해당 국가의 MBTI 16유형 비율을 인터랙티브한 막대그래프로 보여줍니다.
    - 1등 유형은 핑크색, 나머지는 연두~녹색 그라데이션으로 표시됩니다.
    """
)

# 사이드바: 파일설명 및 선택
with st.sidebar:
    st.header("설정")
    st.markdown("CSV 파일: `countriesMBTI_16types.csv` (앱과 같은 폴더에 위치해야 함)")
    st.markdown("데이터 컬럼: `Country` + 16개의 MBTI 유형")
    uploaded = st.file_uploader("CSV 파일 업로드 (선택)", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        mbti_cols = [c for c in df.columns if c != "Country"]
    else:
        try:
            df, mbti_cols = load_data()
        except FileNotFoundError:
            st.error("앱 폴더에 'countriesMBTI_16types.csv' 파일이 없습니다. 사이드바에서 파일을 업로드하거나 파일을 앱 폴더에 올려주세요.")
            st.stop()

    st.markdown("---")
    st.markdown("그래프 색상 설정:")
    top_color = st.color_picker("1등 색상 (핑크 기본)", "#FF69B4")
    grad_from = st.color_picker("그라데이션 시작(연두 밝음)", "#E6F9D5")
    grad_to = st.color_picker("그라데이션 끝(녹색 진함)", "#4CAF50")
    st.markdown("---")
    st.caption("※ 업로드한 파일이 있으면 우선 사용됩니다.")

# -------------------------
# 메인: 국가 선택
# -------------------------
countries = df["Country"].sort_values().tolist()
default_country = countries[0] if countries else None
selected = st.selectbox("국가 선택", countries, index=countries.index(default_country) if default_country else 0)

# 선택 국가의 데이터 가져오기
row = df[df["Country"] == selected]
if row.empty:
    st.error(f"선택한 국가({selected})의 데이터가 없습니다.")
    st.stop()

# MBTI 값 정리: 순서 고정 (mbti_cols)
values = row[mbti_cols].iloc[0].astype(float).tolist()
labels = mbti_cols.copy()

# 색상 생성 (top color + gradient)
colors = make_colors(values, top_color=top_color, gradient_from=grad_from, gradient_to=grad_to)

# Plotly 막대그래프
fig = go.Figure(
    go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>"
    )
)

fig.update_layout(
    title=f"{selected} — MBTI 16유형 비율",
    xaxis_title="MBTI 유형",
    yaxis_tickformat="%",
    yaxis_title="비율",
    template="simple_white",
    margin=dict(l=40, r=20, t=80, b=40),
    height=520
)

# 강조: top label annotation
top_idx = int(pd.Series(values).idxmax())
top_label = labels[top_idx]
top_value = values[top_idx]
fig.add_annotation(
    x=top_label,
    y=top_value,
    text=f"Top: {top_label} ({top_value:.2%})",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# 추가: 데이터 테이블 / 다운로드
# -------------------------
st.markdown("---")
st.subheader("데이터 미리보기 & 다운로드")
st.dataframe(row.reset_index(drop=True).T.rename(columns={0: selected}))

csv_bytes = row.to_csv(index=False).encode('utf-8')
st.download_button("선택 국가 데이터 CSV 다운로드", data=csv_bytes, file_name=f"{selected}_MBTI.csv", mime="text/csv")

# -------------------------
# 간단한 설명 섹션 (리콰이어먼트)
# -------------------------
st.markdown("---")
st.header("리콰이어먼트 (Requirements)")
st.markdown(
    """
    1. 이 앱은 `countriesMBTI_16types.csv` 파일(앱과 동일 폴더 또는 업로드된 파일)을 읽습니다.  
    2. CSV는 첫 번째 컬럼에 `Country`라는 국가명 컬럼이 있어야 하며, 그 외 16개 컬럼은 MBTI 유형(INFJ, ISFJ, INTP, ...)이어야 합니다.  
    3. Streamlit Cloud에서 작동하게 작성되었습니다. 로컬에서 실행 시 `streamlit run app.py`로 실행하세요.
    """
)

st.markdown("**CSV 샘플 헤더 예시:**\n```\nCountry,INFJ,ISFJ,INTP,ISFP,ENTP,INFP,ENTJ,ISTP,INTJ,ESFP,ESTJ,ENFP,ESTP,ISTJ,ENFJ,ESFJ\n```")
st.success("완료! 국가를 선택해서 MBTI 막대그래프를 확인하세요. 🙂")

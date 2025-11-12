# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Country MBTI Explorer", layout="wide")

@st.cache_data
def load_data(path: str = "countriesMBTI_16types.csv") -> pd.DataFrame:
    """데이터 로드. 파일이 앱과 같은 디렉토리에 있다고 가정합니다.
    (Streamlit Cloud에 배포할 때 이 CSV를 같은 repo에 올리면 됩니다.)"""
    p = Path(path)
    if not p.exists():
        st.error(f"데이터 파일이 없습니다: {path}\n앱과 같은 폴더에 'countriesMBTI_16types.csv'를 올려주세요.")
        return pd.DataFrame()
    df = pd.read_csv(p)
    # 국가명 정리
    df = df.rename(columns=lambda c: c.strip())
    return df

def make_color_list(values: pd.Series, first_color: str = "#FF66B2",
                    grad_start: str = "#e6ffcc", grad_end: str = "#7bd24a") -> list:
    """첫 번째(최대값) 막대는 pink, 나머지는 연두 그라데이션으로 생성.
    values는 막대의 값 시퀀스(예: MBTI 비율) — 색 길이는 values 길이와 같아야 함.
    grad_start/grad_end는 연두 그라데이션의 양끝색 (헥스)"""
    n = len(values)
    if n == 0:
        return []
    # 1등 인덱스(최대값) 찾기 - 만약 동률이면 첫 번째 발생을 1등으로 처리
    max_idx = int(np.argmax(values.values))
    # gradient for the others (n-1 colors)
    def hex_to_rgb(hexc):
        he=hexc.lstrip("#")
        return tuple(int(he[i:i+2],16) for i in (0,2,4))
    def rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*[int(round(x)) for x in rgb])
    start_rgb, end_rgb = hex_to_rgb(grad_start), hex_to_rgb(grad_end)
    grads = []
    others_count = n - 1
    if others_count > 0:
        for i in range(others_count):
            t = i / max(1, others_count - 1)  # 0..1
            rgb = tuple(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * t for j in range(3))
            grads.append(rgb_to_hex(rgb))
    # assemble final list
    colors = []
    j = 0
    for i in range(n):
        if i == max_idx:
            colors.append(first_color)
        else:
            colors.append(grads[j])
            j += 1
    return colors

def plot_country_mbti(df: pd.DataFrame, country: str):
    if country not in df['Country'].values:
        st.error(f"'{country}' 데이터를 찾을 수 없습니다.")
        return
    row = df[df['Country'] == country].iloc[0]
    # MBTI columns (exclude Country)
    mbti_cols = [c for c in df.columns if c != "Country"]
    values = row[mbti_cols].astype(float)
    plot_df = pd.DataFrame({"MBTI": mbti_cols, "Ratio": values.values})
    # Sort descending so 1st appears left (optional). But to keep original order (16 types) you can remove sort.
    plot_df = plot_df.sort_values("Ratio", ascending=False).reset_index(drop=True)

    # colors: first one pink, others gradient green
    colors = make_color_list(plot_df["Ratio"], first_color="#FF66B2", grad_start="#e6ffcc", grad_end="#7bd24a")

    fig = px.bar(
        plot_df,
        x="MBTI",
        y="Ratio",
        text=plot_df["Ratio"].apply(lambda v: f"{v:.3f}"),
        labels={"Ratio": "비율", "MBTI": "MBTI 유형"},
        height=520,
    )
    fig.update_traces(marker_color=colors, marker_line_color="rgba(0,0,0,0.0)", textposition="outside", hovertemplate="<b>%{x}</b><br>비율: %{y:.4f}<extra></extra>")
    fig.update_layout(
        title=f"{country} — MBTI 비율",
        yaxis=dict(tickformat=".3f", title="비율"),
        xaxis=dict(title="MBTI 유형"),
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin=dict(l=40,r=20,t=70,b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

def sidebar_controls(df: pd.DataFrame):
    st.sidebar.header("컨트롤")
    countries = sorted(df['Country'].tolist())
    country = st.sidebar.selectbox("국가 선택", countries, index=0)
    sort_display = st.sidebar.checkbox("결과를 내림차순 정렬(1등부터)", value=True)
    show_table = st.sidebar.checkbox("원데이터 표 보기", value=False)
    return country, sort_display, show_table

def show_top3(df: pd.DataFrame, country: str):
    row = df[df['Country'] == country].iloc[0]
    mbti_cols = [c for c in df.columns if c != "Country"]
    values = row[mbti_cols].astype(float)
    top3 = values.sort_values(ascending=False).head(3)
    st.markdown("### Top 3 MBTI")
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    emojis = ["🥇","🥈","🥉"]
    for i, (typ, val) in enumerate(top3.items()):
        with cols[i]:
            st.metric(label=f"{emojis[i]} {typ}", value=f"{val:.3f}")

# --- Main app ---
def main():
    st.title("🌍 Country MBTI Explorer")
    st.write("국가를 선택하면 그 국가의 MBTI 16유형 비율을 인터랙티브한 막대그래프로 보여줍니다.")
    st.caption("그래프 색상: 1등은 핑크(#FF66B2), 나머지는 연두 그라데이션입니다.")

    df = load_data()
    if df.empty:
        return

    country, sort_display, show_table = sidebar_controls(df)

    # 그래프
    if sort_display:
        # plot_country_mbti internally sorts descending; to preserve the option, call accordingly.
        plot_country_mbti(df, country)
    else:
        # If not sorting, construct plot without sorting — we want original column order left-to-right.
        row = df[df['Country'] == country].iloc[0]
        mbti_cols = [c for c in df.columns if c != "Country"]
        values = row[mbti_cols].astype(float)
        plot_df = pd.DataFrame({"MBTI": mbti_cols, "Ratio": values.values})
        # colors: find max index
        colors = make_color_list(plot_df["Ratio"], first_color="#FF66B2", grad_start="#e6ffcc", grad_end="#7bd24a")
        fig = px.bar(plot_df, x="MBTI", y="Ratio", text=plot_df["Ratio"].apply(lambda v: f"{v:.3f}"))
        fig.update_traces(marker_color=colors, textposition="outside", hovertemplate="<b>%{x}</b><br>비율: %{y:.4f}<extra></extra>")
        fig.update_layout(title=f"{country} — MBTI 비율 (원래 순서)", yaxis=dict(tickformat=".3f"), margin=dict(l=40,r=20,t=70,b=40))
        st.plotly_chart(fig, use_container_width=True)

    # Top3
    show_top3(df, country)

    # 원데이터 보기
    if show_table:
        st.markdown("### 원본 데이터 (해당 국가 행 강조)")
        st.dataframe(df.style.highlight_max(axis=1, subset=[c for c in df.columns if c!="Country"]), height=420)

    # 하단 설명
    st.markdown("---")
    st.markdown("""
    **사용법**
    1. 좌측 사이드바에서 국가를 선택하세요.  
    2. `결과를 내림차순 정렬(1등부터)` 체크박스를 통해 막대 정렬 여부 선택 가능.  
    3. `원데이터 표 보기`를 체크하면 전체 데이터표를 볼 수 있습니다.

    **배포 팁 (Streamlit Cloud)**
    - 이 `app.py`와 `countriesMBTI_16types.csv`, `requirements.txt`를 같은 GitHub 레포지토리에 올리고, Streamlit Cloud와 연동하면 자동 배포됩니다.
    """)

if __name__ == "__main__":
    main()

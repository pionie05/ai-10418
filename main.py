import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력하세요')
b=st.selectbox('좋아하는 음식을 선택하새요',['마카롱','케이크','딸기모찌'])
if st.button('인삿말 생성'):
  st.info(a+'안녕하긔')
  st.warning(b+' 맛있갯다..,,')
  st.error('반갑워')
  st.balloons()

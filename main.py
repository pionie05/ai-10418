import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력하세요')
st.selectbox('좋아하는 음식을 선택하새요',['마카롱','케이크',딸기모찌'])
if st.button('인삿말 생성'):
  st.write(a+'님, 안녕하세요 반갑습니다')

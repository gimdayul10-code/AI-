import streamlit as st
st.title('나의 첫 웹 페이지 만들기')
st.text_input('이름을 입력해주세요')
st.selectbox('좋아하는 음식을 선택해주세요',['마라탕','엽떡','불닭','닭갈비'])
st.button('인삿말 생성')

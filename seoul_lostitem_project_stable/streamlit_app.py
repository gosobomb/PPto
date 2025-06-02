
import streamlit as st
import pickle
import pandas as pd

@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()
st.title("서울시 분실물 보관장소 예측 대시보드")
st.header("입력 정보")

lost_id = st.number_input("분실물 ID", value=12345)
status = st.number_input("분실 상태", value=1)
reg_date = st.number_input("등록일자 (초 단위 Timestamp)", value=1672531200)
rcv_date = st.number_input("수령일자 (초 단위 Timestamp)", value=1672617600)
details = st.number_input("상세 내용", value=0)
registrant_id = st.number_input("등록자 ID", value=1234)
item_name = st.number_input("품목명 인코딩", value=5)
item_type = st.number_input("품목종류 인코딩", value=3)
receive_place = st.number_input("수령장소 인코딩", value=2)
view_count = st.number_input("조회수", value=100)

if st.button("보관장소 예측하기"):
    input_data = pd.DataFrame([{
        'lost_id': lost_id,
        'status': status,
        'reg_date': reg_date,
        'rcv_date': rcv_date,
        'details': details,
        'registrant_id': registrant_id,
        'item_name': item_name,
        'item_type': item_type,
        'receive_place': receive_place,
        'view_count': view_count
    }])
    prediction = model.predict(input_data)
    st.success(f"예측된 보관장소 인덱스: {prediction[0]}")

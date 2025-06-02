
import streamlit as st
import pickle
import pandas as pd
import os

if not os.path.exists('model.pkl'):
    from modules import data_collection, preprocessing, feature_selection, model_training, model_evaluation

    st.info("모델이 존재하지 않아 새로 학습을 시작합니다.")

    df_raw = data_collection.load_data_from_api("4b556375586e756e34365179614251", batch_size=1000, delay=0.05)
    df_cleansed = preprocessing.preprocess_data(df_raw)
    train_input, test_input, train_target, test_target = feature_selection.feature_split(df_cleansed)
    model = model_training.train_model(train_input, train_target)
    test_pred = model.predict(test_input)
    metrics = model_evaluation.evaluate_model(test_target, test_pred)
    st.write("모델 평가 결과:", metrics)

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    st.success("모델 저장 완료")
else:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

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

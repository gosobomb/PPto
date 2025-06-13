import streamlit as st
import pickle
import pandas as pd
import os
from datetime import datetime
from functools import lru_cache

from modules import data_collection, preprocessing, feature_selection, model_training, model_evaluation

MODEL_PATH = 'model.pkl'
ENCODER_PATH = 'label_encoders.pkl'

# 1. 모델과 라벨 인코더 불러오기 또는 생성
@st.cache_resource(show_spinner="모델 로딩 중...", max_entries=1)
def load_model_and_encoders():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        st.info("모델이 존재하지 않아 새로 학습을 시작합니다.")
        df_raw = data_collection.load_data_from_api("4b556375586e756e34365179614251", batch_size=1000, delay=0.05)
        df_cleansed = preprocessing.preprocess_data(df_raw)

        # 학습에 사용할 모든 feature 선택
        selected_columns = [
            'item_type', 'reg_date', 'receive_place',
            'status', 'view_count', 'item_name', 'registrant_id',
            'storage_location'  # 타겟
        ]
        df_filtered = df_cleansed[selected_columns].copy()

        train_input, test_input, train_target, test_target = feature_selection.feature_split(
            df_filtered, target_column='storage_location'
        )
        model = model_training.train_model(train_input, train_target)
        test_pred = model.predict(test_input)
        metrics = model_evaluation.evaluate_model(test_target, test_pred)
        st.write("모델 평가 결과:", metrics)

        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)

        st.success("모델 저장 완료")

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(ENCODER_PATH, 'rb') as f:
        label_encoders = pickle.load(f)
    return model, label_encoders

# 모델과 인코더 캐시 로딩
model, label_encoders = load_model_and_encoders()

# 2. 대시보드 UI
st.title("📦 서울시 분실물 보관장소 예측 시스템")
st.markdown("필요한 정보를 입력하면, **예상 보관장소**를 예측합니다.")

# 인코딩된 컬럼 역변환 (사용자용 선택지)
item_type_options = list(label_encoders['item_type'].classes_) if 'item_type' in label_encoders else []
receive_place_options = list(label_encoders['receive_place'].classes_) if 'receive_place' in label_encoders else []
storage_location_options = list(label_encoders['storage_location'].classes_) if 'storage_location' in label_encoders else []

item_type = st.selectbox("품목종류", item_type_options)
reg_date = st.date_input("등록일자", value=datetime.today())
receive_place = st.selectbox("수령장소", receive_place_options)

if st.button("📍 보관장소 예측하기"):
    reg_date_ts = pd.Timestamp(reg_date).timestamp()

    # 사용자 입력 변수를 인코딩
    input_dict = {
        'item_type': label_encoders['item_type'].transform([item_type])[0],
        'reg_date': reg_date_ts,
        'receive_place': label_encoders['receive_place'].transform([receive_place])[0],
    }

    # 추가 feature는 평균 또는 더미값 사용
    input_dict['status'] = 1  # 예: 일반 상태
    input_dict['view_count'] = 50  # 평균적 조회수
    input_dict['item_name'] = 0  # 대표 값 또는 가장 빈도 높은 값
    input_dict['registrant_id'] = 1000  # 임의의 중립값

    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)[0]

    # 결과 복호화 (storage_location으로 해석)
    if 'storage_location' in label_encoders:
        inv_label = label_encoders['storage_location'].inverse_transform([prediction])[0]
        st.success(f"예측된 보관장소는: **{inv_label}** 입니다.")
    else:
        st.success(f"예측된 보관장소 인덱스: **{prediction}** 입니다.")
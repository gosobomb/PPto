
from modules import load_raw_data, preprocess_data, select_features_and_split, train_model, evaluate_model
import pickle

def main():
    df_raw = load_raw_data.load_raw_data()
    df_cleansed = preprocess_data.preprocess_data(df_raw)
    train_input, test_input, train_target, test_target = select_features_and_split.select_features_and_split(df_cleansed)
    model = train_model.train_model(train_input, train_target)
    test_pred = model.predict(test_input)
    metrics = evaluate_model.evaluate_model(test_target, test_pred)
    print("모델 평가 결과:", metrics)

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("모델 저장 완료: model.pkl")

if __name__ == "__main__":
    main()

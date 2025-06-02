
from modules import data_collection, preprocessing, data_check, feature_selection, model_training
from modules import model_prediction, model_evaluation, model_decision, model_improvement, visualization

def main():
    api_key = "4b556375586e756e34365179614251"
    df = data_collection.load_data_from_api(api_key)
    df = preprocessing.preprocess_data(df)
    if not data_check.check_data_sufficiency(df):
        print("데이터량 부족")
        return
    X_train, X_test, y_train, y_test = feature_selection.feature_split(df, target_column='storage')
    model = model_training.train_model(X_train, y_train)
    predictions = model_prediction.predict_model(model, X_test)
    metrics = model_evaluation.evaluate_model(y_test, predictions)
    print("평가 결과:", metrics)
    if not model_decision.is_model_passed(metrics):
        print("모델 개선 수행")
        model = model_improvement.improve_model(X_train, y_train)
        predictions = model_prediction.predict_model(model, X_test)
        metrics = model_evaluation.evaluate_model(y_test, predictions)
        print("개선 결과:", metrics)
    visualization.plot_feature_importances(model, X_train.columns)

if __name__ == "__main__":
    main()

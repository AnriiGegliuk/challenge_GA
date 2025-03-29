import os
import joblib
import argparse
import lightgbm as lgbm
from sklearn.model_selection import train_test_split
from data_processing import load_data, feature_engineering, encode_features

def train_and_save_model(train_csv: str, model_path: str):
    df = load_data(train_csv) # loading data

    # extract target + drop from features
    y = df["Survived"]
    X = df.drop("Survived", axis=1)

    X = feature_engineering(X) # feature engineering according to src/titanic/data_processing.py

    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # encoding features
    X_train = encode_features(X_train)
    X_test = encode_features(X_test)


    model = lgbm.LGBMClassifier(objective="binary",        # creating  and train LightGBM model
                    num_leaves=20,
                    learning_rate=0.01,
                    n_estimators=400,
                    random_state=42)

    model.fit(X_train, y_train,                            # training model
            eval_set=[(X_train, y_train), (X_test, y_test)],
            eval_names=["train", "val"],
            eval_metric="binary_logloss",
            callbacks=[lgbm.early_stopping(stopping_rounds=10)])

    os.makedirs(os.path.dirname(model_path), exist_ok=True) # saving model to dir and check if dir exist or not
    joblib.dump(model, model_path)
    print(f"model is saved to defined path: {model_path}")
    # TODO: report with metrix and png of learning curves

if __name__ == "__main__": # will use argparse since it is convinient to train models using CLI maybe will create makefile? #TODO: come back to this after finishing API
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_csv", type=str, required=True)
    parser.add_argument("--model_path", type=str, required=True)
    args = parser.parse_args()

    train_and_save_model(args.train_csv, args.model_path)


# to run this script: uv run src/titanic/train.py --train_csv "data/train.csv" --model_path "models/model.joblib"

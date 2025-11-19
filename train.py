import pandas as pd
import pickle
import sys

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(dataset_path=Path("data/abalone.data")):
    base_dir = Path(".")
    fpath = base_dir / dataset_path

    if not str(fpath.resolve()).startswith(str(base_dir.resolve())):
        raise ValueError("Access outside of project directory is not allowed")

    variables = [
        "Sex",
        "Length",
        "Diameter",
        "Height",
        "Whole_weight",
        "Shucked_weight",
        "Viscera_weight",
        "Shell_weight",
        "Rings",
    ]
    dtypes = [
        "object",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "int64",
    ]

    features = variables[0:-1]
    target = variables[-1]

    if fpath.exists():
        data = pd.read_csv(
            dataset_path,
            names=variables,
            dtype={feature: dtype for feature, dtype in zip(variables, dtypes)},
        )
    else:
        try:
            from ucimlrepo import fetch_ucirepo

            # fetch dataset
            abalone = fetch_ucirepo(id=1)
            # extract data
            data = pd.concat([abalone.data.features, abalone.data.targets], axis=1)

            # TODO: save the `data` variable to disk in the same format as `abalone.data`
        except ModuleNotFoundError:
            print(
                "Please install the `fetch_ucirepo` Python package to get the dataset."
            )
            print(
                "If you do have the dataset, store 'abalone.data' in './data/' and try again"
            )
            sys.exit(1)
        except ConnectionError:
            print(
                "Error connecting to server. Check your internet connection and try again"
            )
            sys.exit(1)

    cat_idx, num_idx = [0], list(range(1, len(features)))

    return data, features, target, cat_idx, num_idx, dtypes


def train_sklearn(X_train, X_test, y_train, y_test, pipeline, model_params):
    model_name = pipeline.steps[-1][0]
    pipeline.set_params(
        **{f"{model_name}__{param}": value for param, value in model_params.items()}
    )
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    model_rmse = root_mean_squared_error(y_test, y_pred)
    model_mae = mean_absolute_error(y_test, y_pred)
    return model_rmse, model_mae


def train(data, features, target, cat_idx, num_idx, test_size=20):
    hyperparam_1 = "max_depth"
    hyperparam_2 = "min_samples_leaf"
    hyperparam_3 = "n_estimators"
    hyperparams = [hyperparam_1, hyperparam_2, hyperparam_3]
    hyperparam_1_2_3_best = [6, 10, 130]
    best_hyperparams = {
        hyperparam: value
        for hyperparam, value in zip(hyperparams, hyperparam_1_2_3_best)
    }

    preprocess_features = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first"), cat_idx),
            ("num", StandardScaler(), num_idx),
        ]
    )
    pipeline = Pipeline(
        steps=[("preprocess", preprocess_features), ("model", RandomForestRegressor())]
    )

    X_full_train, X_test, y_full_train, y_test = train_test_split(
        data[features].to_numpy(), data[target].to_numpy(), test_size=test_size / 100
    )

    rmse, mae = train_sklearn(
        X_full_train,
        X_test,
        y_full_train,
        y_test,
        pipeline,
        best_hyperparams,
    )

    return pipeline, rmse, mae


def save_pipeline(pipeline, output_file):
    base_dir = Path(".")
    fpath = base_dir / output_file

    if not str(fpath.resolve()).startswith(str(base_dir.resolve())):
        raise ValueError("Access outside of project directory is not allowed")

    if not fpath.exists():
        fpath.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "wb") as f_out:
        pickle.dump(pipeline, f_out)


if __name__ == "__main__":
    sklearn_pipeline_path = Path("assets/sklearn_pipeline.bin")

    print("Loading the dataset...")
    data, features, target, cat_idx, num_idx, dtypes = load_data()

    print("Training the model...")
    pipeline, rmse, mae = train(data, features, target, cat_idx, num_idx, test_size=20)
    print(f"-> testing RMSE = {rmse:.2f}")
    print(f"-> testing MAE  = {mae:.2f}")

    print(f"Saving the model's pipeline to '{sklearn_pipeline_path}'...")
    save_pipeline(pipeline, sklearn_pipeline_path)

    print("Program exited succesfully")

import pickle

from pathlib import Path


def load_pipeline(sklearn_pipeline_path=Path("assets/sklearn_pipeline.bin")):
    base_dir = Path(".")
    fpath = base_dir / sklearn_pipeline_path

    if not str(fpath.resolve()).startswith(str(base_dir.resolve())):
        raise ValueError("Access outside of project directory is not allowed")

    if not fpath.exists():
        raise FileNotFoundError(f"Pipeline file not found in '{sklearn_pipeline_path}'")

    with open(fpath, "rb") as f_in:
        pipeline = pickle.load(f_in)

    return pipeline


def predict(X, pipeline):
    y_pred = pipeline.predict(X)
    return list(map(float, y_pred))


if __name__ == "__main__":
    sklearn_pipeline_path = Path("assets/sklearn_pipeline.bin")

    print(f"Loading the pipeline file from '{sklearn_pipeline_path}'")
    pipeline = load_pipeline(sklearn_pipeline_path)

    X = [["M", 0.455, 0.365, 0.095, 0.514, 0.2245, 0.101, 0.15]]
    print("Predicting values")
    y_pred = predict(X, pipeline)
    if len(y_pred) == 1:
        print(f"The prediction is {y_pred[0]}")
    else:
        print(f"The predictions are {y_pred}")

    print("Program exited succesfully")

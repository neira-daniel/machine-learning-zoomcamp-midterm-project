import argparse
import json
import requests


def make_request(url, payload):
    response = requests.post(url, json=payload)
    predictions = response.json()
    return predictions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url",
        nargs="?",
        default="http://localhost:9696/predict",
        help="URL (endpoint) of the service to query",
    )
    parser.add_argument(
        "--matrix",
        type=json.loads,
        nargs="?",
        default='[["M", 0.455, 0.365, 0.095, 0.514, 0.2245, 0.101, 0.15]]',
        help="JSON-encoded data for the query",
    )
    args = parser.parse_args()

    payload = {"data": args.matrix}

    y_pred = make_request(args.url, payload)

    if len(y_pred) == 1:
        print(f"The prediction is {y_pred[0]}")
    else:
        print(f"The predictions are {y_pred}")

    print("Program exited succesfully")

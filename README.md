# Machine Learning Zoomcamp 2025: Midterm project

Repository of the artifacts that implement the midterm project of Machine Learning Zoomcamp (2025 cohort).

## Project formalities

- [Evaluation criteria](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/1b271a2e36ce1d79b6da55db9565af738a1426b1/projects#evaluation-criteria)
- [Deliverables](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/1b271a2e36ce1d79b6da55db9565af738a1426b1/projects#deliverables)
- [Reviewing peer projects](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/1b271a2e36ce1d79b6da55db9565af738a1426b1/projects/how-to.md#reviewing-peer-projects)
- [Project tips and checklist](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/master/projects/project-tips.md#project-tips-and-checklist)

## Dataset credits

"Abalone" is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.

W. Nash, T. Sellers, S. Talbot, A. Cawthorn, and W. Ford. "Abalone," UCI Machine Learning Repository, 1994. [Online]. Available: https://doi.org/10.24432/C55C7W.

## How to run the application

The following instructions assume the repository was cloned and that [`uv`](https://docs.astral.sh/uv/) is available.

### Using a a monolitical model

We can run `predict_local.py` to query the fitted model stored at `assets/sklearn_pipeline.bin` as follows:

```bash
uv run predict_local.py
```

This will load the model and query it using the record `[["M", 0.455, 0.365, 0.095, 0.514, 0.2245, 0.101, 0.15]]`. It will then print the resulting prediction to the terminal and exit.

### Using a client-server model

We can also serve the model at `localhost:9696/predict` using `uvicorn` and `server.py` and query it with `predict_client.py`. To do so, we run the following commands:

```bash
# run in one terminal
uv run uvicorn server:app --host 127.0.0.1 --port 9696 --reload --log-level debug
# run in another terminal
uv run predict_client.py
```

This will send the exact same query we sent using `predict_local.py`.

We can pass parameters to `predict_client.py` to specify both the endpoint where the service is running (the URL) and the data we want to send in the query.

Run the following to print the "help" to the terminal that describes how to use `predict_client.py`:

```bash
uv run predict_client.py --help
```

In particular, we pass the data using the `--matrix` flag. The format of the data should be JSON-compatible. That is, a list of lists with the strings double-quoted and the whole list within single quotes to prevent the shell from doing "word splitting" and "glob expansion".

For example, the following instruction sends two records to the prediction service that's listening on the default endpoint, `localhost:9696/predict`:

```bash
uv run predict_client.py --matrix '[["M",0.455,0.365,0.095,0.514,0.2245,0.101,0.15],["M",0.35,0.265,0.09,0.2255,0.0995,0.0485,0.07]]'
```

Finally, we stop the server pressing `CTRL-c` in the terminal where it is running.

### Using Docker

This application has a Dockerfile we can use to create a Docker image and then run it.

To create the Docker image:

```bash
docker build -t abalone-predict .
```

To run the image as a Docker container:

```bash
docker run -t --rm -p 9696:9696 abalone-predict
```

We can then query the running container using the same commands described in the section "Using a client-server model".

In case that there's a problem when mounting the image, we can open a Bash session within the container to inspect its contents and debug it running the following command:

```bash
docker run -it --entrypoint /bin/bash abalone-predict
```

# Abalone: predicting the age of abalone sea snails

## Problem statement

The procedure to determine the age of [abalone](https://en.wikipedia.org/wiki/Abalone) sea snails is invasive. As [described by the maintainers of the abalone dataset](https://archive.ics.uci.edu/dataset/1/abalone) we'll use:

> The age of abalone is determined by cutting the shell through the cone, staining it, and counting the number of rings through a microscope -- a boring and time-consuming task.

We'd like to predict the age of abalones without having to perform the described procedure on them. Quoting again the maintainers:

> Other measurements, which are easier to obtain, are used to predict the age.

This isn't necessarily simple:

> Further information, such as weather patterns and location (hence food availability) may be required to solve the problem.

But it's worth to try to prevent people having to perform the invasive procedure described to determine the age of abalones.

## Dataset description

We reproduce here the dataset information that appears both in the `abalone.names` file (included in the `abalone.zip` file when downloading it by hand) and the "Variables Table" section in the [dataset's webpage](https://archive.ics.uci.edu/dataset/1/abalone):

| Name            | Data Type   | Meas.   | Description                         |
|-----------------|-------------|---------|-------------------------------------|
| Sex             | nominal     |         | M, F, and I (infant)                |
| Length          | continuous  | mm      | Longest shell measurement           |
| Diameter        | continuous  | mm      | Perpendicular to length             |
| Height          | continuous  | mm      | With meat in shell                  |
| Whole weight    | continuous  | grams   | Whole abalone                       |
| Shucked weight  | continuous  | grams   | Weight of meat                      |
| Viscera weight  | continuous  | grams   | Gut weight (after bleeding)         |
| Shell weight    | continuous  | grams   | After being dried                   |
| Rings           | integer     |         | +1.5 gives the age in years         |

The target variable is "Rings". It contains integers whose values are meaningful. We can then try to fit either a regression or a classification model to them.

The only feature variable that isn't numerical is "Sex". It has three labels that we'll need to encode accordingly to fit a model.

## EDA summary

The dataset has been pre-processed by its maintainers. [Quoting](https://archive.ics.uci.edu/dataset/1/abalone) them:

> From the original data examples with missing values were removed (the majority having the predicted value missing), and the ranges of the continuous values have been scaled for use with an ANN (by dividing by 200).

In spite of that, we found some "Height" measurements equal to zero. We removed them from the dataset. We did the same with a couple of outliers.

## Modeling approach & metrics

TODO.

## Known limitations / next steps

TODO.

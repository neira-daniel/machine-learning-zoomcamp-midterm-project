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

## Using Docker

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

TODO.

## Dataset description

TODO.

## EDA summary

TODO.

## Modeling approach & metrics

TODO.

## How to run locally and via Docker

TODO.

## API usage example

TODO.

## Known limitations / next steps

TODO.

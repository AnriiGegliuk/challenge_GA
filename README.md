# Titanic Prediction Service
This service provides API to predict survival probability for passengers on the Titanic dataset based on their characteristics.
It provides both synchronous and asynchronous prediction endpoints.

### Features:

- **Synchronous API:** Get immediate prediction results
- **Asynchronous API:** Submit prediction jobs and retrieve results later
- **Containerized:** Run as a Docker container
- **Deployed:** Artifact registry on GCP

# URL for API:

```
https://titanic-prediction-service-897833203261.europe-west2.run.app
```


## Quick Start

1. Clone the repository.

   ```bash
   git clone https://github.com/AnriiGegliuk/challenge_GA.git
   ```

2. Set up the environment. For details including how to install uv, see [Setup](docs/setup.md).

    ```sh
    cd challenge_GA  # move to the cloned directory
    uv python install 3.12 # install 3.12 python (will be recomended since .venv is build on uv and 3.12)
    uv python pin 3.12 # fix the version
    uv sync           # before running this command, you need to install uv and ensure that
    ```


# Building the Docker Image

From the project root directory, after above steps run:

```
docker build -t titanic-api .
```

Above command will build a Docker image named `titanic-api`

## Running the Docker Container

```
docker run -p 8080:8080 titanic-api
```

To acess API use this link: http://localhost:8080

# API Documentation

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/titanic_sync` | Synchronous prediction |
| POST | `/titanic_async` | Asynchronous prediction (returns job ID) |
| GET | `/titanic_async/{job_id}` | Retrieve results of an asynchronous job |

To run Health check of API run following command in the terminal:

```
curl -X GET "https://titanic-prediction-service-897833203261.europe-west2.run.app/"
```

Above command should return json response in the terminal:

```
{"message":"OK","docs":"API documentation inside /docs"}
```

For Synchronous Prediction with endpoint: `/titanic_sync`
Method: POST

```
curl -X POST "https://titanic-prediction-service-897833203261.europe-west2.run.app/titanic_sync" \
  -H "Content-Type: application/json" \
  -d '{"data": [{"Pclass": 1, "Sex": "male", "Age": 30, "SibSp": 0, "Fare": 50, "Embarked": "S"}]}'

```


For Asynchronous Prediction with endpoint `/titanic_async`
Method: POST

```
curl -X POST "https://titanic-prediction-service-897833203261.europe-west2.run.app/titanic_async" \
  -H "Content-Type: application/json" \
  -d '{"data": [{"Pclass": 1, "Sex": "male", "Age": 30, "SibSp": 0, "Fare": 50, "Embarked": "S"}]}'

```

Check the status with the `job_id` you received from the previous request:

```
curl -X GET "https://titanic-prediction-service-897833203261.europe-west2.run.app/titanic_async/job_id_specified_here"
```





Interactive Documentation
For interactive testing, visit:

```
https://titanic-prediction-service-897833203261.europe-west2.run.app/docs

```

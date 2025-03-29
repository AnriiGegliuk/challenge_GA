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
    cd mri_pipelines  # Move to the cloned directory
    uv python install 3.12
    uv python pin 3.12
    uv sync           # before running this command, you need to install uv.
    ```


# Docker build

.....

# Test URL

In terminal:

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

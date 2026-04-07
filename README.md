# Machine Learning Web Application
*Demo project using FastAPI & Streamlit, with GitHub Actions for CI/CD.*

## Overview Of Featured Services

### 1. Model Training
- Synthetic dataset generation
- Model serialization with Joblib

### 2. FastAPI Service
- Input validation using Pydantic
- SQLite logging of predictions

### 3. Streamlit UI
- Interactive single prediction sliders
- Single/Batch prediction execution
- Option to generate charts from the predictions

### 4. Containerized Workflow With Docker Compose
- Build Docker images (manually or via CI)
- Manage services with Docker Compose

### 5. (Optional) Kubernetes Orchestration
- Kubernetes manifests are included to test the deployment workflow in GitHub Actions.

---

## Overview Of Git Practices & GitHub Actions

### Git Practices

During this work, I used feature branches to simulate real-world development practices:
1. Create new branches for specific tasks.
2. Make multiple commits after major changes.
3. Push the branch and let CI workflows run.
4. If tests pass, open a PR to main and delete the feature branch after merge.

### GitHub Actions

This project includes three workflows under `.github/workflows/`:
- `tests.yml`: installs dependencies, checks syntax, runs ruff linting, trains the model as a smoke test, and runs pytest.
    - About ruff: A very fast Python tool that checks the code for problems and style issues.
    - About pytest: Another Python tool that automatically runs tests on code to check that it works as expected.
- `docker.yml`: builds and pushes Docker images for `train`, `api`, and `streamlit` to Docker Hub.
- `deploy.yml`: manual deploy to a self-hosted Minikube runner.
    - About self-hosted run: Since GitHub runners cannot access a local Minikube cluster. We need to set it up locally:
        1. Go to Settings → Actions → Runners → Download & install
        2. Setup the runner locally like:
        ```bash
        mkdir actions-runner && cd actions-runner
        curl -o actions-runner.tar.gz -L https://...
        tar xzf ./actions-runner.tar.gz
        ./config.sh --url https://github.com/user/repo-name --token XXX --label minikube
        ./run.sh
        ```
        - Then GitHub just sends jobs to it

**Typical CI/CD flow in this repo:**

    Push feature branch
     └── actions will trigger if we added the branch in workflow file
        ↓
    CI
     ├── install dependencies
     ├── run linter
     ├── run pytest
     └── build project
        ↓
    CD
     ├── build Docker image
     ├── push image to registry
     └── deploy to server
        ↓
    Make PR to main

---

## Project Structure

    project-root/
    │
    ├─ src/
    │  ├─ api/
    │  │  ├─ main.py
    │  │  └─ db.py
    │  ├─ app/
    │  │  └─ streamlit_app.py
    │  └─ model/
    │     └─ train_model.py
    │
    ├─ docker/
    │  ├─ Dockerfile.train
    │  ├─ Dockerfile.inference
    │  └─ Dockerfile.streamlit
    │
    ├─ k8s/
    ├─ db/
    ├─ output/
    ├─ requirements.txt
    └─ docker-compose.yml

---
## Webapp Snapshots
### Streamlit Prediction Options:
![Streamlit prediction options](https://github.com/bencetaro/mlops_streamlit_app/blob/main/images/streamlit1.png)
  
### Visualized Statistics:
![Streamlit visualization](https://github.com/bencetaro/mlops_streamlit_app/blob/main/images/streamlit2.png)

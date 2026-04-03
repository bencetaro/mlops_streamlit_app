# Machine Learning Web Application Demo
*Demo project using FastAPI & Streamlit, with GitHub Actions for CI/CD.*

The CI/CD workflows include:
- Test the codebase
- Build Docker images
- Push images to Docker Hub
- (Optional) Deploy services with Kubernetes

## Overview of Featured Services

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

### 4. Containerized workflow with Docker Compose
- Image building and service running is handled by Docker Compose

## Overview of Git Practices & GitHub Actions

### GitHub Actions

There are three distinct workflows defined under `.github/workflows/`:
- `tests.yml` (smoke tests and syntax check)
- `docker.yml` (build and push Docker images)
- `deploy.yml` (manual deploy to a Minikube self-hosted runner)

### Git Practices
Throughout the work, I made different feature branches for better simulation of a production environment practices like:
- Making new branches for certain tasks.
- In the new branches, creating several commits after main changes are done.
- After finishing the work on a branch, making PRs to main branch, and deleting the feature branch.


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
## Webapp snapshots
### Streamlit prediction options:
![Streamlit prediction options](https://github.com/bencetaro/mlops_streamlit_app/blob/main/images/streamlit1.png)
  
### Visualized statistics:
![Streamlit visualization](https://github.com/bencetaro/mlops_streamlit_app/blob/main/images/streamlit2.png)

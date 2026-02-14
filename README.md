# Housing Price Estimator (Demo project using FastAPI & Streamlit)

## Overview

This project is a mini MLOps demo application that demonstrates how to:
- Serve predictions via REST API using FastAPI
- Build an interactive UI with Streamlit
- Perform batch predictions from CSV files
- Visualize prediction statistics and correlations
- Containerize the full stack using Docker and Docker Compose
- Log predictions into a SQLite database

The project is designed for learning purposes, focusing on the interaction between Data Science and backend/web technologies.

---

## Tech Stack

**Backend**
- FastAPI
- Uvicorn
- Pydantic
- SQLite

**Frontend**
- Streamlit
- Matplotlib
- Seaborn

**Machine Learning**
- Scikit-learn
- NumPy
- Pandas
- Joblib

**DevOps**
- Docker
- Docker Compose

---

## Features

### 1. Model Training
- Synthetic dataset generation
- Model serialization with Joblib

### 2. FastAPI Service
- Single prediction endpoint
- Batch prediction endpoint
- Input validation using Pydantic
- SQLite logging of predictions

### 3. Streamlit UI
- Interactive single prediction sliders
- CSV batch upload
- Batch prediction execution
- Option to generate charts from the predicitons

---
## Project Structure

    project-root/
    │
    ├─ api/
    │ ├─ main.py
    │ └─ db.py
    │
    ├─ app/
    │ └─ streamlit_app.py
    │
    ├─ model/
    │ └─ train_model.py
    │
    ├─ docker/
    │ ├─ Dockerfile.train
    │ ├─ Dockerfile.inference
    │ └─ Dockerfile.streamlit
    │
    ├─ db/
    ├─ output/
    ├─ requirements.txt
    └─ docker-compose.yml

---
## Visualization Results

![Streamlit prediction options](https://github.com/bencetaro/mlops_streamlit_app/blob/main/images/streamlit1.png)
  

![Streamlit visualization](https://github.com/bencetaro/mlops_streamlit_app/blob/main/images/streamlit2.png)

# Nutrition Analysis API

This API analyzes food ingredients and provides nutritional insights using AI.

## Setup

1. Create a virtual environment:
```
python -m venv .venv
```
2. Activate the virtual environment:
```
source .venv/bin/activate
```
3. Install the dependencies:
```
pip install -r requirements.txt
```
4. Run the application:
```
uvicorn server:app --host 0.0.0.0 --port 8000
```

## Docker

1. Build the Docker image:
```
docker build -t nutrition-analysis-api .
```
2. Run the Docker container:
```
docker run -d -p 8000:8000 nutrition-analysis-api
```